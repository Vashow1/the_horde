#!/usr/bin/env python3
import unittest
import os
from blueprints.base_model import BaseModel
import pep8

class TestBaseModel(unittest.Testcase):
    @classmethod
    def setupClass(cls):
        """Setting up class for test"""
        cls.base = BaseModel()
    
    @classmethod
    def teardown(cls):
        """destroy the class at the end"""
        del cls.base

    def test_pep8_base_model(self):
        """Testing that class passes pep8"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['blueprints/base_model.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")
    
    def test_check_for_documentation(self):
        """checking modules for documentation"""
        self.assertIsNotNone(BaseModel.__doc__)
        self.assertIsNotNone(BaseModel.__init__.__doc__)
        self.assertIsNotNone(BaseModel.__str__.__doc__)
        self.assertIsNotNone(BaseModel.save.__doc__)
        self.assertIsNotNone(BaseModel.to_dict.__doc__)

    def test_method_BaseModel(self):
        """checking if Basemodel have methods"""
        self.assertTrue(hasattr(BaseModel, "__init__"))
        self.assertTrue(hasattr(BaseModel, "save"))
        self.assertTrue(hasattr(BaseModel, "to_dict"))

    def test_init_BaseModel(self):
        """test if the base is an type BaseModel"""
        self.assertTrue(isinstance(self.base, BaseModel))


if __name__ == "__main__":
    unittest.main()