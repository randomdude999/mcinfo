import pkg_resources
import json
import textwrap
import mcinfo


def format_data(data):
    out = ""
    for k, v in data.items():
        out += textwrap.fill("{}: {}\n".format(k.capitalize(), v), width=80,
                             replace_whitespace=False, drop_whitespace=False)
    return out.rstrip()


def handle_request(request):
    out = ""
    if pkg_resources.resource_exists(__name__, "data/%s.json" %
                                     request):
        stream = pkg_resources.resource_stream(__name__, "data/%s.json" %
                                               request)
        data = json.load(stream)
        out = format_data(data)

    if pkg_resources.resource_exists(__name__, "data/recipes/%s.json" %
                                     request):
        stream = pkg_resources.resource_stream(__name__, "data/recipes/%s.json"
                                               % request)
        data = json.load(stream)
        out += str(mcinfo.recipes.RecipeCollection(data))
    return out