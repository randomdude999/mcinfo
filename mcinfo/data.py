import pkg_resources
import json
import textwrap


def format_data(data):
    out = ""
    for k, v in data.items():
        out += textwrap.fill("{}: {}".format(k.capitalize(), v), width=80)


def handle_request(request):
    if pkg_resources.resource_exists(__name__, "data/nbt/%s.json" %
                                     request):
        stream = pkg_resources.resource_stream(__name__, "data/nbt/%s.json" %
                                               request)
        data = json.load(stream)
        return format_data(data)
