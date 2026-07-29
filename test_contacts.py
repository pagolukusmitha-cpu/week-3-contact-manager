import unittest
from contacts_manager import validate_phone, validate_email

class TestContacts(unittest.TestCase):

    def test_valid_phone(self):
        valid, phone = validate_phone("+1 (234) 567-8900")
        self.assertTrue(valid)

    def test_invalid_phone(self):
        valid, phone = validate_phone("123")
        self.assertFalse(valid)

    def test_email(self):
        self.assertTrue(validate_email("abc@gmail.com"))
        self.assertFalse(validate_email("abc@gmail"))

if __name__ == "__main__":
    unittest.main()