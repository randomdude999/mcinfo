import sys
from contextlib import contextmanager
import unittest

from mcinfo import cli


@contextmanager
def redirect_stdout_stdin(new_stdout, new_stdin):
    old_stdout, sys.stdout = sys.stdout, new_stdout
    old_stdin, sys.stdin = sys.stdin, new_stdin
    try:
        yield new_stdout, new_stdin
    finally:
        sys.stdout = old_stdout
        sys.stdin = old_stdin


class TestCLI(unittest.TestCase):

    def test_handle_req_normal(self):
        req = "test"
        expected_out = 'Warning: This is test data! It is not at all useful ' \
                       'for you.\nRecipes:\n'
        self.assertEqual(cli.handle_req(req), expected_out)

    def test_handle_req_nbt(self):
        req = "nbt:test"
        expected_out = "{ }  example nbt structure\n    [All tags from 3]\n  "\
                       "  [All tags from other]\n    [All tags from " \
                       "things]\n    a_string: txt  A string! what did you " \
                       "expect, the spanish inquisition?\n    a_byte: B  A " \
                       "byte. This one has 256 possible values.\n    list: [ "\
                       "]  example list\n        txt  the string."
        self.assertEqual(cli.handle_req(req), expected_out)
