import pickle
import Item, World


class SaveClass:
    def __init__(self, world_obj):
        self.world_obj = world_obj
        self.save_file_name = "save"

    def saving_date(self):
        output_obj = SaveObj(self.world_obj)
        with open(self.save_file_name, "wb") as file:
            pickle.dump(output_obj, file)

    def loading(self):
        try:
            file = open(self.save_file_name, "rb")
        except:
            return False, None
        load_obj = pickle.load(file)
        print("Load:", vars(load_obj))
        file.close()
        self.world_obj.Char_obj.char_name = load_obj.char_name
        self.world_obj.Char_obj.job_idx = load_obj.job_idx
        self.world_obj.Char_obj.job_name = load_obj.job_name
        self.world_obj.Char_obj.job_type = load_obj.job_type
        self.world_obj.Char_obj.base_level = load_obj.base_level
        self.world_obj.Char_obj.job_level = load_obj.job_level
        self.world_obj.Char_obj.zeny = load_obj.zeny
        self.world_obj.Char_obj.base_exp = load_obj.base_exp
        self.world_obj.Char_obj.job_exp = load_obj.job_exp
        self.world_obj.Char_obj.define_base_exp_type()
        self.world_obj.Char_obj.define_job_exp_type()
        self.world_obj.Char_obj.equipment.reset_equip()                                     # 重置清空裝備欄
        for idx, item_idx in enumerate(load_obj.equipment):
            print("idx = ", idx, "item_idx = ", item_idx)
            if item_idx is not None:
                self.world_obj.Char_obj.equipment.equip(Item.ItemObj(1, item_idx, self.world_obj.Char_obj, 1))
            else:
                self.world_obj.Char_obj.equipment.equip_list[idx] = item_idx                # None
        self.world_obj.Char_obj.equipment.reset_equip_bonus()
        self.world_obj.Char_obj.equipment.calculate_bonus()
        self.world_obj.Char_obj.ability = load_obj.ability
        self.world_obj.Char_obj.item = Item.ItemList(self.world_obj.Char_obj.equipment)     # 重置清空物品欄
        for item_type, idx, amount in load_obj.item:
            self.world_obj.Char_obj.item.add_item(Item.ItemObj(item_type, idx, self.world_obj.Char_obj, amount))
        self.world_obj.Char_obj.hp = load_obj.hp
        self.world_obj.Char_obj.sp = load_obj.sp
        self.world_obj.Char_obj.sit_img_path = load_obj.sit_img_path
        self.world_obj.Char_obj.stand_img_path = load_obj.stand_img_path
        self.world_obj.Char_obj.standby_img_path = load_obj.standby_img_path
        self.world_obj.Char_obj.attack_img_path = load_obj.attack_img_path
        self.world_obj.Char_obj.dead_img_path = load_obj.dead_img_path
        self.world_obj.Char_obj.load_img()
        self.world_obj.Char_obj.attribute.transform(self.world_obj.Char_obj)
        self.world_obj.auto_health = World.AutoHealthByMedicine(self.world_obj.Char_obj, load_obj.item_order_in_list,
                                                                self.world_obj.Char_obj.item, 0.5)
        return True, load_obj.current_pos


class SaveObj:
    def __init__(self, world_obj):
        self.current_pos = world_obj.current_pos
        self.item_order_in_list = world_obj.auto_health.item_order_in_list
        self.char_name = world_obj.Char_obj.char_name
        self.job_idx = world_obj.Char_obj.job_idx
        self.job_name = world_obj.Char_obj.job_name
        self.job_type = world_obj.Char_obj.job_type
        self.base_level = world_obj.Char_obj.base_level
        self.job_level = world_obj.Char_obj.job_level
        self.zeny = world_obj.Char_obj.zeny
        self.base_exp = world_obj.Char_obj.base_exp
        self.job_exp = world_obj.Char_obj.job_exp
        self.equipment = world_obj.Char_obj.equipment.get_idx()
        self.ability = world_obj.Char_obj.ability
        # [[item_type, item_idx, amount], [item_type, item_idx, amount]...]
        self.item = [[obj.item_type, obj.item_idx, obj.amount] for obj in world_obj.Char_obj.item.usable_item_list] + \
                    [[obj.item_type, obj.item_idx, obj.amount] for obj in world_obj.Char_obj.item.equipment_list] + \
                    [[obj.item_type, obj.item_idx, obj.amount] for obj in world_obj.Char_obj.item.collection_list]
        self.hp = world_obj.Char_obj.hp
        self.sp = world_obj.Char_obj.sp
        self.sit_img_path = world_obj.Char_obj.sit_img_path
        self.stand_img_path = world_obj.Char_obj.stand_img_path
        self.standby_img_path = world_obj.Char_obj.standby_img_path
        self.attack_img_path = world_obj.Char_obj.attack_img_path
        self.dead_img_path = world_obj.Char_obj.dead_img_path
        print("Save:", vars(self))    # show all member variables


