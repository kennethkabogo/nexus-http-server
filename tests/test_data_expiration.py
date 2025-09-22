"""
Unit tests for the data expiration module.
"""

import unittest
import time
from nexus_server.security.data_expiration import DataExpirationManager


class TestDataExpirationManager(unittest.TestCase):
    """Test cases for the DataExpirationManager class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.data_expiration_manager = DataExpirationManager()

    def test_set_data_expiration(self):
        """Test setting data expiration."""
        data_id = "data_123"
        ttl_seconds = 10
        
        # Set expiration
        result = self.data_expiration_manager.set_data_expiration(data_id, ttl_seconds)
        
        self.assertTrue(result)
        
        # Check that expiration info is stored
        expiration_info = self.data_expiration_manager.get_expiration_info(data_id)
        self.assertIsNotNone(expiration_info)
        self.assertEqual(expiration_info['ttl_seconds'], ttl_seconds)
        self.assertGreater(expiration_info['expires_at'], time.time())

    def test_get_expiration_info(self):
        """Test getting expiration info."""
        data_id = "data_456"
        ttl_seconds = 5
        
        # Set expiration
        self.data_expiration_manager.set_data_expiration(data_id, ttl_seconds)
        
        # Get expiration info
        expiration_info = self.data_expiration_manager.get_expiration_info(data_id)
        
        self.assertEqual(expiration_info['ttl_seconds'], ttl_seconds)
        self.assertGreater(expiration_info['time_remaining'], 0)
        self.assertFalse(expiration_info['is_expired'])

    def test_cancel_expiration(self):
        """Test canceling data expiration."""
        data_id = "data_789"
        ttl_seconds = 10
        
        # Set expiration
        self.data_expiration_manager.set_data_expiration(data_id, ttl_seconds)
        
        # Cancel expiration
        result = self.data_expiration_manager.cancel_expiration(data_id)
        
        self.assertTrue(result)
        
        # Check that expiration info is removed
        expiration_info = self.data_expiration_manager.get_expiration_info(data_id)
        self.assertIsNone(expiration_info)

    def test_extend_expiration(self):
        """Test extending data expiration."""
        data_id = "data_abc"
        initial_ttl = 5
        extension_seconds = 10
        
        # Set expiration
        self.data_expiration_manager.set_data_expiration(data_id, initial_ttl)
        
        # Get initial expiration time
        initial_info = self.data_expiration_manager.get_expiration_info(data_id)
        initial_expires_at = initial_info['expires_at']
        
        # Extend expiration
        result = self.data_expiration_manager.extend_expiration(data_id, extension_seconds)
        
        self.assertTrue(result)
        
        # Check that expiration time was extended
        extended_info = self.data_expiration_manager.get_expiration_info(data_id)
        extended_expires_at = extended_info['expires_at']
        
        # The extended expiration should be later than the initial expiration
        self.assertGreater(extended_expires_at, initial_expires_at)
        self.assertEqual(extended_info['ttl_seconds'], initial_ttl + extension_seconds)

    def test_get_all_expiring_data(self):
        """Test getting all expiring data."""
        # Set expirations for multiple data items
        self.data_expiration_manager.set_data_expiration("data_1", 10)
        self.data_expiration_manager.set_data_expiration("data_2", 20)
        self.data_expiration_manager.set_data_expiration("data_3", 30)
        
        # Get all expiring data
        all_expiring = self.data_expiration_manager.get_all_expiring_data()
        
        self.assertEqual(len(all_expiring), 3)
        self.assertIn('data_1', all_expiring)
        self.assertIn('data_2', all_expiring)
        self.assertIn('data_3', all_expiring)


if __name__ == '__main__':
    unittest.main()