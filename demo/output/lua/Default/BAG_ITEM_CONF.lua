-- automatically generated by the FlatBuffers compiler, do not modify

-- namespace: Default

local flatbuffers = require('flatbuffers')

local BAG_ITEM_CONF = {} -- the module
local BAG_ITEM_CONF_mt = {} -- the class metatable

function BAG_ITEM_CONF.New()
    local o = {}
    setmetatable(o, {__index = function(t, key)
    local f = rawget(BAG_ITEM_CONF_mt, key)
    if key == 'Init' then
        return f
    end
    return f(t)
end})    return o
end
function BAG_ITEM_CONF.GetRootAsBAG_ITEM_CONF(buf, offset)
    local n = flatbuffers.N.UOffsetT:Unpack(buf, offset)
    local o = BAG_ITEM_CONF.New()
    o:Init(buf, n + offset)
    return o
end
function BAG_ITEM_CONF_mt:Init(buf, pos)
    self.view = flatbuffers.view.New(buf, pos)
end
function BAG_ITEM_CONF_mt:id()
    local o = self.view:Offset(4)
    if o ~= 0 then
        return self.view:Get(flatbuffers.N.Int32, o + self.view.pos)
    end
    return 0
end
function BAG_ITEM_CONF_mt:name()
    local o = self.view:Offset(6)
    if o ~= 0 then
        return self.view:String(o + self.view.pos)
    end
end
function BAG_ITEM_CONF_mt:description()
    local o = self.view:Offset(8)
    if o ~= 0 then
        return self.view:String(o + self.view.pos)
    end
end
function BAG_ITEM_CONF_mt:icon()
    local o = self.view:Offset(10)
    if o ~= 0 then
        return self.view:String(o + self.view.pos)
    end
end
function BAG_ITEM_CONF_mt:visible_in_bag()
    local o = self.view:Offset(12)
    if o ~= 0 then
        return self.view:Get(flatbuffers.N.Uint32, o + self.view.pos)
    end
    return 0
end
function BAG_ITEM_CONF_mt:item_quality()
    local o = self.view:Offset(14)
    if o ~= 0 then
        return self.view:Get(flatbuffers.N.Uint32, o + self.view.pos)
    end
    return 0
end
function BAG_ITEM_CONF_mt:pos()
local ret = rawget(self, "_fb_pos_arr")
if ret then
    return ret
end
ret = setmetatable({}, {
__len = function(t)
    local l = rawget(t, "_fb_pos_len")
    if l then return l end
    local f = rawget(BAG_ITEM_CONF_mt, "posLength")
    l = f(t)
    rawset(t, "_fb_pos_len", l)
    return l
end,

__index = function(t, j)
    if type(j) == 'number' then
    local o = self.view:Offset(16)
    if o ~= 0 then
        local x = self.view:Vector(o)
        x = x + ((j-1) * 4)
        x = self.view:Indirect(x)
        local obj = require('Default.pos_struct_type').New()
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
rawset(self, "_fb_pos_arr", ret)
return ret
end
function BAG_ITEM_CONF_mt:posLength()
    local o = self.view:Offset(16)
    if o ~= 0 then
        return self.view:VectorLen(o)
    end
    return 0
end
function BAG_ITEM_CONF.Start(builder) builder:StartObject(7) end
function BAG_ITEM_CONF.AddId(builder, id) builder:PrependInt32Slot(0, id, 0) end
function BAG_ITEM_CONF.AddName(builder, name) builder:PrependUOffsetTRelativeSlot(1, name, 0) end
function BAG_ITEM_CONF.AddDescription(builder, description) builder:PrependUOffsetTRelativeSlot(2, description, 0) end
function BAG_ITEM_CONF.AddIcon(builder, icon) builder:PrependUOffsetTRelativeSlot(3, icon, 0) end
function BAG_ITEM_CONF.AddVisibleInBag(builder, visibleInBag) builder:PrependUint32Slot(4, visibleInBag, 0) end
function BAG_ITEM_CONF.AddItemQuality(builder, itemQuality) builder:PrependUint32Slot(5, itemQuality, 0) end
function BAG_ITEM_CONF.AddPos(builder, pos) builder:PrependUOffsetTRelativeSlot(6, pos, 0) end
function BAG_ITEM_CONF.StartPosVector(builder, numElems) return builder:StartVector(4, numElems, 4) end
function BAG_ITEM_CONF.End(builder) return builder:EndObject() end

return BAG_ITEM_CONF -- return the module