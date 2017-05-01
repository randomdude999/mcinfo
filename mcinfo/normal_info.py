from __future__ import unicode_literals
import pkg_resources
import json
import textwrap
import mcinfo


def format_data(data):
    out = ""
    for k, v in sorted(data.items()):
        out += textwrap.fill("{0}: {1}".format(k.capitalize(), v), width=80,
                             subsequent_indent="  ") + "\n"
    return out.rstrip()


def handle_request(request):
    out = ""
    if pkg_resources.resource_exists(__name__, "data/%s.json" %
                                     request):
        data_str = pkg_resources.resource_string(__name__, "data/%s.json" %
                                                 request)
        data = json.loads(data_str)
        out = format_data(data)

    if pkg_resources.resource_exists(__name__, "data/recipes/%s.json" %
                                     request):
        data_str = pkg_resources.resource_string(__name__,
                                                 "data/recipes/%s.json" %
                                                 request)
        data = json.load(data_str)
        out += "\nRecipes:\n"
        out += str(mcinfo.recipes.RecipeCollection(data)).rstrip()
    return out
