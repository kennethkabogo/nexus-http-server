"""
Unit tests for the homomorphic encryption module.
"""

import unittest
from nexus_server.security.homomorphic_encryption import HomomorphicEncryption


class TestHomomorphicEncryption(unittest.TestCase):
    """Test cases for the HomomorphicEncryption class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.homomorphic_encryption = HomomorphicEncryption()

    def test_generate_keys(self):
        """Test generating homomorphic encryption keys."""
        keys = self.homomorphic_encryption.generate_keys()
        
        self.assertIn('public_key', keys)
        self.assertIn('private_key', keys)
        self.assertEqual(keys['public_key'], 'public_key_placeholder')
        self.assertEqual(keys['private_key'], 'private_key_placeholder')

    def test_encrypt_decrypt_int(self):
        """Test encrypting and decrypting an integer value."""
        public_key = 'public_key_placeholder'
        private_key = 'private_key_placeholder'
        value = 42
        
        # Encrypt the value
        encrypted = self.homomorphic_encryption.encrypt_int(value, public_key)
        
        self.assertIn('encrypted_value', encrypted)
        self.assertEqual(encrypted['type'], 'integer')
        self.assertEqual(encrypted['encryption_scheme'], 'demo_homomorphic')
        
        # Decrypt the value
        decrypted = self.homomorphic_encryption.decrypt(encrypted, private_key)
        self.assertEqual(decrypted, value)

    def test_encrypt_decrypt_float(self):
        """Test encrypting and decrypting a float value."""
        public_key = 'public_key_placeholder'
        private_key = 'private_key_placeholder'
        value = 3.14159
        
        # Encrypt the value
        encrypted = self.homomorphic_encryption.encrypt_float(value, public_key)
        
        self.assertIn('encrypted_value', encrypted)
        self.assertEqual(encrypted['type'], 'float')
        self.assertEqual(encrypted['encryption_scheme'], 'demo_homomorphic')
        
        # Decrypt the value
        decrypted = self.homomorphic_encryption.decrypt(encrypted, private_key)
        self.assertAlmostEqual(decrypted, value, places=5)

    def test_homomorphic_add(self):
        """Test homomorphic addition."""
        public_key = 'public_key_placeholder'
        value_a = 15
        value_b = 25
        
        # Encrypt both values
        encrypted_a = self.homomorphic_encryption.encrypt_int(value_a, public_key)
        encrypted_b = self.homomorphic_encryption.encrypt_int(value_b, public_key)
        
        # Perform homomorphic addition
        result = self.homomorphic_encryption.homomorphic_add(encrypted_a, encrypted_b)
        
        self.assertIn('encrypted_value', result)
        self.assertIn('add(', result['encrypted_value'])
        self.assertEqual(result['type'], 'integer')
        self.assertEqual(result['operation'], 'addition')

    def test_homomorphic_multiply(self):
        """Test homomorphic multiplication."""
        public_key = 'public_key_placeholder'
        value = 15
        scalar = 3
        
        # Encrypt the value
        encrypted = self.homomorphic_encryption.encrypt_int(value, public_key)
        
        # Perform homomorphic multiplication
        result = self.homomorphic_encryption.homomorphic_multiply(encrypted, scalar)
        
        self.assertIn('encrypted_value', result)
        self.assertIn('mult(', result['encrypted_value'])
        self.assertEqual(result['type'], 'integer')
        self.assertEqual(result['operation'], 'multiplication')

    def test_encrypt_vector(self):
        """Test encrypting a vector of values."""
        public_key = 'public_key_placeholder'
        values = [1, 2.5, 3, 4.7]
        
        # Encrypt the vector
        encrypted_vector = self.homomorphic_encryption.encrypt_vector(values, public_key)
        
        self.assertEqual(len(encrypted_vector), len(values))
        self.assertEqual(encrypted_vector[0]['type'], 'integer')
        self.assertEqual(encrypted_vector[1]['type'], 'float')
        self.assertEqual(encrypted_vector[2]['type'], 'integer')
        self.assertEqual(encrypted_vector[3]['type'], 'float')

    def test_homomorphic_vector_sum(self):
        """Test computing the homomorphic sum of a vector."""
        public_key = 'public_key_placeholder'
        values = [1, 2, 3, 4, 5]
        
        # Encrypt the vector
        encrypted_vector = self.homomorphic_encryption.encrypt_vector(values, public_key)
        
        # Compute homomorphic sum
        result = self.homomorphic_encryption.homomorphic_vector_sum(encrypted_vector)
        
        self.assertIn('encrypted_value', result)
        self.assertIn('sum(', result['encrypted_value'])
        self.assertEqual(result['type'], 'float')
        self.assertEqual(result['operation'], 'vector_sum')

    def test_decrypt_with_wrong_type(self):
        """Test decrypting with wrong value type."""
        public_key = 'public_key_placeholder'
        private_key = 'private_key_placeholder'
        
        # Create an invalid encrypted value
        encrypted = {
            'encrypted_value': 'enc_invalid',
            'type': 'invalid_type',
            'encryption_scheme': 'demo_homomorphic'
        }
        
        # This should raise a ValueError
        with self.assertRaises(ValueError):
            self.homomorphic_encryption.decrypt(encrypted, private_key)


if __name__ == '__main__':
    unittest.main()