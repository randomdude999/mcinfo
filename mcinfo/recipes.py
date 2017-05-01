from __future__ import unicode_literals


class SmeltingRecipe:
    def __init__(self, data):
        self.input = data["input"]

    def __str__(self):
        return "Smelt {}".format(self.input)


class BrewingRecipe:
    def __init__(self, data):
        self.base = data["base"]
        self.modifier = data["modifier"]

    def __str__(self):
        return "Brew {0} into {1}".format(self.modifier, self.base)


class TradingRecipe:
    def __init__(self, data):
        self.price_min = data["price_min"]
        self.price_max = data["price_max"]
        self.single_price = (self.price_min == 1 and self.price_max == 1)
        try:
            self.secondary_item = data["secondary_item"]
            self.secondary_count = data["secondary_count"]
            self.has_secondary_item = True
        except KeyError:
            self.secondary_item = None
            self.secondary_count = 0
            self.has_secondary_item = False
        self.out_count_min = data["out_count_min"]
        self.out_count_max = data["out_count_max"]
        self.single_out = (self.out_count_min == 1 and self.out_count_max == 1)
        self.career = data["career"]

    def __str__(self):
        out = "Can be bought from {0} for ".format(self.career.capitalize())
        if self.single_price:
            out += "1 Emerald"
        else:
            out += "{0}-{1} Emeralds".format(self.price_min, self.price_max)
        if self.has_secondary_item:
            out += " and {0} {1}.".format(self.secondary_count,
                                          self.secondary_item)
        else:
            out += "."
        if not self.single_out:
            out += " Yields {0}-{1}.".format(self.out_count_min,
                                             self.out_count_max)
        return out


class ChestLootRecipe:
    def __init__(self, data):
        self.location = data["location"]
        self.chance = data["chance"]

    def __str__(self):
        return "Can be found from {0} with {1}% chance.".format(
            self.location, self.chance)


class MobDropRecipe:
    def __init__(self, data):
        self.drop_type = data["drop_type"]
        self.source = data["source"]
        if self.drop_type == "common":
            self.min_count = data["min_count"]
            self.max_count = data["max_count"]
            self.drops_single = (self.min_count == 1 and self.max_count == 1)
        elif self.drop_type == "rare":
            self.drop_chance = data["drop_chance"]
        if "extra_conditions" in data:
            self.extra_conditions = data["extra_conditions"]
        else:
            self.extra_conditions = ""

    def __str__(self):
        if self.drop_type == "common":
            if self.drops_single:
                out = "{0} drops 1 on death".format(self.source)
            else:
                out = "{0} drops {1}-{2} on death".format(
                    self.source, self.min_count, self.max_count)
        else:
            out = "{0} has {1}% chance to drop on death".format(
                self.source, self.drop_chance)
        if self.extra_conditions:
            out += ' ' + self.extra_conditions
        out += '.'
        return out


class CraftingRecipe:
    def __init__(self, data):
        if data["is_shaped"]:
            self.item_map = data["item_map"]
            self.grid = data["grid"]
            self.grid_size = len(self.grid)
        else:
            self.items = data["items"]
        self.is_shaped = data["is_shaped"]

    def pretty_print_crafting(self):
        out = ("+---" * self.grid_size) + "+\n"
        for line in self.grid:
            out += "|"
            for col in line:
                out += " {0} |".format(" " if col == "" else col)
            out += "\n" + ("+---" * self.grid_size) + "+\n"
        return out

    def __str__(self):
        if self.is_shaped:
            out = self.pretty_print_crafting()
            for k, v in self.item_map.items():
                out += "{0}: {1}\n".format(k, v)
        else:
            out = "Shapeless"
            for x in self.items:
                out += "\n* " + x
        return out

type_map = {
    "smelting": SmeltingRecipe,
    "brewing": BrewingRecipe,
    "trading": TradingRecipe,
    "chest_loot": ChestLootRecipe,
    "mob_loot": MobDropRecipe,
    "crafting": CraftingRecipe
}


class Recipe:
    def __init__(self, data):
        if data["type"] not in type_map:
            raise ValueError("No such crafting method")
        self.method = data["type"]
        self.recipe = type_map[self.method](data)

    def __str__(self):
        return str(self.recipe)


class RecipeCollection:
    def __init__(self, data):
        self.recipes = []
        for x in data:
            self.recipes.append(Recipe(x))

    def __str__(self):
        out = ""
        for x in self.recipes:
            out += "{0} recipe: \n{1}\n".format(x.method.capitalize(),
                                                x.recipe)
        return out
