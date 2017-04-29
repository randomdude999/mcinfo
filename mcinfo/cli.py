from __future__ import print_function
import sys
import mcinfo.data
import mcinfo.nbt

try:
    # noinspection PyUnresolvedReferences,PyShadowingBuiltins
    input = raw_input
except NameError:
    pass


def handle_req(req):
    if req.startswith('nbt:'):
        return mcinfo.nbt.handle_nbt_request(req.replace('nbt:', '', 1))
    else:
        return mcinfo.normal_info.handle_request(req)


def input_loop():
    try:
        while True:
            inp = input('> ')
            if inp in ('quit', 'exit'):
                break
            print(handle_req(inp))
    except KeyboardInterrupt:
        print('\n')


def main():
    args = sys.argv[1:]
    if len(args) < 1:
        input_loop()
    else:
        # Not using print because someone already adds an extra newline
        sys.stdout.write(handle_req(' '.join(args)))

if __name__ == '__main__':
    main()
