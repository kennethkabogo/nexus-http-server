"""
Test cases for privacy budget management functionality.
"""

import unittest
import time
from nexus_server.security.privacy_budget import PrivacyBudgetManager


class TestPrivacyBudgetManager(unittest.TestCase):
    """Test cases for the PrivacyBudgetManager class."""

    def setUp(self):
        """Set up test fixtures."""
        self.budget_manager = PrivacyBudgetManager()
        self.test_user_id = "test_user_123"

    def test_set_and_get_user_budget(self):
        """Test setting and getting user budget."""
        # Set budget
        self.budget_manager.set_user_budget(self.test_user_id, 5.0)
        
        # Get budget
        budget_info = self.budget_manager.get_user_budget(self.test_user_id)
        
        self.assertEqual(budget_info['total_epsilon'], 5.0)
        self.assertEqual(budget_info['consumed_epsilon'], 0.0)
        self.assertEqual(budget_info['remaining_epsilon'], 5.0)
        self.assertEqual(budget_info['usage_percentage'], 0.0)

    def test_consume_budget_success(self):
        """Test successfully consuming budget."""
        # Set initial budget
        self.budget_manager.set_user_budget(self.test_user_id, 3.0)
        
        # Consume some budget
        success = self.budget_manager.consume_budget(self.test_user_id, 1.0, "count_query")
        
        self.assertTrue(success)
        
        # Check updated budget
        budget_info = self.budget_manager.get_user_budget(self.test_user_id)
        self.assertEqual(budget_info['consumed_epsilon'], 1.0)
        self.assertEqual(budget_info['remaining_epsilon'], 2.0)
        self.assertAlmostEqual(budget_info['usage_percentage'], 100 * 1.0 / 3.0, places=10)

    def test_consume_budget_insufficient(self):
        """Test consuming more budget than available."""
        # Set initial budget
        self.budget_manager.set_user_budget(self.test_user_id, 1.0)
        
        # Try to consume more than available
        success = self.budget_manager.consume_budget(self.test_user_id, 2.0, "count_query")
        
        self.assertFalse(success)
        
        # Check that budget was not consumed
        budget_info = self.budget_manager.get_user_budget(self.test_user_id)
        self.assertEqual(budget_info['consumed_epsilon'], 0.0)
        self.assertEqual(budget_info['remaining_epsilon'], 1.0)

    def test_consume_budget_multiple_times(self):
        """Test consuming budget multiple times."""
        # Set initial budget
        self.budget_manager.set_user_budget(self.test_user_id, 5.0)
        
        # Consume budget multiple times
        self.assertTrue(self.budget_manager.consume_budget(self.test_user_id, 1.0, "count_query"))
        self.assertTrue(self.budget_manager.consume_budget(self.test_user_id, 1.5, "mean_query"))
        self.assertTrue(self.budget_manager.consume_budget(self.test_user_id, 0.5, "histogram_query"))
        
        # Check final state
        budget_info = self.budget_manager.get_user_budget(self.test_user_id)
        self.assertEqual(budget_info['consumed_epsilon'], 3.0)
        self.assertEqual(budget_info['remaining_epsilon'], 2.0)
        self.assertEqual(len(budget_info['queries']), 3)

    def test_reset_budget(self):
        """Test resetting budget."""
        # Set initial budget and consume some
        self.budget_manager.set_user_budget(self.test_user_id, 5.0)
        self.budget_manager.consume_budget(self.test_user_id, 2.0, "count_query")
        
        # Reset budget
        self.budget_manager.reset_budget(self.test_user_id)
        
        # Check that budget is reset
        budget_info = self.budget_manager.get_user_budget(self.test_user_id)
        self.assertEqual(budget_info['consumed_epsilon'], 0.0)
        self.assertEqual(budget_info['remaining_epsilon'], 5.0)
        self.assertEqual(len(budget_info['queries']), 0)

    def test_get_budget_history(self):
        """Test getting budget history."""
        # Set initial budget and consume some
        self.budget_manager.set_user_budget(self.test_user_id, 5.0)
        self.budget_manager.consume_budget(self.test_user_id, 1.0, "count_query")
        time.sleep(0.01)  # Small delay to ensure different timestamps
        self.budget_manager.consume_budget(self.test_user_id, 1.5, "mean_query")
        
        # Get history
        history = self.budget_manager.get_budget_history(self.test_user_id)
        
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['query_type'], "count_query")
        self.assertEqual(history[0]['epsilon'], 1.0)
        self.assertEqual(history[1]['query_type'], "mean_query")
        self.assertEqual(history[1]['epsilon'], 1.5)

    def test_get_budget_history_limit(self):
        """Test getting budget history with limit."""
        # Set initial budget and consume many times
        self.budget_manager.set_user_budget(self.test_user_id, 10.0)
        for i in range(10):
            self.budget_manager.consume_budget(self.test_user_id, 0.1, f"query_{i}")
        
        # Get history with limit
        history = self.budget_manager.get_budget_history(self.test_user_id, limit=5)
        
        self.assertEqual(len(history), 5)
        # Should get the most recent 5 entries

    def test_suggest_epsilon(self):
        """Test suggesting epsilon values."""
        # Set initial budget
        self.budget_manager.set_user_budget(self.test_user_id, 5.0)
        
        # Get suggestions
        suggestions = self.budget_manager.suggest_epsilon(self.test_user_id)
        
        self.assertIn('suggestions', suggestions)
        self.assertIn('conservative', suggestions['suggestions'])
        self.assertIn('moderate', suggestions['suggestions'])
        self.assertIn('liberal', suggestions['suggestions'])
        self.assertGreater(suggestions['remaining_budget'], 0)

    def test_suggest_epsilon_after_consumption(self):
        """Test suggesting epsilon values after consuming some budget."""
        # Set initial budget and consume some
        self.budget_manager.set_user_budget(self.test_user_id, 5.0)
        self.budget_manager.consume_budget(self.test_user_id, 3.0, "count_query")
        
        # Get suggestions
        suggestions = self.budget_manager.suggest_epsilon(self.test_user_id)
        
        self.assertLess(suggestions['remaining_budget'], 5.0)
        self.assertGreater(suggestions['remaining_budget'], 0)


if __name__ == '__main__':
    unittest.main()