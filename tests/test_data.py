from __future__ import unicode_literals
import unittest
import pkg_resources
import json

from mcinfo import nbt
from mcinfo import normal_info
from mcinfo import recipes


# This returns absolute paths relative to the package specified.
def pkg_resources_get_all_files(package, start_path, cur_path=None):
    if cur_path is None:
        cur_path = start_path
    out = []
    dir_contents = pkg_resources.resource_listdir(package, cur_path)
    for dir_item in dir_contents:
        abs_path = (cur_path if cur_path.endswith('/') else cur_path +
                    '/') + dir_item
        if pkg_resources.resource_isdir(package, abs_path):
            out.extend(pkg_resources_get_all_files(package, start_path,
                                                   abs_path))
        else:
            out.append(abs_path)
    return out


class TestData(unittest.TestCase):

    def test_nbt_data(self):
        files = pkg_resources_get_all_files("mcinfo", "data/nbt")
        success = True
        out = []
        for f_name in files:
            s = pkg_resources.resource_string("mcinfo", f_name)
            if isinstance(s, bytes):
                s = s.decode()
            try:
                data = json.loads(s)
                nbt.pretty_format_nbt(nbt.NBTTemplate(data))
            except Exception as e:
                out.append("%s in data file %s: %s" % (type(e).__name__,
                                                       f_name, str(e)))
                success = False
        out = "\n" + "\n".join(out)
        self.assertTrue(success, out)

    def testNormalData(self):
        files = pkg_resources_get_all_files("mcinfo", "data")
        success = True
        out = []
        for f_name in files:
            if f_name.startswith("data/nbt") or \
                    f_name.startswith("data/recipes"):
                continue
            s = pkg_resources.resource_string("mcinfo", f_name)
            if isinstance(s, bytes):
                s = s.decode()
            try:
                data = json.loads(s)
                str(normal_info.format_data(data))
            except Exception as e:
                out.append("%s in data file %s: %s" % (type(e).__name__,
                                                       f_name, str(e)))
                success = False
        out = "\n" + "\n".join(out)
        self.assertTrue(success, out)

    def test_recipes(self):
        files = pkg_resources_get_all_files("mcinfo", "data/recipes")
        success = True
        out = []
        for f_name in files:
            s = pkg_resources.resource_string("mcinfo", f_name)
            if isinstance(s, bytes):
                s = s.decode()
            try:
                data = json.loads(s)
                str(recipes.RecipeCollection(data))
            except Exception as e:
                out.append("%s in data file %s: %s" % (type(e).__name__,
                                                       f_name, str(e)))
                success = False
        out = "\n" + "\n".join(out)
        self.assertTrue(success, out)
