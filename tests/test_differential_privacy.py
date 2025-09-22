import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nexus_server.security.differential_privacy import add_laplace_noise, dp_count, dp_mean


class TestDifferentialPrivacy(unittest.TestCase):
    """Test differential privacy functionality"""
    
    def test_add_laplace_noise(self):
        """Test that Laplace noise is added to values"""
        original_value = 100.0
        epsilon = 1.0
        
        # Add noise multiple times
        noisy_values = [add_laplace_noise(original_value, epsilon) for _ in range(100)]
        
        # Check that not all values are exactly the same
        # (there's a tiny chance they could be, but it's extremely unlikely)
        unique_values = set(noisy_values)
        self.assertGreater(len(unique_values), 1)
        
        # Check that values are reasonably close to the original
        # (this is a probabilistic check)
        average = sum(noisy_values) / len(noisy_values)
        self.assertLess(abs(average - original_value), 10.0)
    
    def test_dp_count(self):
        """Test differentially private count"""
        items = list(range(100))  # 100 items
        epsilon = 1.0
        
        # Get noisy count
        noisy_count = dp_count(items, epsilon)
        
        # The noisy count should be reasonably close to 100
        # Note: This is a probabilistic test and might occasionally fail
        self.assertGreater(noisy_count, 50)  # Should be positive and reasonably large
        self.assertLess(noisy_count, 150)    # Should not be too large
    
    def test_dp_mean(self):
        """Test differentially private mean"""
        values = [10.0] * 100  # 100 values of 10.0 each
        epsilon = 1.0
        
        # Get noisy mean
        noisy_mean = dp_mean(values, epsilon)
        
        # The noisy mean should be reasonably close to 10.0
        # Note: This is a probabilistic test and might occasionally fail
        self.assertGreater(noisy_mean, 0)   # Should be positive
        self.assertLess(noisy_mean, 20)     # Should not be too large


if __name__ == '__main__':
    unittest.main()