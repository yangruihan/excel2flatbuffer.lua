#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import os
import xlrd
from excel_parser.excel_parser import ExcelParser


"""
```python
python3 gen_luautils.py EXCEL_DIR BIN_DIR NAMESPACE LUA_DIR OUTPUT_PATH
```

根据 Excel 配置，生成对应的 Lua 辅助脚本
"""

LUA_DATACONFIG_MANAGER_TEMPLATE = \
    r"""
------------------------------
---该文件由工具自动生成
---DataConfigManager
------------------------------

---@class DataConfigManager
local DataConfigManager = {}

DataConfigManager.BinPath = "%{BIN_DIR}"
DataConfigManager.LuaPath = "%{LUA_PATH}"

local flatbuffers = require(string.format("%s.%s", DataConfigManager.LuaPath, "flatbuffers"))

local function BinaryFindCfgById(id, cfg)
    local len = #cfg.data
    local left, right, mid = 1, len, 0
    while left <= right do
        mid = math.ceil((left + right) / 2)
        local itemCfg = cfg.data[mid]
        local itemCfgId = itemCfg.id

        if id == itemCfgId then
            return itemCfg
        elseif id < itemCfgId then
            right = mid - 1
        else
            left = mid + 1
        end
    end

    return nil
end

local function FindCfgByKey(key, cfg, keyField)
    local len = #cfg.data
    for i = 1, len do
        local item = cfg.data[i]
        if item[keyField] == key then
            return item
        end
    end

    return nil
end

%{BODY}

return DataConfigManager

"""

LUA_LOAD_CONF_TEMPLATE = r"""
function DataConfigManager:Load%{CfgName}()
    local file = io.open(string.format("%s/%s.bin", DataConfigManager.BinPath, "%{SheetName}"), "rb")
    local buf = flatbuffers.binaryArray.New(file:read("*a"))
    file:close()

    self.%{SheetName}_ARR = require(string.format("%s.%{Namespace}.%s", DataConfigManager.LuaPath, "%{SheetName}_ARR")).GetRootAs%{SheetName}_ARR(buf, 0)
end
"""

LUA_GET_CONF_TEMPLATE_BY_ID = r"""
function DataConfigManager:Get%{CfgName}(id)
    return BinaryFindCfgById(id, self.%{SheetName}_ARR)
end
"""

LUA_GET_CONF_TEMPLATE_BY_KEY = r"""
function DataConfigManager:Get%{CfgName}(key)
    return FindCfgByKey(key, self.%{SheetName}_ARR, "%{KeyField}")
end
"""

EXCEL_DIR = ''
BIN_DIR = ''
LUA_DIR = ''
OUTPUT_PATH = ''
NAMESPACE = ''

ExcelParser = ExcelParser()

body_content = ''


def normalize_name(name: str):
    idx = 0
    ret = ''
    while idx < len(name):
        if idx == 0:
            ret += name[idx].upper()
        elif name[idx] == '_':
            idx += 1
            if idx < len(name):
                ret += name[idx].upper()
        else:
            ret += name[idx].lower()

        idx += 1

    return ret


def solve_sheet(sheet):
    global ExcelParser, body_content, NAMESPACE

    class_define = ExcelParser.parse_with_sheet(sheet, 0)

    cfg_name = normalize_name(sheet.name)

    load_content = LUA_LOAD_CONF_TEMPLATE \
        .replace("%{CfgName}", cfg_name) \
        .replace("%{SheetName}", sheet.name) \
        .replace("%{Namespace}", NAMESPACE)

    get_cfg = ""

    if class_define[0]["name"] == "id" and class_define[0]["type"] == "uint32":
        get_cfg = LUA_GET_CONF_TEMPLATE_BY_ID \
            .replace("%{CfgName}", cfg_name) \
            .replace("%{SheetName}", sheet.name)
    else:
        get_cfg = LUA_GET_CONF_TEMPLATE_BY_KEY \
            .replace("%{CfgName}", cfg_name) \
            .replace("%{SheetName}", sheet.name) \
            .replace("%{KeyField}", class_define[0]["name"])

    body_content += f"""
{load_content}

{get_cfg}
"""


def gen_file(config_file):
    print(f'start gen_file {config_file} ...')

    book = xlrd.open_workbook(config_file)
    for sheet in book.sheets():
        if sheet.name.isupper() and not sheet.name.startswith('#'):
            solve_sheet(sheet)

    print(f'end gen_file {config_file}')


def gen_dir(config_dir):
    filenames = os.listdir(config_dir)
    for filename in filenames:
        if not filename.startswith("~$"):
            gen_file(os.path.join(config_dir, filename))


def main():
    global EXCEL_DIR, BIN_DIR, LUA_DIR, OUTPUT_PATH, NAMESPACE, body_content

    if len(sys.argv) != 6:
        print('python3 gen_luautils.py EXCEL_DIR BIN_DIR NAMESPACE LUA_DIR OUTPUT_PATH')
        sys.exit(-1)

    EXCEL_DIR = sys.argv[1]
    BIN_DIR = sys.argv[2]
    NAMESPACE = sys.argv[3]
    LUA_DIR = sys.argv[4]
    OUTPUT_PATH = sys.argv[5]

    gen_dir(EXCEL_DIR)

    content = LUA_DATACONFIG_MANAGER_TEMPLATE \
        .replace("%{BIN_DIR}", BIN_DIR) \
        .replace("%{LUA_PATH}", LUA_DIR) \
        .replace("%{BODY}", body_content)

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == "__main__":
    main()
