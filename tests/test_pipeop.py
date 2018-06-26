import unittest
from pipeop import pipes


def add2(a, b):
    return a + b


def add3(a, b, c):
    return a + b + c


class PipeOpTestCase(unittest.TestCase):

    @pipes
    def test_pipe_one_arg(self):
        assert [1, 2, 3] >> sum() == 6

    @pipes
    def test_pipe_two_args(self):
        assert 1 >> add2(2) == 3

    @pipes
    def test_pipe_three_args(self):
        assert 1 >> add3(2, 3) == 6

    @pipes
    def test_left_pipe(self):
        assert 2 << pow(3) == 9

    @pipes
    def test_pipe_one_arg_no_braces(self):
        assert [1, 2, 3] >> sum == 6

    @pipes
    def test_left_pipe_one_arg_no_braces(self):
        assert [1, 2, 3] << sum == 6

    @pipes(True)
    def test_explicit_cache(self):
        pass

    @pipes(False)
    def test_no_cache(self):
        assert [1, 2, 3] << sum == 6

    @pipes
    def test_multiline(self):
        assert (
            range(-5, 0)
            << map(lambda x: x + 1)
            << map(abs)
            << map(str)
            >> tuple
        ) == ('4', '3', '2', '1', '0')
