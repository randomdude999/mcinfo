import unittest

from mcinfo import normal_info


class TestNormalInfo(unittest.TestCase):

    def test_format_data(self):
        inp = {'hello': "world", 'test_data_1': "A " + "really " * 30 +
                                                "long paragraph"}
        out = "Hello: world\nTest_data_1: A really really really really " \
              "really really really really really\n  really really really " \
              "really really really really really really really really\n  " \
              "really really really really really really really really " \
              "really really long\n  paragraph"
        self.assertEqual(normal_info.format_data(inp), out)

    def test_handle_request(self):
        out = normal_info.handle_request('test')
        expected_out = "Warning: This is test data! It is not at all useful " \
                       "for you.\nRecipes:\n"
        self.assertEqual(out, expected_out)
