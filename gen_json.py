#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import sys
import os


"""
依赖 Lua 解释器

```python
python3 gen_json.py LUATABLE_DIR OUTPUT_DIR
```

根据 Lua 表生成 Json 文件
"""


def main():
    if len(sys.argv) != 3:
        print('python3 gen_json.py LUATABLE_DIR OUTPUT_DIR')
        sys.exit(-1)

    output_dir = os.path.abspath(sys.argv[2])

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    config_dir = sys.argv[1]

    filenames = os.listdir(config_dir)
    for filename in filenames:
        if filename.endswith('.lua'):
            print(f'start handle {os.path.join(config_dir, filename)} ...')
            os.system(
                f'lua luatable2json.lua {os.path.join(config_dir, filename)} {output_dir}/{filename.replace(".lua", ".json")}')
            print(f'end handle {os.path.join(config_dir, filename)}\n')


if __name__ == "__main__":
    main()
