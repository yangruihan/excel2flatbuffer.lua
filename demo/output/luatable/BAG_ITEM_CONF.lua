------------------------------
---该文件由工具自动生成
---配置表转Lua Table
------------------------------

---@type BAG_ITEM_CONF[]
local BAG_ITEM_CONFS = {
    [1] = {
        id = 100001,
        name = "测试道具1",
        description = "这是一个测试道具",
        icon = "res/test1.png",
        visible_in_bag = 1,
        item_quality = 0,
        pos = {
            {
                pos_x = 1,
                pos_y = 2,
                pos_z = 3,
            },
            {
                pos_x = 4,
                pos_y = 5,
                pos_z = 6,
            },
        },
    },

    [2] = {
        id = 100002,
        name = "测试道具2",
        description = "这是一个测试道具",
        icon = "res/test2.png",
        visible_in_bag = 0,
        item_quality = 1,
        pos = {
            {
                pos_x = 7,
                pos_y = 8,
                pos_z = 9,
            },
            {
                pos_x = 10,
                pos_y = 11,
                pos_z = 12,
            },
        },
    },

}

return BAG_ITEM_CONFS
