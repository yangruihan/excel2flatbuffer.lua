-- automatically generated by the FlatBuffers compiler, do not modify

-- namespace: Default

local flatbuffers = require('flatbuffers')

local BAG_ITEM_CONF_ARR = {} -- the module
local BAG_ITEM_CONF_ARR_mt = {} -- the class metatable

function BAG_ITEM_CONF_ARR.New()
    local o = {}
    setmetatable(o, {__index = function(t, key)
    local f = rawget(BAG_ITEM_CONF_ARR_mt, key)
    if key == 'Init' then
        return f
    end
    return f(t)
end})    return o
end
function BAG_ITEM_CONF_ARR.GetRootAsBAG_ITEM_CONF_ARR(buf, offset)
    local n = flatbuffers.N.UOffsetT:Unpack(buf, offset)
    local o = BAG_ITEM_CONF_ARR.New()
    o:Init(buf, n + offset)
    return o
end
function BAG_ITEM_CONF_ARR_mt:Init(buf, pos)
    self.view = flatbuffers.view.New(buf, pos)
end
function BAG_ITEM_CONF_ARR_mt:data()
local ret = rawget(self, "_fb_data_arr")
if ret then
    return ret
end
ret = setmetatable({}, {
__len = function(t)
    local l = rawget(t, "_fb_data_len")
    if l then return l end
    local f = rawget(BAG_ITEM_CONF_ARR_mt, "dataLength")
    l = f(t)
    rawset(t, "_fb_data_len", l)
    return l
end,

__index = function(t, j)
    if type(j) == 'number' then
    local o = self.view:Offset(4)
    if o ~= 0 then
        local x = self.view:Vector(o)
        x = x + ((j-1) * 4)
        x = self.view:Indirect(x)
        local obj = require('Default.BAG_ITEM_CONF').New()
        obj:Init(self.view.bytes, x)
        return obj
    end
    else
        return rawget(self, j)
    end
end,

__ipairs = function(t)
    local idx = 0
    local l = #t
    return function()
        idx = idx + 1
        if idx <= l then
            return idx, t[idx]
        end
    end
end
}
)
rawset(self, "_fb_data_arr", ret)
return ret
end
function BAG_ITEM_CONF_ARR_mt:dataLength()
    local o = self.view:Offset(4)
    if o ~= 0 then
        return self.view:VectorLen(o)
    end
    return 0
end
function BAG_ITEM_CONF_ARR.Start(builder) builder:StartObject(1) end
function BAG_ITEM_CONF_ARR.AddData(builder, data) builder:PrependUOffsetTRelativeSlot(0, data, 0) end
function BAG_ITEM_CONF_ARR.StartDataVector(builder, numElems) return builder:StartVector(4, numElems, 4) end
function BAG_ITEM_CONF_ARR.End(builder) return builder:EndObject() end

return BAG_ITEM_CONF_ARR -- return the module