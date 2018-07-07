import unittest
from pipeop import pipes


class PipeOpTestCase(unittest.TestCase):

    @pipes
    def test_chaining(self):
        assert 2 >> pow(2) >> print is None
