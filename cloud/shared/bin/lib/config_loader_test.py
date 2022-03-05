import unittest

from config_loader import ConfigLoader

# To run the tests: python3 bin/lib/config_loader_test.py
class TestConfigLoader(unittest.TestCase):

    def test_validate_config_for_not_including_required(self):
        config_loader = ConfigLoader("fake_vars", "fake_defs")
        defs = {
            "FOO": {
                "required": True,
                "secret": False,
                "type": "string"
            }, 
            "Bar": {
                "required": True,
                "secret": False,
                "type": "string"
            }, 
            "Bat": {
                "required": False,
                "secret": False,
                "type": "string"
            }
        }

        configs = {
            "FOO": "test"
        }

        is_valid, errors = config_loader._validate_config(defs, configs)
        self.assertFalse(is_valid)
        self.assertEqual(errors, ['Bar is required, but not provided'])

    def test_validate_config_for_incorrect_enums(self):
        config_loader = ConfigLoader("fake_vars", "fake_defs")
        defs = {
            "FOO": {
                "required": True,
                "secret": False,
                "type": "enum", 
                "values": ['abc']
            }, 
        }

        configs = {
            "FOO": "test"
        }

        is_valid, errors = config_loader._validate_config(defs, configs)
        self.assertFalse(is_valid)
        self.assertEqual(errors, ['test not supported enum for FOO'])

    def test_validate_config_for_correct_enums(self):
        config_loader = ConfigLoader("fake_vars", "fake_defs")
        defs = {
            "FOO": {
                "required": True,
                "secret": False,
                "type": "enum", 
                "values": ['abc']
            }, 
        }

        configs = {
            "FOO": "abc"
        }

        is_valid, errors = config_loader._validate_config(defs, configs)
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])
    
    def test_validate_config_for_empty_enum(self):
        config_loader = ConfigLoader("fake_vars", "fake_defs")
        defs = {
            "FOO": {
                "required": True,
                "secret": False,
                "type": "enum", 
                "values": ['abc']
            }, 
        }

        configs = {
            "FOO": ""
        }

        is_valid, errors = config_loader._validate_config(defs, configs)
        self.assertFalse(is_valid)
        self.assertEqual(errors, [' not supported enum for FOO'])

if __name__ == '__main__':
    unittest.main()
