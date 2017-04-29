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


def pretty_format_nbt(nbt_data):
    if nbt_data.type == "TAG_Compound":
        indent_level = 4
        out = ""
        for x in nbt_data.includes:
            out += "[All tags from " + x + "]\n"
        for x in nbt_data.data:
            out += x + ": " + pretty_format_nbt(nbt_data.data[x]) + "\n"
        out = " " * indent_level + out.replace("\n",
                                               "\n" + (indent_level * " "))
        return short_names[nbt_data.type] + "  " + nbt_data.description + \
            "\n" + out.rstrip()
    elif nbt_data.type == "TAG_List":
        indent_level = 4
        out = ""
        for x in nbt_data.data:
            out += pretty_format_nbt(x)
        out = " " * indent_level + out.replace("\n",
                                               "\n" + (indent_level * " "))
        return short_names[nbt_data.type] + "  " + nbt_data.description + \
            "\n" + out
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
                self.includes = data['includes']
                self.data = {}
                for k in data['content']:
                    self.data[k] = NBTTemplate(data['content'][k])
            self.type = data['type']
            self.description = data['desc']
        else:
            raise TypeError("Invalid data type")


def handle_nbt_request(request):
    if pkg_resources.resource_exists(__name__, "data/nbt/%s.json" %
                                     request):
        stream = pkg_resources.resource_stream(__name__, "data/nbt/%s.json" %
                                               request)
        data = json.load(stream)
        return pretty_format_nbt(NBTTemplate(data))
