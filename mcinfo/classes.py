#!/usr/bin/env python3

nbt_int_types = ['TAG_Byte', 'TAG_Short', 'TAG_Int', 'TAG_Long']
nbt_float_types = ['TAG_Float', 'TAG_Double']
nbt_str_types = ['TAG_String']
nbt_list_types = ['TAG_Byte_Array', 'TAG_List', 'TAG_Int_Array']
nbt_dict_types = ['TAG_Compound']
nbt_all_types = nbt_int_types + nbt_float_types + nbt_str_types + \
                nbt_list_types + nbt_dict_types

def prettyFormatNBT(nbt_data):
    shortNames = {
            'TAG_Byte': '8b', # Number of bits
            'TAG_Short': '16b',
            'TAG_Int': '32b',
            'TAG_Long': '64b',
            'TAG_Float': '32f', # Because f obviously means float
            'TAG_Double': '64f',
            'TAG_Byte_Array': '[B]', # Array around byte symbol
            'TAG_String': 'S',
            'TAG_List': '[ ]', # Array
            'TAG_Compound': '{ }', # Dict, object, whatever
            'TAG_Int_Array': '[I]' # Array around int symbol
    }
    if nbt_data.type == "TAG_Compound":
        identLevel = 4
        out = ""
        for x in nbt_data.data:
            out += x + ": " + prettyFormatNBT(nbt_data.data[x])
        out = " " * identLevel + out.replace("\n", "\n" + (identLevel * " ") )
        return shortNames[nbt_data.type] + "  " + nbt_data.description + "\n" + out
    elif nbt_data.type == "TAG_List":
        identLevel = 4
        out = ""
        for x in nbt_data.data:
            out += prettyFormatNBT(x)
        out = " " * identLevel + out.replace("\n", "\n" + (identLevel * " ") )
        return shortNames[nbt_data.type] + "  " + nbt_data.description + "\n" + out
    else:
        return shortNames[nbt_data.type] + "  " + nbt_data.description


class NBTTemplate(object):
    def __init__(self, data):
        if data['type'] in nbt_all_types:
            if data['type'] in nbt_list_types:
                self.data = []
                for x in data['content']:
                    self.data.append(NBTTemplate(x))
            elif data['type'] in nbt_dict_types:
                self.data = {}
                for k in data['content']:
                    self.data[k] = NBTTemplate(data['content'][k])
            self.type = data['type']
            self.description = data['desc']
        else:
            raise TypeError("Invalid data type")
    
    def prettyPrint(self):
        print prettyFormatNBT(self)

class BaseItem(object):
    def __init__(self, mc_id, mc_name, english_name, nbt_data):
        self.mc_id = mc_id
        self.mc_name = mc_name
        self.english_name = english_name

class Item(BaseItem):
    pass

class Tool(Item):
    pass

class Block(BaseItem):
    pass

class Entity(object):
    pass

class Mob(Entity):
    pass

class Projectile(Entity):
    pass

class Vehicle(Entity):
    pass

class BlockEntity(object):
    pass

class PotionEffect(object):
    pass

class Enchantment(object):
    pass

