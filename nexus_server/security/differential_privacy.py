"""
Differential privacy utilities for privacy-preserving analytics.
"""
import random
import math
from typing import List, Union


def add_laplace_noise(value: float, epsilon: float, sensitivity: float = 1.0) -> float:
    """
    Add Laplace noise to a value for differential privacy.
    
    Args:
        value: The original value
        epsilon: Privacy parameter (smaller = more private)
        sensitivity: Sensitivity of the function (default 1.0 for counting queries)
        
    Returns:
        Value with added Laplace noise
    """
    # Scale parameter for Laplace distribution
    scale = sensitivity / epsilon
    
    # Generate Laplace noise
    u = random.uniform(-0.5, 0.5)
    noise = -scale * math.copysign(1.0, u) * math.log(1 - 2 * abs(u))
    
    return value + noise


def dp_count(items: List, epsilon: float) -> float:
    """
    Differentially private count of items.
    
    Args:
        items: List of items to count
        epsilon: Privacy parameter
        
    Returns:
        Noisy count
    """
    true_count = len(items)
    return add_laplace_noise(true_count, epsilon, sensitivity=1.0)


def dp_mean(values: List[Union[int, float]], epsilon: float) -> float:
    """
    Differentially private mean calculation.
    
    Args:
        values: List of numeric values
        epsilon: Privacy parameter (split between count and sum)
        
    Returns:
        Noisy mean
    """
    if not values:
        return 0.0
    
    # Split epsilon budget between count and sum queries
    epsilon_per_query = epsilon / 2
    
    # Get noisy count
    noisy_count = dp_count(values, epsilon_per_query)
    
    # Get noisy sum
    true_sum = sum(values)
    noisy_sum = add_laplace_noise(true_sum, epsilon_per_query, sensitivity=1.0)
    
    # Calculate noisy mean
    if noisy_count == 0:
        return 0.0
    
    return noisy_sum / noisy_count


def add_differential_privacy_routes():
    """
    Add differential privacy API routes.
    """
    from ..server import route, json_response
    from ..utils.validation import validate_json
    
    @route('/api/dp/count')
    @validate_json({
        'values': {'type': 'list', 'required': True},
        'epsilon': {'type': 'float', 'required': True, 'min': 0.01, 'max': 10.0}
    })
    def dp_count_handler(request):
        try:
            values = request.data['values']
            epsilon = request.data['epsilon']
            
            # For count queries, we just need the length
            result = dp_count(values, epsilon)
            
            return json_response({
                'noisy_count': result,
                'epsilon': epsilon
            })
        except Exception as e:
            return json_response({
                'error': f'DP count failed: {str(e)}'
            }, status='400 Bad Request')
    
    @route('/api/dp/mean')
    @validate_json({
        'values': {'type': 'list', 'required': True, 'schema': {'type': 'number'}},
        'epsilon': {'type': 'float', 'required': True, 'min': 0.01, 'max': 10.0}
    })
    def dp_mean_handler(request):
        try:
            values = request.data['values']
            epsilon = request.data['epsilon']
            
            result = dp_mean(values, epsilon)
            
            return json_response({
                'noisy_mean': result,
                'epsilon': epsilon
            })
        except Exception as e:
            return json_response({
                'error': f'DP mean failed: {str(e)}'
            }, status='400 Bad Request')