# Demo

## 测试平台

- 系统: macOS 10.15.4
- python: 3.8.5
- xlrd: 1.3.0
- lua: 5.3.5
- flac: https://github.com/yangruihan/flatbuffers

## 运行

```sh
./gen.sh

export LUA_PATH="output/lua/?.lua;./?.lua;"
lua demo.lua
```
