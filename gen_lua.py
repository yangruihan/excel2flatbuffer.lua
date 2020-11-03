#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import sys
import os


"""
```python
python3 gen_lua.py FBS_DIR OUTPUT_DIR
```

根据 FBS 生成对应的辅助 Lua 脚本
"""


def main():
    if len(sys.argv) != 3:
        print('python3 gen_lua.py FBS_DIR OUTPUT_DIR')
        sys.exit(-1)

    output_dir = os.path.abspath(sys.argv[2])

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    fbs_dir = sys.argv[1]

    filenames = os.listdir(fbs_dir)
    for filename in filenames:
        os.system(
            f'flatc -o {output_dir} --lua {os.path.join(fbs_dir, filename)}')


if __name__ == "__main__":
    main()
