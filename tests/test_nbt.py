import unittest

from mcinfo import nbt

testData = {
    'type': "TAG_Compound",
    'includes': ['3', 'other', 'things'],
    'desc': "example nbt structure",
    'content': {
        'a_string': {
            'type': "TAG_String",
            'desc': "A string! what did you expect, the spanish inquisition?"
        },
        'a_byte': {
            'type': "TAG_Byte",
            'desc': "A byte. This one has 256 possible values."
        },
        'list': {
            'type': "TAG_List",
            'desc': 'example list',
            'content': {
                'type': 'TAG_String',
                'desc': 'the string.'
            }
        }
    }
}

expectedFormatting = '{ }  example nbt structure\n    [All tags from 3]\n  ' \
                       '  [All tags from other]\n    [All tags from ' \
                       'things]\n    a_byte: B  A byte. This one has 256 ' \
                       'possible values.\n    a_string: txt  A string! what ' \
                       'did you expect, the spanish inquisition?\n    list: ' \
                       '[ ]  example list\n        txt  the string.'


class TestNBT(unittest.TestCase):

    def test_formatting(self):
        nbt_a = nbt.NBTTemplate(testData)
        self.assertEqual(nbt.pretty_format_nbt(nbt_a), expectedFormatting)

    def test_invalid_types(self):
        with self.assertRaises(TypeError):
            nbt.NBTTemplate({'type': "invalid", 'desc': "something"})
        with self.assertRaises(ValueError):
            nbt.NBTTemplate({})  # No type or anything
        with self.assertRaises(ValueError):
            nbt.NBTTemplate({'type': "TAG_List"})  # No content

    def test_no_desc(self):
        a = nbt.NBTTemplate({'type': "TAG_String"})  # No desc!
        b = nbt.NBTTemplate({'type': "TAG_String", 'desc': ""})
        self.assertEqual(a, b)

    def test_no_includes(self):
        a = nbt.NBTTemplate({'type': "TAG_Compound", 'desc': '', "includes":
                            [], "content": {}})
        b = nbt.NBTTemplate({'type': "TAG_Compound", 'desc': '', "content":
                            {}})  # no includes
        self.assertEqual(a, b)

    def test_equality(self):
        nbt_a = {
            'type': "TAG_Compound",
            'content': {
                'hello': {'type': "TAG_String"},
                'test': {'type': "TAG_Int"}
            }
        }
        nbt_b = {
            'type': "TAG_Compound",
            'content': {
                'test': {'type': "TAG_String"}
            }
        }
        nbt_c = {
            'type': "TAG_Compound",
            'content': {
                'test': {'type': "TAG_Int"}
            }
        }
        a = nbt.NBTTemplate(nbt_a)
        b = nbt.NBTTemplate(nbt_b)
        c = nbt.NBTTemplate(nbt_c)
        self.assertNotEqual(a, b)
        self.assertNotEqual(b, c)

    def test_list_equality(self):
        nbt_a = {
            'type': "TAG_List",
            'content': {
                'type': "TAG_String"
            }
        }
        nbt_b = {
            'type': "TAG_List",
            'content': {
                'type': "TAG_Int"
            }
        }
        a = nbt.NBTTemplate(nbt_a)
        b = nbt.NBTTemplate(nbt_b)
        self.assertNotEqual(a, b)

    def test_handle_request(self):
        expected_out = "{ }  Entity data\n    [All tags from entity]\n    [" \
                       "All tags from mob]\n    [All tags from breedable]"
        out = nbt.handle_nbt_request("cow")
        self.assertEqual(out, expected_out)
