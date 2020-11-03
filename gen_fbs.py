#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import os
import xlrd
import json

import queue
from excel_parser.excel_parser import ExcelParser


"""
```python
python3 gen_fbs.py EXCEL_DIR OUTPUT_DIR
```

根据 Excel 配置表生成 FBS
"""


class CONFIG:
    PATH = './config.json'
    KEY_NAMESPACE = 'namespace'
    KEY_FILEHEADER = 'file_header'
    KEY_TYPEREPLACE = 'type_replace'


ExcelParser = ExcelParser()

output_dir = ''
solved_head = {}
solved_tail = {}

global_config = {}


def prepare_global_config():
    global global_config

    if os.path.isfile(CONFIG.PATH):
        with open(CONFIG.PATH, 'r', encoding='utf-8') as config_file:
            global_config = json.loads(config_file.read())

    if CONFIG.KEY_FILEHEADER not in global_config:
        global_config[CONFIG.KEY_FILEHEADER] = ''

    if CONFIG.KEY_NAMESPACE not in global_config:
        global_config[CONFIG.KEY_NAMESPACE] = 'Default'

    if CONFIG.KEY_TYPEREPLACE not in global_config:
        global_config[CONFIG.KEY_TYPEREPLACE] = {}

    print(f"Global Config: {global_config}")


def solve_type(t):
    global global_config

    if t in global_config[CONFIG.KEY_TYPEREPLACE].keys():
        t = global_config[CONFIG.KEY_TYPEREPLACE][t]

    return t


def solve_sheet(sheet):
    global ExcelParser, output_dir, global_config

    print(f'- solve sheet {sheet.name}')

    output_filename = sheet.name.upper()
    output_filepath = os.path.join(output_dir, output_filename + '.fbs')

    ncols = sheet.ncols
    endCol = ncols - 1

    class_define = ExcelParser.parse_with_sheet(sheet, 0, endCol)

    # 如果没有处理过文件头，则在这里处理文件头
    if output_filename not in solved_head:
        solved_head[output_filename] = True
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            # 写入文件头内容
            outfile.write(global_config[CONFIG.KEY_FILEHEADER])

            outfile.write('\n')

            # 写入命名空间
            outfile.write(
                f'namespace {global_config[CONFIG.KEY_NAMESPACE]};\n\n')

    struct_queue = queue.Queue()
    struct_define = ""

    with open(output_filepath, 'a', encoding='utf-8') as outfile:
        outfile.write(f"table {sheet.name.upper()} {{\n")
        ret = ''
        for item in class_define:
            # 数组
            if item['type'].startswith('[]'):
                if item['type'] == '[]struct':
                    ret += f'    {item["name"]}: [{item["name"]}_struct_type];\n'
                    struct_d, append_struct = gen_struct(item)
                    struct_define += struct_d
                    for i in append_struct:
                        struct_queue.put(i)
                else:
                    ret += f'    {item["name"]}: [{solve_type(item["type"][2:])}];\n'
            elif item['type'] == 'struct':
                ret += f'    {item["name"]}: {item["name"]}_struct_type;\n'
                struct_d, append_struct = gen_struct(item)
                struct_define += struct_d
                for i in append_struct:
                    struct_queue.put(i)
            else:
                ret += f'    {item["name"]}: {solve_type(item["type"])};\n'

        outfile.write(ret)
        outfile.write(f"}}\n\n")

        while not struct_queue.empty():
            struct_d, append_struct = gen_struct(struct_queue.get())
            struct_define += struct_d
            for i in append_struct:
                struct_queue.put(i)

        outfile.write(struct_define)

        outfile.write(f"""
table {sheet.name.upper()}_ARR {{
    data: [{sheet.name.upper()}];
}}

root_type {sheet.name.upper()}_ARR;

""")


def gen_struct(table_dict):
    struct_type = table_dict['struct_type']
    ret = f'table {table_dict["name"]}_struct_type {{\n'
    append_struct = []
    for item in struct_type:
        if item['type'].startswith('[]'):
            if item['type'] == '[]struct':
                ret += f'    {item["name"]}: [{item["name"]}_struct_type];\n'
                append_struct.append(item)
            else:
                ret += f'    {item["name"]}: [{solve_type(item["type"][2:])}];\n'
        elif item['type'] == 'struct':
            ret += f'    {item["name"]}: {item["name"]}_struct_type;\n'
            append_struct.append(item)
        else:
            ret += f'    {item["name"]}: {solve_type(item["type"])};\n'

    ret += f'}}\n\n'

    return ret, append_struct


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


def gen(config_path):
    '''
    根据配置目录，生成对应的fbs文件
    '''
    if os.path.isfile(config_path):
        gen_file(config_path)
    else:
        gen_dir(config_path)


def main():
    if len(sys.argv) != 3:
        print('python3 gen_fbs.py EXCEL_DIR OUTPUT_DIR')
        sys.exit(-1)

    global output_dir
    output_dir = os.path.abspath(sys.argv[2])

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    prepare_global_config()

    gen(sys.argv[1])


if __name__ == '__main__':
    main()
