from main import hello_world
import unittest

class Test_main(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello_world(), "hello_world")