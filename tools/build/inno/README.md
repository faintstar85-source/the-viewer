# Korean installer messages

`Korean.isl` is the unchanged upstream Inno Setup 6.5.0+ Korean translation.
Its translator credits remain in the file. It is covered by the accompanying
Inno Setup `LICENSE.txt`.

- Upstream: https://github.com/jrsoftware/issrc/blob/main/Files/Languages/Korean.isl
- Upstream Git blob: `c31d21078a0e379aa5d16fc6fdfc24d3fbc25969`
- SHA-256: `a9427833f1975fb13dcaa09bc38aa16eba07698ce9d9596575fdd3362f2646a1`
- License blob: `ac4dfe9e6543a360c5422b6f1fb88075e8b6073d`

When a Windows runner omits this language, the build copies its installed
compiler to the temporary build directory and adds these messages there.
The staged copy adds a UTF-8 BOM to make its encoding explicit. The installed
compiler and the upstream file stored here are unchanged.
