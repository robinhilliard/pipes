import unittest
from pipeop import pipes


def add2(a, b):
    return a + b


def add3(a, b, c):
    return a + b + c


class PipeOpTestCase(unittest.TestCase):

    @pipes
    def test_chaining_1(self):
        assert 2 >> pow(2) >> print is None

    @pipes
    def test_chaining_2(self):
        assert range(-5, 0) << map(abs) >> list == [5, 4, 3, 2, 1]
