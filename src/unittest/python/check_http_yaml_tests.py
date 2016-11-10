'''
Created on 15.09.2013

@author: Marco Hoyer
'''
import unittest
import check_http_yaml


class Test(unittest.TestCase):
    
    def test_exit_ok(self):
        with self.assertRaises(SystemExit) as cm:
            check_http_yaml.exit_ok("Test")
            self.assertEqual(cm.exception.code, 0)
            
    def test_exit_warning(self):
        with self.assertRaises(SystemExit) as cm:
            check_http_yaml.exit_warning("Test")
            self.assertEqual(cm.exception.code, 1)
    
    def test_exit_critical(self):
        with self.assertRaises(SystemExit) as cm:
            check_http_yaml.exit_critical("Test")
            self.assertEqual(cm.exception.code, 2)
            
    def test_exit_unknown(self):
        with self.assertRaises(SystemExit) as cm:
            check_http_yaml.exit_unknown("Test")
            self.assertEqual(cm.exception.code, 3)
    
    def test_check_value(self):
        with self.assertRaises(SystemExit) as cm:
            check_http_yaml.check_value("TEST", 1, 5, 10, False)
            self.assertEqual(cm.exception.code, 0)
        with self.assertRaises(SystemExit) as cm:
            check_http_yaml.check_value("TEST", 6, 5, 10, False)
            self.assertEqual(cm.exception.code, 1)
        with self.assertRaises(SystemExit) as cm:
            check_http_yaml.check_value("TEST", 12, 5, 10, False)
            self.assertEqual(cm.exception.code, 2)
        with self.assertRaises(SystemExit) as cm:
            check_http_yaml.check_value("TEST", 0, 5, 10, False)
            self.assertEqual(cm.exception.code, 0)
        with self.assertRaises(SystemExit) as cm:
            check_http_yaml.check_value("TEST", 5, 5, 10, False)
            self.assertEqual(cm.exception.code, 1)
        with self.assertRaises(SystemExit) as cm:
            check_http_yaml.check_value("TEST", 10, 5, 10, False)
            self.assertEqual(cm.exception.code, 2)
            
    def test_check_value_inverted(self):
        with self.assertRaises(SystemExit) as cm:
            check_http_yaml.check_value("TEST", 12, 10, 5, True)
            self.assertEqual(cm.exception.code, 0)
        with self.assertRaises(SystemExit) as cm:
            check_http_yaml.check_value("TEST", 7, 10, 5, True)
            self.assertEqual(cm.exception.code, 1)
        with self.assertRaises(SystemExit) as cm:
            check_http_yaml.check_value("TEST", 3, 10, 5, True)
            self.assertEqual(cm.exception.code, 2)
        with self.assertRaises(SystemExit) as cm:
            check_http_yaml.check_value("TEST", 11, 10, 5, True)
            self.assertEqual(cm.exception.code, 0)
        with self.assertRaises(SystemExit) as cm:
            check_http_yaml.check_value("TEST", 10, 10, 5, True)
            self.assertEqual(cm.exception.code, 1)
        with self.assertRaises(SystemExit) as cm:
            check_http_yaml.check_value("TEST", 5, 10, 5, True)
            self.assertEqual(cm.exception.code, 2)
            
    def test_find_value_for_key(self):
        # test simple key-value dict
        self.assertEqual(check_http_yaml.find_value_for_key({"TEST":100}, "TEST"),100)
        # test case sensivity
        self.assertEqual(check_http_yaml.find_value_for_key({"test":200,"TEST":100}, "TEST"),100)
        # test more complex dict
        self.assertEqual(check_http_yaml.find_value_for_key({"A":100,"B":200,"C":300,"D":400}, "C"),300)
        
        # test exitting with unknown if there is no usable value
        with self.assertRaises(SystemExit) as cm:
            check_http_yaml.find_value_for_key({"TEST":"A"},"TEST")
            self.assertEqual(cm.exception.code, 3)


    def test_get_url(self):
        self.assertEqual(check_http_yaml.get_url("testhost", 9000, "/icinga-status?query=STATUSFILEAGETT"),"http://testhost:9000/icinga-status?query=STATUSFILEAGETT")

    def test_parse_yaml(self):
        self.assertEqual(check_http_yaml.parse_yaml("{statusfileage: 100}"), {"statusfileage":100})
        self.assertEqual(check_http_yaml.parse_yaml("{1: 100}"), {1:100})
        
    def test_parse_json(self):
        self.assertEqual(check_http_yaml.parse_json('["foo", {"bar":["baz", null, 1.0, 2]}]'), [u'foo', {u'bar': [u'baz', None, 1.0, 2]}])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()