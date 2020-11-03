local DataConfigManager = require("DataConfigManager")

DataConfigManager:LoadBagItemConf()
local bagItem = DataConfigManager:GetBagItemConf(100001)

print(bagItem.id)
print(bagItem.description)
print(bagItem.visible_in_bag)
print(bagItem.pos[2].pos_y)
