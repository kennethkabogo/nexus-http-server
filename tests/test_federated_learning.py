"""
Tests for the federated learning module.
"""

import unittest
import json
from nexus_server.security.federated_learning import FederatedLearningCoordinator


class TestFederatedLearningCoordinator(unittest.TestCase):
    """Test cases for the FederatedLearningCoordinator class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.coordinator = FederatedLearningCoordinator()
        self.sample_model = {
            'weights': [0.1, 0.2, 0.3],
            'bias': 0.05
        }
        
    def test_initialize_model(self):
        """Test initializing the global model."""
        self.coordinator.initialize_model(self.sample_model)
        self.assertEqual(self.coordinator.global_model, self.sample_model)
        
    def test_start_training_round(self):
        """Test starting a new training round."""
        self.coordinator.initialize_model(self.sample_model)
        round_info = self.coordinator.start_training_round('round_1')
        
        self.assertEqual(round_info['round_id'], 'round_1')
        self.assertEqual(round_info['status'], 'active')
        self.assertIn('started_at', round_info)
        
    def test_submit_client_update(self):
        """Test submitting a client update."""
        self.coordinator.initialize_model(self.sample_model)
        self.coordinator.start_training_round('round_1')
        
        client_update = {
            'weights': [0.05, 0.15, 0.25],
            'bias': 0.02
        }
        
        success = self.coordinator.submit_client_update('client_1', 'round_1', client_update)
        self.assertTrue(success)
        
        # Check that the update was stored
        updates = self.coordinator.client_updates['round_1']
        self.assertEqual(len(updates), 1)
        self.assertEqual(updates[0]['client_id'], 'client_1')
        
    def test_submit_client_update_invalid_round(self):
        """Test submitting a client update to an invalid round."""
        client_update = {
            'weights': [0.05, 0.15, 0.25],
            'bias': 0.02
        }
        
        success = self.coordinator.submit_client_update('client_1', 'invalid_round', client_update)
        self.assertFalse(success)
        
    def test_aggregate_updates_fedavg(self):
        """Test aggregating updates using federated averaging."""
        self.coordinator.initialize_model(self.sample_model)
        self.coordinator.start_training_round('round_1')
        
        # Submit updates from multiple clients
        client_updates = [
            {'weights': [0.05, 0.15, 0.25], 'bias': 0.02},
            {'weights': [0.15, 0.25, 0.35], 'bias': 0.08},
            {'weights': [0.10, 0.20, 0.30], 'bias': 0.05}
        ]
        
        for i, update in enumerate(client_updates):
            self.coordinator.submit_client_update(f'client_{i}', 'round_1', update)
            
        # Aggregate updates
        updated_model = self.coordinator.aggregate_updates('round_1', 'fedavg')
        
        # Check that the model was updated
        self.assertIn('weights', updated_model)
        self.assertIn('bias', updated_model)
        
        # Check that round status was updated
        round_status = self.coordinator.get_round_status('round_1')
        self.assertEqual(round_status['status'], 'completed')
        self.assertEqual(round_status['participant_count'], 3)
        
    def test_get_round_status(self):
        """Test getting round status."""
        self.coordinator.initialize_model(self.sample_model)
        self.coordinator.start_training_round('round_1')
        
        status = self.coordinator.get_round_status('round_1')
        self.assertEqual(status['round_id'], 'round_1')
        self.assertEqual(status['status'], 'active')
        
    def test_get_client_statistics(self):
        """Test getting client participation statistics."""
        self.coordinator.initialize_model(self.sample_model)
        self.coordinator.start_training_round('round_1')
        
        # Submit updates from clients
        client_update = {'weights': [0.05, 0.15, 0.25], 'bias': 0.02}
        self.coordinator.submit_client_update('client_a', 'round_1', client_update)
        self.coordinator.submit_client_update('client_b', 'round_1', client_update)
        self.coordinator.submit_client_update('client_a', 'round_1', client_update)  # Client A participates twice
        
        stats = self.coordinator.get_client_statistics()
        self.assertEqual(stats['client_a'], 2)
        self.assertEqual(stats['client_b'], 1)


if __name__ == '__main__':
    unittest.main()