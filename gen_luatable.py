#! /usr/bin/env python
# coding=utf-8

# 主要功能：
#     直接由xls生成lua table，可以跳过策划在任意位置定义的*注释列或空白列
#
# 设计思想：
#    1.生成：先根据xls前5行生成lua table描述信息（用Python字典描述），再生成每一行实例
#    每一个Python字典对应一个lua table，可以嵌套
#    2.合并表：同名输出文件追加写入，后处理阶段统一追加文件尾部
#
# 参数1：xls[x]文件，或为目录，则处理目录下所有文件
# 参数2：输出目录
#
# 依赖:
# 1 xlrd

import sys
import xlrd
import os
import os.path as p


"""
```python
python3 gen_luatable.py EXCEL_DIR OUTPUT_DIR
```

根据 Excel 配置表生成包含数据的 Lua 表

"""

global OUTPUT_DIRECTORY
INDENT = "    "


def is_enum_type(xls_type):
    if type(xls_type) == type("") and xls_type.startswith("enum") and not xls_type.endswith("[]"):
        return True
    else:
        return False


def is_single_arr(xls_type):
    if type(xls_type) == type("") and xls_type.endswith("[]"):
        return True
    else:
        return False


def is_simple_type(xls_type):
    if xls_type == "uint32" or xls_type == "sint32" or xls_type == "float" or xls_type == "string" or xls_type == "int32" \
            or xls_type == "bool" or is_enum_type(xls_type) or xls_type == "DateTime":
        return True
    else:
        return False


# xlrd读取到的xls_value可能为str，也可能为整形或浮点数字
# 最后需要返回string类型的value
def process_value(xls_type, xls_value):
    if xls_value == "":  # 单元格为空
        if xls_type == "string" or xls_type == "DateTime":
            return "''"
        elif xls_type == "uint32" or xls_type == "sint32" or xls_type == "int32" or xls_type == "float":
            return "0"
        elif xls_type == "bool":
            return "false"
        else:
            return "nil"
    else:  # 单元格不为空
        if xls_type == "string" or xls_type == "DateTime":
            if str(xls_value).find("\n") == -1:
                return "\"" + str(xls_value).replace("\"", r"\"") + "\""
            else:
                return "[===[" + str(xls_value).replace("\"", r"\"") + "]===]"
        elif xls_type == "uint32" or xls_type == "sint32" or xls_type == "int32":
            return str(int(float(xls_value)))
        elif xls_type == "bool":
            if xls_value == "false" or xls_value == "FALSE" or xls_value == "False" or xls_value == "0":
                return "false"
            else:
                return "true"
        elif xls_type == "float":
            return str(xls_value)
        elif is_enum_type(xls_type):
            return xls_type + "." + xls_value


def is_skip(proto_type):
    proto_type = proto_type.strip()

    if proto_type == "*" or proto_type == "":
        return True

    return False


def get_next(sheet, x, max=-1):
    if max == -1:
        max = sheet.ncols

    proto_type = sheet.cell_value(0, x)

    while is_skip(proto_type) and x < max:
        x = x + 1
        proto_type = sheet.cell_value(0, x)

    if x == max:
        return -1
    else:
        return x


# 用字典描述的lua table：
# name为成员名，class_define[name]中对应类型描述，为字符串描述或对应的类型变量：
#   基本变量：字符串描述
#   单列数组：字符串描述 + []
#   简单元素分列数组：[]，数组成员为字符串描述的类型
#   结构体：{}，{}中为子类描述
#   结构体数组：[{}]，{}为每个子类描述，注意因为记录列不同，每个子类描述是不一样的
#
# __line字典中记录成员名对应出现在excel中哪一列：
#   基本变量：出现列
#   单列数组：出现列
#   简单元素分列数组：数组声明出现列（备注：注释、无效列在生成实例时处理）
#   结构体：结构体声明出现列
#   结构体数组：数组声明出现列
def parse_class(sheet, start_col, end_col, max_element=sys.maxsize):
    class_define = {"__line": {}}

    i = start_col
    solved_element = 0
    calc_invalid_num = 0

    while i <= end_col and solved_element < max_element:
        proto_type = sheet.cell_value(0, i)
        lua_type = sheet.cell_value(1, i)
        name = sheet.cell_value(2, i)
        comment = str(sheet.cell_value(4, i)).replace(
            '\n', '').replace('\r', '')

        if comment != "":
            comment = " @" + comment

        if proto_type == "repeated":
            if isinstance(lua_type, int) or isinstance(lua_type, float):  # 不是单列数组
                num = int(lua_type)

                x = get_next(sheet, i + 1)

                next_proto_type = sheet.cell_value(0, x)
                next_lua_type = sheet.cell_value(1, x)
                next_name = sheet.cell_value(2, x)
                next_comment = str(sheet.cell_value(4, x)).replace(
                    '\n', '').replace('\r', '')

                if next_comment != "":
                    next_comment = " @" + next_comment

                if next_proto_type == "required_struct" or next_proto_type == "optional_struct":  # 结构体数组
                    struct_element_num = int(next_lua_type)

                    class_define[next_name] = [{}] * num
                    # class_define["__line"][next_name] = x + 1
                    class_define["__line"][next_name] = i   # 结构体、数组的line仅有排序意义

                    sub_index = 0
                    next_x = x + 1

                    while sub_index != len(class_define[next_name]):
                        class_define[next_name][sub_index], next_x = parse_class(sheet, next_x, end_col,
                                                                                 struct_element_num)
                        sub_index = sub_index + 1

                    i = next_x

                else:  # 简单元素分列数组
                    class_define[next_name] = [next_lua_type] * num
                    class_define["__line"][next_name] = i   # 结构体、数组的line仅有排序意义
                    i = x + num

            else:  # 单列数组
                class_define[name] = lua_type + "[]"
                class_define["__line"][name] = i
                i = i + 1

        elif proto_type == "required_struct" or proto_type == "optional_struct":

            struct_element_num = int(lua_type)

            class_define[name], next_x = parse_class(
                sheet, i + 1, end_col, struct_element_num)
            class_define["__line"][name] = i    # 结构体、数组的line仅有排序意义

            i = next_x

        elif is_skip(proto_type):
            calc_invalid_num = calc_invalid_num + 1
            i = i + 1
        else:  # required,optional
            class_define[name] = lua_type
            class_define["__line"][name] = i

            i = i + 1

        if not is_skip(proto_type):
            solved_element = solved_element + 1

    return class_define, i


def gen_instance(sheet, class_define, id, current_indent, outfile):
    elements = sorted(class_define["__line"].items(), key=lambda x: x[1])

    if len(elements):
        print("generate_instance, first start at: row {}, column {}".format(
            id, elements[0][1]))

    for name, line in elements:
        define = class_define[name]

        xls_value = sheet.cell_value(id, line)

        if is_simple_type(define):
            print(current_indent + name + " = " +
                  process_value(define, xls_value) + ",", file=outfile)
        elif is_single_arr(define):  # 单列数组
            elem_type = define[:-2]

            if str(xls_value).endswith(";"):
                xls_value = xls_value[:-1]

            if str(xls_value) == "":
                print(current_indent + name + " = {},", file=outfile)
            else:
                xls_values = str(xls_value).split(";")
                ans = []
                for elem in xls_values:
                    ans.append(process_value(elem_type, elem))
                print(current_indent + name +
                      " = {" + ",".join(ans) + "},", file=outfile)
        elif type(define) == type({}):  # 结构体
            print(current_indent + name + " = {", file=outfile)
            gen_instance(sheet, define, id, current_indent + INDENT)
            print(current_indent + "},", file=outfile)
        elif type(define) == type([]):  # 简单元素分列数组或结构体数组
            if is_simple_type(define[0]):   # 简单元素分列数组
                num = len(define)
                if xls_value != "":
                    num = min(int(xls_value), num)
                    num = max(0, num)

                x = line + 1
                skip_num = 0
                ans = []

                while x - line - skip_num <= num:
                    proto_type = sheet.cell_value(0, x)
                    xls_value = sheet.cell_value(id, x)
                    if is_skip(proto_type):
                        skip_num = skip_num + 1
                    else:
                        ans.append(process_value(define[0], xls_value))
                    x = x + 1

                print(current_indent + name +
                      " = {" + ",".join(ans) + "},", file=outfile)

            else:   # 结构体数组
                num = len(define)
                if xls_value != "":
                    num = min(int(xls_value), num)
                    num = max(0, num)

                print(current_indent + name + " = {", file=outfile)
                for sub_define in define[:num]:
                    print(current_indent + INDENT + "{", file=outfile)
                    gen_instance(sheet, sub_define, id,
                                 current_indent + INDENT * 2, outfile)
                    print(current_indent + INDENT + "},", file=outfile)
                print(current_indent + "},", file=outfile)


solved_head = {}
solved_tail = {}
head = \
    '''------------------------------
---该文件由工具自动生成
---配置表转Lua Table
------------------------------
'''


def solve_sheet(sheet):
    print("generate_sheet, sheet name = " + sheet.name)
    output_filename = sheet.name.upper()
    output_filepath = p.join(OUTPUT_DIRECTORY, output_filename + ".lua")

    ncols = sheet.ncols
    endCol = ncols - 1

    class_define, _ = parse_class(sheet, 0, endCol)

    print(class_define)

    if output_filename not in solved_head:
        solved_head[output_filename] = True
        outfile = open(output_filepath, 'w', encoding='utf-8')

        print(head, file=outfile)
        print("---@type " + sheet.name + "[]", file=outfile)
        print("local " + sheet.name + "S = {", file=outfile)
    else:
        outfile = open(output_filepath, 'a', encoding='utf-8')

    nrows = sheet.nrows

    for i in range(5, nrows):
        print("    [" + str(i - 4) + "] = {", file=outfile)

        gen_instance(sheet, class_define, i, "        ", outfile)
        print("    },", file=outfile)
        print("", file=outfile)

    outfile.close()


def post_solve_sheet(sheet):
    output_filename = sheet.name.upper()
    output_filepath = p.join(OUTPUT_DIRECTORY, output_filename + ".lua")

    if output_filename not in solved_tail:
        solved_tail[output_filename] = True

        outfile = open(output_filepath, 'a', encoding='utf-8')
        print("}", file=outfile)
        print("", file=outfile)
        print("return " + sheet.name + "S", file=outfile)
        outfile.close()


def post_generate_file(xls_file):
    book = xlrd.open_workbook(xls_file)
    for sheet in book.sheets():
        if sheet.name.isupper() and "#" not in sheet.name:
            post_solve_sheet(sheet)


def post_generate_dir(xls_dir):
    filenames = os.listdir(xls_dir)
    for filename in filenames:
        if not filename.startswith("~$"):
            post_generate_file(p.join(xls_dir, filename))


def generate_file(xls_file):
    print("generate_flie, file path = " + xls_file)
    book = xlrd.open_workbook(xls_file)
    for sheet in book.sheets():
        if sheet.name.isupper() and "#" not in sheet.name:
            solve_sheet(sheet)


def generate_dir(xls_dir):
    print("generate_dir: " + xls_dir)
    filenames = os.listdir(xls_dir)
    for filename in filenames:
        if not filename.startswith("~$"):
            generate_file(p.join(xls_dir, filename))


def generate(argv1):
    if p.isfile(argv1):  # 参数为指定文件
        generate_file(argv1)
        post_generate_file(argv1)
    else:  # 参数为目录
        generate_dir(argv1)
        post_generate_dir(argv1)


def main():
    if len(sys.argv) != 3:
        print("python3 gen_luatable.py EXCEL_DIR OUTPUT_DIR")
        sys.exit(-1)

    global OUTPUT_DIRECTORY
    OUTPUT_DIRECTORY = p.abspath(sys.argv[2])

    if not p.isdir(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    generate(sys.argv[1])


if __name__ == '__main__':
    main()
