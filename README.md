# Excel2Flatbuffer

根据 Excel 表内容生成对应的 FBS 定义文件、二进制数据文件、Lua 访问脚本

## Excel 配置规则

- Excel Sheet 名全大写且不以'#'开头，则为合法配置
- 支持 flatbuffer 支持的类型
- 支持类型替换配置（兼容自定义类型）

## 依赖

- python3
- xlrd 1.2.0
- lua
- flatc（https://github.com/google/flatbuffers）

## 脚本配置说明

配置文件：config.json

- namespace：FBS 命名空间
- file_header：每个生成的 FBS 文件头部自动添加该内容（可以处理统一的 include 或说明等）
- type_replace：类型替换，前面是待替换的类型（flatbuffer 不支持的类型），后面是替换的类型（flatbuffer支持的类型）

## 脚本说明

- `gen_fbs.py`

    ```python
    python3 gen_fbs.py EXCEL_DIR OUTPUT_DIR
    ```

    根据 Excel 配置表生成 FBS

- `gen_luatable.py`

    ```python
    python3 gen_luatable.py EXCEL_DIR OUTPUT_DIR
    ```

    根据 Excel 配置表生成包含数据的 Lua 表

- `gen_json.py`

    依赖 Lua 解释器

    ```python
    python3 gen_json.py LUATABLE_DIR OUTPUT_DIR
    ```

    根据 Lua 表生成 Json 文件

- `gen_bin.py`

    ```python
    python3 gen_bin.py FBS_DIR JSON_DIR OUTPUT_DIR
    ```

    根据 FBS 及 Json 生成对应的二进制数据文件

- `gen_lua.py`

    ```python
    python3 gen_lua.py FBS_DIR OUTPUT_DIR
    ```

    根据 FBS 生成对应的辅助 Lua 脚本

- `gen_luautils.py`

    ```python
    python3 gen_luautils.py EXCEL_DIR BIN_DIR NAMESPACE LUA_DIR OUTPUT_PATH
    ```

    根据 Excel 配置，生成对应的 Lua 辅助脚本
