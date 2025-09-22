import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nexus_server.security.encryption import encrypt_data, decrypt_data


class TestEncryption(unittest.TestCase):
    """Test encryption functionality"""
    
    def test_encrypt_decrypt(self):
        """Test that data can be encrypted and then decrypted correctly"""
        original_data = "This is a secret message"
        password = "strongpassword123"
        
        # Encrypt the data
        encrypted = encrypt_data(original_data, password)
        
        # Decrypt the data
        decrypted = decrypt_data(encrypted, password)
        
        # Check that the decrypted data matches the original
        self.assertEqual(original_data, decrypted)
    
    def test_different_passwords(self):
        """Test that different passwords produce different results"""
        data = "Secret message"
        password1 = "password1"
        password2 = "password2"
        
        encrypted1 = encrypt_data(data, password1)
        encrypted2 = encrypt_data(data, password2)
        
        # The encrypted data should be different
        self.assertNotEqual(encrypted1['data'], encrypted2['data'])
        
        # Both should decrypt correctly with their respective passwords
        decrypted1 = decrypt_data(encrypted1, password1)
        decrypted2 = decrypt_data(encrypted2, password2)
        
        self.assertEqual(data, decrypted1)
        self.assertEqual(data, decrypted2)
    
    def test_same_data_different_salts(self):
        """Test that encrypting the same data twice produces different results"""
        data = "Secret message"
        password = "password"
        
        encrypted1 = encrypt_data(data, password)
        encrypted2 = encrypt_data(data, password)
        
        # The encrypted data should be different due to different salts
        self.assertNotEqual(encrypted1['data'], encrypted2['data'])
        self.assertNotEqual(encrypted1['salt'], encrypted2['salt'])
        
        # Both should decrypt correctly
        decrypted1 = decrypt_data(encrypted1, password)
        decrypted2 = decrypt_data(encrypted2, password)
        
        self.assertEqual(data, decrypted1)
        self.assertEqual(data, decrypted2)


if __name__ == '__main__':
    unittest.main()