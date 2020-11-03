cd ..

export PATH="./demo:$PATH"

# 根据 excel 生成 fbs
python3 gen_fbs.py demo/config demo/output/fbs

# 根据 excel 生成 luatable
python3 gen_luatable.py demo/config demo/output/luatable

# 根据 lua 生成 json
export LUA_PATH="demo/output/luatable/?.lua;./?.lua;"
python3 gen_json.py demo/output/luatable demo/output/json

# 根据 json 生成 bin
python3 gen_bin.py demo/output/fbs demo/output/json demo/output/bin

# 根据 fbs 生成对应的 lua 脚本
python3 gen_lua.py demo/output/fbs demo/output/lua

# 生成访问辅助 lua
python3 gen_luautils.py demo/config output/bin Default output.lua demo/DataConfigManager.lua

cd -
