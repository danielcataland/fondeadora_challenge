import main
import unittest


class TestMain(unittest.TestCase):

    def test_manage_operations(self):
        self.assertEqual(main.manage_operations('ABC', 1), 'No compression needed')
        self.assertEqual(main.manage_operations('', 1), 'String not provided')
        self.assertEqual(main.manage_operations('', 2), 'String not provided')
        self.assertEqual(main.manage_operations('BCD', 2), 'BCD')
    
    def test_validate_input_encode(self):
        self.assertEqual(main.validate_input_encode(''), (False, 'String not provided'))
        self.assertEqual(main.validate_input_encode('ABV"'), (False, 'String must contains only chars [A-Z]'))
        self.assertEqual(main.validate_input_encode('ABVC'), (True, ''))

    def test_validate_input_decode(self):
        self.assertEqual(main.validate_input_decode(''), (False, 'String not provided'))
        self.assertEqual(main.validate_input_decode('('), (False, 'Incorrect input format, verify your input'))
        self.assertEqual(main.validate_input_decode('a(3)'), (False, 'Incorrect input format, verify your input'))
    
    def test_validate_quantity_format(self):
        self.assertTrue(main.validate_quantity_format('(z)'))
        self.assertFalse(main.validate_quantity_format('(Z)'))
        self.assertTrue(main.validate_quantity_format('(z1)'))
        self.assertFalse(main.validate_quantity_format('(z1z)'))
        self.assertTrue(main.validate_quantity_format('(b3)'))
        self.assertFalse(main.validate_quantity_format('(ZA)'))
        self.assertFalse(main.validate_quantity_format('(!)'))
        

    def test_encode_rle(self):
        self.assertEqual(main.encode_rle('AAAAAA'), 'A(6)')
        self.assertEqual(main.encode_rle('ABCCCCC'), 'ABC(5)')
        self.assertEqual(main.encode_rle('ABCCCCCD'), 'ABC(5)D')
        self.assertEqual(main.encode_rle('AABC'), 'AABC')
        self.assertEqual(main.encode_rle('AAAAAAAAAABC'), 'A(a)BC')
        self.assertEqual(main.encode_rle('AAAAAAAAAABBC'), 'A(a)BBC')
        self.assertEqual(main.encode_rle('AAAAAAAAAABBCC'), 'A(a)BBCC')
        self.assertEqual(main.encode_rle('AAAAAAAAAABBCCC'), 'A(a)BBC(3)')
    
    def test_encode_ascii_rule(self):
        assert main.encode_ascii_rule(5) == '5'
        assert main.encode_ascii_rule(10) == 'a'
        assert main.encode_ascii_rule(36) == 'z1'
    
    def test_decode_ascii_rule(self):
        self.assertEqual(main.decode_ascii_rule('z'), 35)
        self.assertEqual(main.decode_ascii_rule('7'), 7)
        self.assertEqual(main.decode_ascii_rule('zz'), 70)
    
    def test_decode_rle(self):
        self.assertEqual(main.decode_rle('A(3)'), 'AAA')
        self.assertEqual(main.decode_rle('B(b)'), 'BBBBBBBBBBB')
        self.assertEqual(main.decode_rle('B(b)C'), 'BBBBBBBBBBBC')
        self.assertEqual(main.decode_rle('A(a)C(a)BCD(7)'), 'AAAAAAAAAACCCCCCCCCCBCDDDDDDD')
    

if __name__ == '__main__':
    unittest.main()