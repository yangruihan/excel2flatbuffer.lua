#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import sys
import os

"""
```python
python3 gen_bin.py FBS_DIR JSON_DIR OUTPUT_DIR
```

根据 FBS 及 Json 生成对应的二进制数据文件
"""


def main():
    if len(sys.argv) != 4:
        print('python3 gen_bin.py FBS_DIR JSON_DIR OUTPUT_DIR')
        sys.exit(-1)

    output_dir = os.path.abspath(sys.argv[3])

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    fbs_dir = sys.argv[1]
    json_dir = sys.argv[2]

    filenames = os.listdir(fbs_dir)
    for filename in filenames:
        json_filename = filename.replace('.fbs', '.json')
        os.system(
            f'flatc -o {output_dir} -b {os.path.join(fbs_dir, filename)} {os.path.join(json_dir, json_filename)}')


if __name__ == "__main__":
    main()
