from __future__ import unicode_literals
import unittest

from mcinfo import recipes


class TestRecipes(unittest.TestCase):

    def test_smelting_recipe(self):
        data = {'input': "test"}
        expected_out = "Smelt test"
        self.assertEqual(str(recipes.SmeltingRecipe(data)), expected_out)

    def test_brewing_recipe(self):
        data = {'base': 'test1', 'modifier': 'test2'}
        expected_out = "Brew test2 into test1"
        self.assertEqual(str(recipes.BrewingRecipe(data)), expected_out)

    def test_trading_multito1(self):
        data = {'price_min': 3, 'price_max': 5, 'out_count_min': 1,
                'out_count_max': 1, 'career': 'test1'}
        expected_out = "Can be bought from Test1 for 3-5 Emeralds."
        self.assertEqual(str(recipes.TradingRecipe(data)), expected_out)

    def test_trading_1tomulti(self):
        data = {'price_min': 1, 'price_max': 1, 'out_count_min': 5,
                'out_count_max': 10, 'career': 'test1'}
        expected_out = "Can be bought from Test1 for 1 Emerald. Yields 5-10."
        self.assertEqual(str(recipes.TradingRecipe(data)), expected_out)

    def test_trading_1to1(self):
        data = {'price_min': 1, 'price_max': 1, 'out_count_min': 1,
                'out_count_max': 1, 'career': 'test1'}
        expected_out = "Can be bought from Test1 for 1 Emerald."
        self.assertEqual(str(recipes.TradingRecipe(data)), expected_out)

    def test_trading_2inputs(self):
        data = {'price_min': 10, 'price_max': 15, 'out_count_min': 1,
                'out_count_max': 1, 'secondary_item': 'test2',
                'secondary_count': 1, 'career': 'test1'}
        expected_out = "Can be bought from Test1 for 10-15 Emeralds and 1 " \
                       "test2."
        self.assertEqual(str(recipes.TradingRecipe(data)), expected_out)

    def test_chest_loot_recipe(self):
        data = {'location': "test1", 'chance': 50}
        expected_out = "Can be found from test1 with 50% chance."
        self.assertEqual(str(recipes.ChestLootRecipe(data)), expected_out)

    def test_mob_drop_common(self):
        data = {'drop_type': "common", 'source': 'test1', 'min_count': 0,
                'max_count': 2}
        expected_out = "test1 drops 0-2 on death."
        self.assertEqual(str(recipes.MobDropRecipe(data)), expected_out)

    def test_mob_drop_rare(self):
        data = {'drop_type': "rare", 'source': 'test1', 'drop_chance': 50}
        expected_out = "test1 has 50% chance to drop on death."
        self.assertEqual(str(recipes.MobDropRecipe(data)), expected_out)

    def test_mob_drop_extra_conditions(self):
        data = {'drop_type': "rare", 'source': 'test1', 'drop_chance': 50,
                'extra_conditions': 'if killed by player'}
        expected_out = "test1 has 50% chance to drop on death if killed " \
                       "by player."
        self.assertEqual(str(recipes.MobDropRecipe(data)), expected_out)

    def test_mob_drop_single(self):
        data = {'drop_type': "common", 'source': 'test1', 'min_count': 1,
                'max_count': 1}
        expected_out = "test1 drops 1 on death."
        self.assertEqual(str(recipes.MobDropRecipe(data)), expected_out)

    def test_crafting_recipe_shapeless(self):
        data = {'is_shaped': False, 'items': ['test1', 'test2', 'test3']}
        expected_out = "Shapeless\n* test1\n* test2\n* test3"
        self.assertEqual(str(recipes.CraftingRecipe(data)), expected_out)

    def test_crafting_recipe_shaped(self):
        data = {'is_shaped': True, 'item_map': {'t': 'test1'}, 'grid': [[
            't', 't', 't'], ['t', 't', 't'], ['t', 't', 't']]}
        expected_out = "+---+---+---+\n" \
                       "| t | t | t |\n" \
                       "+---+---+---+\n" \
                       "| t | t | t |\n" \
                       "+---+---+---+\n" \
                       "| t | t | t |\n" \
                       "+---+---+---+\n" \
                       "t: test1\n"
        self.assertEqual(str(recipes.CraftingRecipe(data)), expected_out)

    def test_recipe(self):
        self.assertRaises(ValueError, recipes.Recipe, {'type': "nothing"})
        recipe = recipes.Recipe({'type': 'smelting', 'input': 'test1'})
        self.assertEqual(recipe.method, 'smelting')
        self.assertEqual(str(recipe), "Smelt test1")

    def test_recipe_collection(self):
        data = [{'type': 'smelting', 'input': 'test1'}, {'type': 'smelting',
                                                         'input': "test2"}]
        expected_out = "Smelting recipe: \nSmelt test1\nSmelting recipe: " \
                       "\nSmelt test2\n"
        self.assertEqual(str(recipes.RecipeCollection(data)), expected_out)
