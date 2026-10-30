//! Experimental PDF reader only; the application UI and compatibility engine remain Python.
//! All PDFium calls run on this one thread. stdout is exclusively the original wire protocol.
use libloading::Library;
use serde_json::{json, Value};
use std::{
    collections::{HashMap, VecDeque},
    env,
    ffi::{c_char, c_int, c_ulong, c_void, CString},
    fs,
    io::{self, BufRead, BufReader, Read, Write},
    path::{Path, PathBuf},
    process::{Child, ChildStdin, ChildStdout, Command, Stdio},
    ptr,
    rc::Rc,
    time::SystemTime,
};

type Handle = *mut c_void;
type R<T> = Result<T, String>;
const MAX_BYTES: usize = 75_000_000;
const MAX_LINE: u64 = 8 * 1024 * 1024;

#[repr(C)]
struct Matrix {
    a: f32,
    b: f32,
    c: f32,
    d: f32,
    e: f32,
    f: f32,
}
#[repr(C)]
struct Rect {
    left: f32,
    top: f32,
    right: f32,
    bottom: f32,
}

// PDFium public/fpdfview.h. `system` matches FPDF_CALLCONV on supported Windows x64.
struct Api {
    load: unsafe extern "system" fn(*const c_char, *const c_char) -> Handle,
    close: unsafe extern "system" fn(Handle),
    count: unsafe extern "system" fn(Handle) -> c_int,
    page: unsafe extern "system" fn(Handle, c_int) -> Handle,
    close_page: unsafe extern "system" fn(Handle),
    bitmap: unsafe extern "system" fn(c_int, c_int, c_int, *mut c_void, c_int) -> Handle,
    close_bitmap: unsafe extern "system" fn(Handle),
    fill: unsafe extern "system" fn(Handle, c_int, c_int, c_int, c_int, c_ulong) -> c_int,
    buffer: unsafe extern "system" fn(Handle) -> *mut c_void,
    stride: unsafe extern "system" fn(Handle) -> c_int,
    render: unsafe extern "system" fn(Handle, Handle, *const Matrix, *const Rect, c_int),
    destroy: unsafe extern "system" fn(),
    _lib: Library,
}
impl Api {
    fn open(path: &Path) -> R<Rc<Self>> {
        // The caller supplies the same trusted absolute library as the Python baseline.
        if !path.is_absolute() {
            return Err("PDFium library path must be absolute".into());
        }
        unsafe {
            let lib = Library::new(path).map_err(|e| e.to_string())?;
            macro_rules! get {
                ($n:literal) => {
                    *lib.get(concat!($n, "\0").as_bytes())
                        .map_err(|e| e.to_string())?
                };
            }
            let init: unsafe extern "system" fn() = get!("FPDF_InitLibrary");
            let api = Self {
                load: get!("FPDF_LoadDocument"),
                close: get!("FPDF_CloseDocument"),
                count: get!("FPDF_GetPageCount"),
                page: get!("FPDF_LoadPage"),
                close_page: get!("FPDF_ClosePage"),
                bitmap: get!("FPDFBitmap_CreateEx"),
                close_bitmap: get!("FPDFBitmap_Destroy"),
                fill: get!("FPDFBitmap_FillRect"),
                buffer: get!("FPDFBitmap_GetBuffer"),
                stride: get!("FPDFBitmap_GetStride"),
                render: get!("FPDF_RenderPageBitmapWithMatrix"),
                destroy: get!("FPDF_DestroyLibrary"),
                _lib: lib,
            };
            init();
            Ok(Rc::new(api))
        }
    }
}
impl Drop for Api {
    fn drop(&mut self) {
        unsafe { (self.destroy)() }
    }
}

#[derive(PartialEq)]
struct Signature {
    len: u64,
    modified: Option<SystemTime>,
    created: Option<SystemTime>,
    inode: u64,
}
fn signature(path: &str) -> R<Signature> {
    let m = fs::metadata(path).map_err(|e| e.to_string())?;
    #[cfg(unix)]
    let inode = {
        use std::os::unix::fs::MetadataExt;
        m.ino()
    };
    #[cfg(not(unix))]
    let inode = 0;
    Ok(Signature {
        len: m.len(),
        modified: m.modified().ok(),
        created: m.created().ok(),
        inode,
    })
}
struct Document {
    api: Rc<Api>,
    handle: Handle,
    signature: Signature,
    geometry: HashMap<i64, Value>,
}
impl Drop for Document {
    fn drop(&mut self) {
        unsafe { (self.api.close)(self.handle) }
    }
}
struct Page {
    api: Rc<Api>,
    handle: Handle,
}
impl Drop for Page {
    fn drop(&mut self) {
        unsafe { (self.api.close_page)(self.handle) }
    }
}
struct Bitmap {
    api: Rc<Api>,
    handle: Handle,
}
impl Drop for Bitmap {
    fn drop(&mut self) {
        unsafe { (self.api.close_bitmap)(self.handle) }
    }
}

struct Packet {
    header: Value,
    bytes: Vec<u8>,
}
fn ok(value: Value) -> Packet {
    Packet {
        header: value,
        bytes: Vec::new(),
    }
}

struct Compatibility {
    command: Vec<String>,
    child: Option<Child>,
    input: Option<ChildStdin>,
    output: Option<BufReader<ChildStdout>>,
}
impl Compatibility {
    fn start(&mut self) -> R<()> {
        if self.child.is_some() {
            return Ok(());
        }
        let (program, args) = self
            .command
            .split_first()
            .ok_or("Compatibility worker command is missing")?;
        let mut cmd = Command::new(program);
        cmd.args(args)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::inherit());
        #[cfg(windows)]
        {
            use std::os::windows::process::CommandExt;
            cmd.creation_flags(0x08000000);
        }
        let mut child = cmd.spawn().map_err(|e| e.to_string())?;
        self.input = child.stdin.take();
        self.output = child.stdout.take().map(BufReader::new);
        self.child = Some(child);
        Ok(())
    }
    fn request(&mut self, request: &Value) -> R<Packet> {
        self.start()?;
        let result = self.exchange(request);
        if result.is_err() {
            self.stop();
        } // Never replay a failed write/edit request.
        result
    }
    fn exchange(&mut self, request: &Value) -> R<Packet> {
        let input = self
            .input
            .as_mut()
            .ok_or("Compatibility stdin unavailable")?;
        serde_json::to_writer(&mut *input, request).map_err(|e| e.to_string())?;
        input
            .write_all(b"\n")
            .and_then(|_| input.flush())
            .map_err(|e| e.to_string())?;
        let output = self
            .output
            .as_mut()
            .ok_or("Compatibility stdout unavailable")?;
        let mut line = Vec::new();
        (&mut *output)
            .take(MAX_LINE + 1)
            .read_until(b'\n', &mut line)
            .map_err(|e| e.to_string())?;
        if line.is_empty() || line.len() as u64 > MAX_LINE || !line.ends_with(b"\n") {
            return Err("Invalid compatibility response header".into());
        }
        let header: Value = serde_json::from_slice(&line).map_err(|e| e.to_string())?;
        if header.get("id") != request.get("id") {
            return Err("Compatibility response id mismatch".into());
        }
        let size = match header.get("nbytes") {
            None => 0,
            Some(n) => n.as_u64().ok_or("Invalid frame length")?,
        };
        if size > MAX_BYTES as u64 {
            return Err("Compatibility frame exceeds GUI limit".into());
        }
        let mut bytes = vec![0; size as usize];
        output.read_exact(&mut bytes).map_err(|e| e.to_string())?;
        Ok(Packet { header, bytes })
    }
    fn stop(&mut self) {
        self.input.take();
        self.output.take();
        if let Some(mut child) = self.child.take() {
            let _ = child.kill();
            let _ = child.wait();
        }
    }
}
impl Drop for Compatibility {
    fn drop(&mut self) {
        self.stop()
    }
}

struct Worker {
    api: Rc<Api>,
    docs: VecDeque<(String, Document)>,
    compat: Compatibility,
}
impl Worker {
    fn document(&mut self, path: &str) -> R<&mut Document> {
        let sig = signature(path)?;
        if let Some(i) = self.docs.iter().position(|(p, _)| p == path) {
            let old = self.docs.remove(i).unwrap();
            if old.1.signature == sig {
                self.docs.push_back(old);
                return Ok(&mut self.docs.back_mut().unwrap().1);
            }
        }
        let name = CString::new(path).map_err(|_| "File path contains NUL")?;
        let handle = unsafe { (self.api.load)(name.as_ptr(), ptr::null()) };
        if handle.is_null() {
            return Err("PDFium could not open this PDF".into());
        }
        if unsafe { (self.api.count)(handle) } < 1 {
            unsafe { (self.api.close)(handle) };
            return Err("PDF contains no pages".into());
        }
        self.docs.push_back((
            path.to_owned(),
            Document {
                api: self.api.clone(),
                handle,
                signature: sig,
                geometry: HashMap::new(),
            },
        ));
        while self.docs.len() > 4 {
            self.docs.pop_front();
        }
        Ok(&mut self.docs.back_mut().unwrap().1)
    }
    fn fallback(&mut self, request: &Value, reason: &str) -> R<Packet> {
        let mut packet = self.compat.request(request)?;
        packet.header["engine"] = json!("python-compat");
        packet.header["fallback_reason"] = json!(reason);
        Ok(packet)
    }
    fn request(&mut self, request: &Value) -> R<Packet> {
        let op = request["op"]
            .as_str()
            .ok_or("Request op must be a string")?;
        if op == "release" {
            self.docs.clear();
            return if self.compat.child.is_some() {
                self.fallback(request, "release compatibility handles")
            } else {
                Ok(ok(json!({"engine":"rust-pdfium"})))
            };
        }
        if op == "inspect" {
            let path = request["path"]
                .as_str()
                .ok_or("File path must be a string")?;
            return match self.document(path) {
                Ok(doc) => Ok(ok(
                    json!({"count":unsafe{(doc.api.count)(doc.handle)},"engine":"rust-pdfium"}),
                )),
                Err(reason) => self.fallback(request, &reason),
            };
        }
        if matches!(op, "preview" | "render") && request["payload"]["raw_frame"] == true {
            return match self.render(request) {
                Ok(packet) => Ok(packet),
                Err(reason) => self.fallback(request, &reason),
            };
        }
        // Release native file handles before delegating editing, batch saves, and all other operations.
        self.docs.clear();
        self.fallback(request, "operation retained in original engine")
    }
    fn render(&mut self, request: &Value) -> R<Packet> {
        let path = request["path"]
            .as_str()
            .ok_or("File path must be a string")?;
        let index = request["page"]
            .as_i64()
            .filter(|n| *n >= 0 && *n <= i32::MAX as i64)
            .ok_or("Invalid page index")?;
        let cached = {
            let d = self.document(path)?;
            d.geometry.get(&index).cloned()
        };
        let geometry = match cached {
            Some(g) => g,
            None => {
                let meta = self.compat.request(
                    &json!({"id":request["id"],"op":"_rust_geometry","path":path,"page":index}),
                )?;
                if meta.header["ok"] != true {
                    return Err("Original metadata reader rejected the page".into());
                }
                let g = meta.header["geometry"].clone();
                self.document(path)?.geometry.insert(index, g.clone());
                g
            }
        };
        if geometry["compatible"] != true {
            return Err("Widget or nonstandard geometry: use original renderer".into());
        }
        let w = geometry["width"].as_f64().ok_or("Missing width")?;
        let h = geometry["height"].as_f64().ok_or("Missing height")?;
        let unit = geometry["unit"].as_f64().ok_or("Missing UserUnit")?;
        let scale = if request["op"] == "preview" {
            request
                .get("max_side")
                .and_then(Value::as_f64)
                .unwrap_or(1800.)
                .clamp(1000., 5000.)
                / w.max(h).max(1.)
        } else {
            let side = request["payload"]
                .get("thumb_side")
                .and_then(Value::as_f64)
                .unwrap_or(370.);
            (side * 280. / 370. / w.max(1.)).min(side / h.max(1.))
        };
        if !scale.is_finite() || scale <= 0. {
            return Err("Invalid scale".into());
        }
        let width = (w * scale - 1e-8).ceil();
        let height = (h * scale - 1e-8).ceil();
        if !(1. ..=5000.).contains(&width) || !(1. ..=5000.).contains(&height) {
            return Err("Frame exceeds GUI dimensions".into());
        }
        let (width, height) = (width as usize, height as usize);
        let size = width
            .checked_mul(height)
            .and_then(|n| n.checked_mul(3))
            .filter(|n| *n <= MAX_BYTES)
            .ok_or("Frame exceeds GUI limit")?;
        let api = self.api.clone();
        let doc = self.document(path)?;
        let raw_page = unsafe { (api.page)(doc.handle, index as c_int) };
        if raw_page.is_null() {
            return Err("PDFium could not load the page".into());
        }
        let page = Page {
            api: api.clone(),
            handle: raw_page,
        };
        let handle =
            unsafe { (api.bitmap)(width as c_int, height as c_int, 2, ptr::null_mut(), 0) };
        if handle.is_null() {
            return Err("PDFium could not allocate the bitmap".into());
        }
        let bitmap = Bitmap {
            api: api.clone(),
            handle,
        };
        let matrix = Matrix {
            a: (scale * unit) as f32,
            b: 0.,
            c: 0.,
            d: (scale * unit) as f32,
            e: 0.,
            f: 0.,
        };
        let clip = Rect {
            left: 0.,
            top: 0.,
            right: (w * scale) as f32,
            bottom: (h * scale) as f32,
        };
        unsafe {
            (api.fill)(
                bitmap.handle,
                0,
                0,
                width as c_int,
                height as c_int,
                0xffffffff,
            );
            (api.render)(bitmap.handle, page.handle, &matrix, &clip, 0x01 | 0x10);
        }
        let stride = unsafe { (api.stride)(bitmap.handle) };
        let data = unsafe { (api.buffer)(bitmap.handle) } as *const u8;
        if data.is_null() || stride < width as c_int * 3 {
            return Err("Invalid PDFium buffer".into());
        }
        let mut bytes = vec![0u8; size];
        // PDFium may align rows to four bytes; GUI receives tightly packed RGB.
        for y in 0..height {
            unsafe {
                ptr::copy_nonoverlapping(
                    data.add(y * stride as usize),
                    bytes.as_mut_ptr().add(y * width * 3),
                    width * 3,
                )
            }
        }
        Ok(Packet {
            header: json!({"width":width,"height":height,"stride":width*3,"nbytes":size,"engine":"rust-pdfium"}),
            bytes,
        })
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().skip(1).collect();
    if args == ["--version"] {
        println!("viewer-rust-worker 0.1.0 (hybrid PDF reader experiment)");
        return Ok(());
    }
    let value = |flag: &str| {
        args.iter()
            .position(|a| a == flag)
            .and_then(|i| args.get(i + 1))
    };
    let path = PathBuf::from(value("--pdfium").ok_or("--pdfium PATH is required")?);
    let command: Vec<String> = serde_json::from_str(
        value("--fallback-json").ok_or("--fallback-json JSON_ARRAY is required")?,
    )?;
    if command.is_empty() {
        return Err("Empty compatibility command".into());
    }
    let api = Api::open(&path)?;
    let mut worker = Worker {
        api,
        docs: VecDeque::new(),
        compat: Compatibility {
            command,
            child: None,
            input: None,
            output: None,
        },
    };
    let stdin = io::stdin();
    let mut input = stdin.lock();
    let stdout = io::stdout();
    let mut output = stdout.lock();
    loop {
        let mut line = Vec::new();
        let n = (&mut input)
            .take(MAX_LINE + 1)
            .read_until(b'\n', &mut line)?;
        if n == 0 {
            break;
        }
        if line.len() as u64 > MAX_LINE || !line.ends_with(b"\n") {
            return Err("Request line exceeds limit or is incomplete".into());
        }
        let parsed = serde_json::from_slice::<Value>(&line);
        let id = parsed
            .as_ref()
            .ok()
            .and_then(|v| v.get("id"))
            .cloned()
            .unwrap_or(Value::Null);
        let result = parsed
            .map_err(|e| e.to_string())
            .and_then(|req| worker.request(&req));
        let mut packet = match result {
            Ok(p) => p,
            Err(e) => ok(json!({"ok":false,"error":e,"engine":"rust-error"})),
        };
        packet.header["id"] = id;
        if packet.header.get("ok").is_none() {
            packet.header["ok"] = json!(true)
        }
        serde_json::to_writer(&mut output, &packet.header)?;
        output.write_all(b"\n")?;
        output.write_all(&packet.bytes)?;
        output.flush()?;
    }
    worker.docs.clear();
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn ffi_layout_matches_pdfium() {
        assert_eq!(std::mem::size_of::<Matrix>(), 24);
        assert_eq!(std::mem::size_of::<Rect>(), 16);
    }
}
