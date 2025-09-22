"""
Unit tests for the AI privacy module.
"""

import unittest
import time
from nexus_server.security.ai_privacy import AIPrivacyManager


class TestAIPrivacyManager(unittest.TestCase):
    """Test cases for the AIPrivacyManager class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.ai_privacy_manager = AIPrivacyManager()

    def test_set_ai_opt_out(self):
        """Test setting AI training data opt-out preference."""
        user_id = "user_123"
        
        # Set opt-out preference
        result = self.ai_privacy_manager.set_ai_opt_out(user_id, True)
        
        self.assertIn('message', result)
        self.assertTrue(result['opt_out'])
        self.assertIn('opted out', result['message'])
        
        # Check that the preference was set
        self.assertTrue(self.ai_privacy_manager.is_ai_opt_out(user_id))

    def test_set_ai_opt_in(self):
        """Test setting AI training data opt-in preference."""
        user_id = "user_456"
        
        # Set opt-in preference
        result = self.ai_privacy_manager.set_ai_opt_out(user_id, False)
        
        self.assertIn('message', result)
        self.assertFalse(result['opt_out'])
        self.assertIn('opted in', result['message'])
        
        # Check that the preference was set
        self.assertFalse(self.ai_privacy_manager.is_ai_opt_out(user_id))

    def test_get_ai_opt_out_status(self):
        """Test getting AI training data opt-out status."""
        user_id = "user_789"
        
        # Set opt-out preference
        self.ai_privacy_manager.set_ai_opt_out(user_id, True)
        
        # Get status
        status = self.ai_privacy_manager.get_ai_opt_out_status(user_id)
        
        self.assertEqual(status['user_id'], user_id)
        self.assertTrue(status['opt_out'])
        self.assertEqual(status['status'], 'opted_out')
        self.assertIsNotNone(status['set_at'])

    def test_add_ai_privacy_headers(self):
        """Test adding AI privacy headers."""
        # Start with some existing headers
        existing_headers = [
            ('Content-Type', 'application/json'),
            ('Cache-Control', 'no-cache')
        ]
        
        # Add AI privacy headers
        updated_headers = self.ai_privacy_manager.add_ai_privacy_headers(existing_headers)
        
        # Check that existing headers are preserved
        self.assertIn(('Content-Type', 'application/json'), updated_headers)
        self.assertIn(('Cache-Control', 'no-cache'), updated_headers)
        
        # Check that AI privacy headers are added
        self.assertIn(('X-AI-Training-Opt-Out', 'true'), updated_headers)
        self.assertIn(('X-No-AI-Model-Training', 'true'), updated_headers)
        self.assertIn(('X-No-Machine-Learning', 'true'), updated_headers)
        self.assertIn(('X-AI-Respect-Privacy', 'true'), updated_headers)
        self.assertIn(('X-Do-Not-Train', 'true'), updated_headers)
        self.assertIn(('X-Do-Not-Profile', 'true'), updated_headers)

    def test_log_ai_training_request(self):
        """Test logging an AI training request."""
        request_info = {
            'model_type': 'recommendation',
            'data_sources': ['user_data_1', 'user_data_2'],
            'training_parameters': {'epochs': 10, 'batch_size': 32}
        }
        
        # Log the request
        request_id = self.ai_privacy_manager.log_ai_training_request(request_info)
        
        self.assertTrue(request_id.startswith('ai_train_'))
        self.assertEqual(len(self.ai_privacy_manager.ai_training_requests), 1)
        
        # Check the logged request
        logged_request = self.ai_privacy_manager.ai_training_requests[0]
        self.assertEqual(logged_request['request_id'], request_id)
        self.assertEqual(logged_request['request_info'], request_info)

    def test_start_model_training_job(self):
        """Test starting an AI model training job."""
        job_id = "job_123"
        model_type = "recommendation_model"
        data_sources = ["user_data_1", "user_data_2", "user_data_3"]
        
        # Set opt-out for one data source
        self.ai_privacy_manager.set_ai_opt_out("user_data_2", True)
        
        # Start the training job
        job_info = self.ai_privacy_manager.start_model_training_job(
            job_id, model_type, data_sources
        )
        
        self.assertEqual(job_info['job_id'], job_id)
        self.assertEqual(job_info['model_type'], model_type)
        self.assertEqual(job_info['data_sources'], data_sources)
        self.assertIn('user_data_2', job_info['opted_out_sources'])
        self.assertEqual(job_info['excluded_sources'], 1)
        self.assertEqual(job_info['included_sources'], 2)
        self.assertEqual(job_info['status'], 'partially_running')

    def test_get_ai_training_jobs(self):
        """Test getting AI training jobs."""
        # Start a training job
        self.ai_privacy_manager.start_model_training_job(
            "job_123", "model_type_1", ["data_1"]
        )
        
        # Start another training job
        self.ai_privacy_manager.start_model_training_job(
            "job_456", "model_type_2", ["data_2", "data_3"]
        )
        
        # Get all training jobs
        jobs = self.ai_privacy_manager.get_ai_training_jobs()
        
        self.assertEqual(len(jobs), 2)
        self.assertIn('job_123', jobs)
        self.assertIn('job_456', jobs)
        self.assertEqual(jobs['job_123']['model_type'], 'model_type_1')
        self.assertEqual(jobs['job_456']['model_type'], 'model_type_2')

    def test_get_ai_privacy_report(self):
        """Test getting AI privacy report."""
        user_id = "user_123"
        
        # Set opt-out preference
        self.ai_privacy_manager.set_ai_opt_out(user_id, True)
        
        # Get privacy report
        report = self.ai_privacy_manager.get_ai_privacy_report(user_id)
        
        self.assertEqual(report['user_id'], user_id)
        self.assertTrue(report['opt_out_status']['opt_out'])
        self.assertEqual(report['protection_status'], 'active')
        self.assertIsNotNone(report['report_generated_at'])

    def test_is_ai_opt_out_default(self):
        """Test default AI opt-out status."""
        user_id = "new_user"
        
        # Check default opt-out status (should be False)
        self.assertFalse(self.ai_privacy_manager.is_ai_opt_out(user_id))


if __name__ == '__main__':
    unittest.main()