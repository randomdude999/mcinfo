
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
        return "Brew {} into {}".format(self.modifier, self.base)


class TradingRecipe:
    def __init__(self, data):
        self.price_min = data['price_min']
        self.price_max = data['price_max']
        self.single_price = (self.price_min == 1 and self.price_max == 1)
        try:
            self.secondary_item = data['secondary_item']
            self.secondary_count = data['secondary_count']
            self.has_secondary_item = True
        except AttributeError:
            self.secondary_item = None
            self.secondary_count = 0
            self.has_secondary_item = False
        self.out_count_min = data['out_count_min']
        self.out_count_max = data['out_count_max']
        self.single_out = (self.out_count_min == 1 and self.out_count_max == 1)
        self.career = data['career']

    def __str__(self):
        out = "Can be bought from {} for ".format(self.career.capitalize())
        if self.single_price:
            out += "1 Emerald"
        else:
            out += "{}-{} Emeralds".format(self.price_min, self.price_max)
        if self.has_secondary_item:
            out += " and {} {}.".format(self.secondary_item,
                                        self.secondary_count)
        else:
            out += "."
        if not self.single_out:
            out += " Yields {}-{}.".format(self.out_count_min,
                                           self.out_count_max)
        return out


class ChestLootRecipe:
    def __init__(self, data):
        self.location = data["location"]
        self.chance = data["chance"]

    def __str__(self):
        return "Can be found from {} with {.1f}% chance.".format(
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
                out = "{} drops 1 on death ".format(self.source)
            else:
                out = "{} drops {}-{} on death ".format(
                    self.source, self.min_count, self.max_count)
        else:
            out = "{} has {.1f}% chance to drop on death ".format(
                self.source, self.drop_chance)
        if self.extra_conditions:
            out += self.extra_conditions

type_map = {
    "smelting": SmeltingRecipe,
    "brewing": BrewingRecipe,
    "trading": TradingRecipe,
    "chest_loot": ChestLootRecipe,
    "mob_loot": MobDropRecipe
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
            out += "{} recipe: \n{}\n".format(x.method.capitalize(), x.recipe)
        return out
