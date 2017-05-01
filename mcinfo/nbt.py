from __future__ import unicode_literals
import pkg_resources
import json
import textwrap

nbt_all_types = ['TAG_Byte', 'TAG_Short', 'TAG_Int', 'TAG_Long', 'TAG_Float',
                 'TAG_Double', 'TAG_String', 'TAG_Byte_Array', 'TAG_List',
                 'TAG_Int_Array', 'TAG_Compound']

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

wrapper = textwrap.TextWrapper


def pretty_format_nbt(nbt):
    indent = " " * 4
    if nbt.type == "TAG_Compound":
        out = ""
        for x in nbt.includes:
            out += "[All tags from {0}]\n".format(x)
        for x in sorted(nbt.data):
            out += "{0}: {1}\n".format(x, pretty_format_nbt(nbt.data[x]))
        out = indent + out.rstrip().replace("\n", "\n" + indent)
        return "{0}  {1}\n{2}".format(short_names[nbt.type], nbt.desc, out)
    elif nbt.type == "TAG_List":
        out = "{0}\n".format(pretty_format_nbt(nbt.data))
        out = indent + out.rstrip().replace("\n", "\n" + indent)
        return "{0}  {1}\n{2}".format(short_names[nbt.type], nbt.desc, out)
    else:
        return "{0}  {1}".format(short_names[nbt.type], nbt.desc)


class NBTTemplate(object):
    def __init__(self, data):
        if 'type' not in data:
            raise ValueError("Missing data type")
        if data['type'] in nbt_all_types:
            if data['type'] == "TAG_List":
                if 'content' not in data:
                    raise ValueError("Missing content for list")
                self.data = NBTTemplate(data['content'])
            elif data['type'] == "TAG_Compound":
                if 'includes' in data:
                    self.includes = data['includes']
                else:
                    self.includes = []
                self.data = {}
                if 'content' in data:
                    for k in sorted(data['content']):
                        self.data[k] = NBTTemplate(data['content'][k])
            self.type = data['type']
            try:
                self.desc = data['desc']
            except KeyError:
                self.desc = ""
        else:
            raise TypeError("Invalid data type")

    def __eq__(self, other):
        if type(self) == type(other):
            if self.type == other.type and self.desc == other.desc:
                if self.type == "TAG_Compound":
                    for k, v in sorted(self.data.items()):
                        if k not in other.data:
                            return False
                        if other.data[k] != v:
                            return False
                    return sorted(self.includes) == sorted(other.includes)
                elif self.type == "TAG_List":
                    return self.data == other.data
                else:
                    return True
        return False


def handle_nbt_request(request):
    if pkg_resources.resource_exists(__name__, "data/nbt/%s.json" %
                                     request):
        data_str = pkg_resources.resource_string(__name__, "data/nbt/%s.json" %
                                                 request)
        data = json.loads(data_str)
        return pretty_format_nbt(NBTTemplate(data))
