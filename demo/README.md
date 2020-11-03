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

## 输出

```
100001
这是一个测试道具
1
5
```

## 说明

由于修改了 flatc 的源码，生成的 Lua 辅助脚本不再需要使用方法的方式访问对应字段，具体修改可查看：

- https://github.com/yangruihan/flatbuffers/commit/6abd2754b63e0f983567e9748a23b8e60b216db6
- https://github.com/yangruihan/flatbuffers/commit/ded9b7b1b06e25f34fe710ab1cf03d3650930061
