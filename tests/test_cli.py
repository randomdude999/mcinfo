import sys, io
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


@contextmanager
def redirect_stdout(new_stdout):
    old_stdout, sys.stdout = sys.stdout, new_stdout
    try:
        yield new_stdout
    finally:
        sys.stdout = old_stdout


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

    def test_main_with_args(self):
        expected_out = 'Warning: This is test data! It is not at all useful ' \
                       'for you.\nRecipes:\n'
        args = ["test"]
        new_stdout = io.StringIO()
        with redirect_stdout(new_stdout):
            cli.main(args)
        new_stdout.seek(0)
        out = new_stdout.read()
        self.assertEqual(out, expected_out)

    def test_main_interactive(self):
        new_stdin = io.StringIO("test\nexit\n")
        new_stdout = io.StringIO()
        with redirect_stdout_stdin(new_stdout, new_stdin):
            cli.main([])
        new_stdout.seek(0)
        out = new_stdout.read()
        expected_out = "> Warning: This is test data! It is not at all " \
                       "useful for you.\nRecipes:\n\n> "
        self.assertEqual(out, expected_out)
