#!/usr/bin/env python3

nbt_all_types = ['TAG_Byte', 'TAG_Short', 'TAG_Int', 'TAG_Long', 'TAG_Float',
                 'TAG_Double', 'TAG_String', 'TAG_Byte_Array', 'TAG_List',
                 'TAG_Int_Array', 'TAG_Compound']


def pretty_format_nbt(nbt_data):
    short_names = {
        'TAG_Byte': 'B',
        'TAG_Short': 'S',
        'TAG_Int': 'I',
        'TAG_Long': 'L',
        'TAG_Float': 'F',
        'TAG_Double': 'D',
        'TAG_Byte_Array': '[B]',  # Array around byte symbol
        'TAG_String': 'txt',
        'TAG_List': '[ ]',  # Array
        'TAG_Compound': '{ }',  # Dict, object, whatever
        'TAG_Int_Array': '[I]'  # Array around int symbol
    }
    if nbt_data.type == "TAG_Compound":
        indent_level = 4
        out = ""
        for x in nbt_data.data:
            out += x + ": " + pretty_format_nbt(nbt_data.data[x])
        out = " " * indent_level + out.replace("\n",
                                               "\n" + (indent_level * " "))
        return short_names[
                   nbt_data.type] + "  " + nbt_data.description + "\n" + out
    elif nbt_data.type == "TAG_List":
        indent_level = 4
        out = ""
        for x in nbt_data.data:
            out += pretty_format_nbt(x)
        out = " " * indent_level + out.replace("\n",
                                               "\n" + (indent_level * " "))
        return short_names[
                   nbt_data.type] + "  " + nbt_data.description + "\n" + out
    else:
        return short_names[nbt_data.type] + "  " + nbt_data.description


class NBTTemplate(object):
    def __init__(self, data):
        if data['type'] in nbt_all_types:
            if data['type'] == "TAG_List":
                self.data = []
                for x in data['content']:
                    self.data.append(NBTTemplate(x))
            elif data['type'] == "TAG_Compound":
                self.data = {}
                for k in data['content']:
                    self.data[k] = NBTTemplate(data['content'][k])
            self.type = data['type']
            self.description = data['desc']
        else:
            raise TypeError("Invalid data type")

    def pretty_print(self):
        print(pretty_format_nbt(self))


class CraftingTableRecipe(object):
    def __init__(self, data):
        self.grid_size = data["grid_size"]
        self.recipe = []
        for x in data["recipe_rows"]:
            self.recipe.append([])
            for y in x:
                if y in data["recipe_components"] or y == " ":
                    self.recipe[-1].append(y)
                else:
                    raise ValueError("Letter " + repr(y) + " used in recipe, "
                                     "but undefined in recipe_components")
        self.recipe_components = data["recipe_components"]

    def str(self):
        pass


class SmeltingRecipe(object):
    def __init__(self, data):
        self.inp = data

    def str(self):
        return "Smelt " + self.inp


class BrewingRecipe(object):
    def __init__(self, data):
        self.base = data[0]
        self.modifier = data[1]

    def str(self):
        return "Brew " + self.modifier + " into " + self.base


class Recipe(object):
    def __init__(self, methods, *args):
        self.methods = []
        for i, s in enumerate(methods):
            if s == "crafting":
                recipe_type = CraftingTableRecipe
            elif s == "smelting":
                recipe_type = SmeltingRecipe
            elif s == "brewing":
                recipe_type = BrewingRecipe
            else:
                raise ValueError("Invalid crafting method: should be one of "
                                 "[crafting, smelting, brewing]")
            self.methods.append({'method': s, 'recipe': recipe_type(args[i])})

    def str(self):
        out = "Recipes:\n"
        for x in self.methods:
            out += x['method'].capitalize() + ":\n"
            out += x['recipe'].str() + "\n"
        return out


class Representable(object):
    allowed_keys = dict()

    def __init__(self, data):
        filtered_dict = {k: self.allowed_keys[k](v) for k, v in data.items()
                         if k in self.allowed_keys}
        self.__dict__.update(filtered_dict)


class Item(Representable):
    allowed_keys = {
        'mc_id': str,
        'mc_name': str,
        'english_name': str,
        'desc': str,
        'recipe': Recipe,
        'stack_size': int,
        'nbt_data': NBTTemplate,
    }