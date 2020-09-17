import unittest

from whole_process.whole_process import process_image


class TestWholeProcess(unittest.TestCase):
    def test_it(self):
        res = process_image("./tests/path_config.json", "tests/form_for_test/image.jpg")
        self.assertEqual((False, False, False, True, False), res.fields[0].recognized)
        self.assertEqual(("0", "3", " ", "0", "5", " ", "2", "0", "2", "0"), res.fields[1].recognized)
        self.assertEqual(("R", "Y", "C", "H", "L", "Y", " ", "M", "Q", "U", "C", "H", "Y"), res.fields[2].recognized)
