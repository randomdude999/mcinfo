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
            out += "[All tags from {}]\n".format(x)
        for x in nbt.data:
            out += "{}: {}\n".format(x, pretty_format_nbt(nbt.data[x]))
        out = indent + out.rstrip().replace("\n", "\n" + indent)
        return "{}  {}\n{}".format(short_names[nbt.type], nbt.desc, out)
    elif nbt.type == "TAG_List":
        out = ""
        for x in nbt.data:
            out += "{}\n".format(pretty_format_nbt(x))
        out = indent + out.rstrip().replace("\n", "\n" + indent)
        return "{}  {}\n{}".format(short_names[nbt.type], nbt.desc, out)
    else:
        return "{}  {}".format(short_names[nbt.type], nbt.desc)


class NBTTemplate(object):
    def __init__(self, data):
        if data['type'] in nbt_all_types:
            if data['type'] == "TAG_List":
                self.data = []
                for x in data['content']:
                    self.data.append(NBTTemplate(x))
            elif data['type'] == "TAG_Compound":
                self.includes = data['includes']
                self.data = {}
                for k in data['content']:
                    self.data[k] = NBTTemplate(data['content'][k])
            self.type = data['type']
            self.desc = data['desc']
        else:
            raise TypeError("Invalid data type")


def handle_nbt_request(request):
    if pkg_resources.resource_exists(__name__, "data/nbt/%s.json" %
                                     request):
        stream = pkg_resources.resource_stream(__name__, "data/nbt/%s.json" %
                                               request)
        data = json.load(stream)
        return pretty_format_nbt(NBTTemplate(data))
