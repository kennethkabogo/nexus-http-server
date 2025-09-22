"""
Test cases for zero-knowledge encryption functionality.
"""

import unittest
import json
from nexus_server.security.zero_knowledge import ZeroKnowledgeEncryption


class TestZeroKnowledgeEncryption(unittest.TestCase):
    """Test cases for the ZeroKnowledgeEncryption class."""

    def setUp(self):
        """Set up test fixtures."""
        self.encryption = ZeroKnowledgeEncryption()
        self.test_password = "test_password_123"
        self.test_data = {"message": "This is a secret", "value": 42}
        self.test_string = "This is a secret string"

    def test_generate_key_from_password(self):
        """Test generating a key from a password."""
        key, salt = self.encryption.generate_key_from_password(self.test_password)
        self.assertIsInstance(key, bytes)
        self.assertIsInstance(salt, bytes)
        self.assertEqual(len(salt), 16)  # Salt should be 16 bytes

    def test_generate_key_from_password_with_salt(self):
        """Test generating a key with a provided salt."""
        salt = b"salt_123456789012"
        key1, _ = self.encryption.generate_key_from_password(self.test_password, salt)
        key2, _ = self.encryption.generate_key_from_password(self.test_password, salt)
        self.assertEqual(key1, key2)  # Same salt should produce same key

    def test_encrypt_decrypt_data_for_storage_dict(self):
        """Test encrypting and decrypting dictionary data."""
        encrypted = self.encryption.encrypt_data_for_storage(self.test_data, self.test_password)
        self.assertIn('encrypted_data', encrypted)
        self.assertIn('salt', encrypted)
        self.assertIn('version', encrypted)
        self.assertIn('algorithm', encrypted)
        
        decrypted = self.encryption.decrypt_data_from_storage(encrypted, self.test_password)
        self.assertEqual(decrypted, self.test_data)

    def test_encrypt_decrypt_data_for_storage_string(self):
        """Test encrypting and decrypting string data."""
        encrypted = self.encryption.encrypt_data_for_storage(self.test_string, self.test_password)
        decrypted = self.encryption.decrypt_data_from_storage(encrypted, self.test_password)
        self.assertEqual(decrypted, self.test_string)

    def test_encrypt_decrypt_with_generated_key(self):
        """Test encrypting and decrypting with a generated key."""
        key = self.encryption.generate_encryption_key()
        encrypted = self.encryption.encrypt_with_key(self.test_data, key)
        decrypted = self.encryption.decrypt_with_key(encrypted, key)
        self.assertEqual(decrypted, self.test_data)

    def test_decrypt_with_wrong_password(self):
        """Test that decryption fails with wrong password."""
        encrypted = self.encryption.encrypt_data_for_storage(self.test_data, self.test_password)
        with self.assertRaises(ValueError):
            self.encryption.decrypt_data_from_storage(encrypted, "wrong_password")

    def test_decrypt_with_wrong_key(self):
        """Test that decryption fails with wrong key."""
        key1 = self.encryption.generate_encryption_key()
        key2 = self.encryption.generate_encryption_key()
        encrypted = self.encryption.encrypt_with_key(self.test_data, key1)
        with self.assertRaises(ValueError):
            self.encryption.decrypt_with_key(encrypted, key2)

    def test_encrypt_decrypt_complex_data(self):
        """Test encrypting and decrypting complex nested data."""
        complex_data = {
            "user": {
                "name": "John Doe",
                "age": 30,
                "preferences": ["reading", "coding", "hiking"],
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown"
                }
            },
            "timestamp": 1234567890,
            "active": True
        }
        
        encrypted = self.encryption.encrypt_data_for_storage(complex_data, self.test_password)
        decrypted = self.encryption.decrypt_data_from_storage(encrypted, self.test_password)
        self.assertEqual(decrypted, complex_data)


if __name__ == '__main__':
    unittest.main()