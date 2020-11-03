
------------------------------
---该文件由工具自动生成
---DataConfigManager
------------------------------

---@class DataConfigManager
local DataConfigManager = {}

DataConfigManager.BinPath = "output/bin"
DataConfigManager.LuaPath = "output.lua"

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



function DataConfigManager:LoadBagItemConf()
    local file = io.open(string.format("%s/%s.bin", DataConfigManager.BinPath, "BAG_ITEM_CONF"), "rb")
    local buf = flatbuffers.binaryArray.New(file:read("*a"))
    file:close()

    self.BAG_ITEM_CONF_ARR = require(string.format("%s.Default.%s", DataConfigManager.LuaPath, "BAG_ITEM_CONF_ARR")).GetRootAsBAG_ITEM_CONF_ARR(buf, 0)
end



function DataConfigManager:GetBagItemConf(key)
    return FindCfgByKey(key, self.BAG_ITEM_CONF_ARR, "id")
end



return DataConfigManager

