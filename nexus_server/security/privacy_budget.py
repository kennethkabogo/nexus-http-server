"""
Privacy Budget Management for Differential Privacy

This module provides utilities for managing differential privacy budgets,
allowing users to track and control their privacy consumption.
"""

import time
import json
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


class PrivacyBudgetManager:
    """
    Manages differential privacy budgets for users.
    
    This class tracks privacy budget consumption and provides
    mechanisms for budget allocation and monitoring.
    """
    
    def __init__(self):
        # Store privacy budgets for each user
        self.user_budgets: Dict[str, Dict] = defaultdict(lambda: {
            'total_epsilon': 1.0,  # Default total budget
            'consumed_epsilon': 0.0,  # Amount already used
            'queries': [],  # History of queries
            'created_at': time.time()
        })
    
    def set_user_budget(self, user_id: str, total_epsilon: float) -> None:
        """
        Set the total privacy budget for a user.
        
        Args:
            user_id: Unique identifier for the user
            total_epsilon: Total privacy budget (smaller = more private)
        """
        self.user_budgets[user_id]['total_epsilon'] = total_epsilon
        self.user_budgets[user_id]['updated_at'] = time.time()
    
    def get_user_budget(self, user_id: str) -> Dict:
        """
        Get the current privacy budget status for a user.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Dictionary with budget information
        """
        budget_info = self.user_budgets[user_id].copy()
        budget_info['remaining_epsilon'] = (
            budget_info['total_epsilon'] - budget_info['consumed_epsilon']
        )
        budget_info['usage_percentage'] = (
            budget_info['consumed_epsilon'] / budget_info['total_epsilon'] * 100
            if budget_info['total_epsilon'] > 0 else 0
        )
        return budget_info
    
    def consume_budget(self, user_id: str, epsilon: float, query_type: str) -> bool:
        """
        Consume a portion of the user's privacy budget.
        
        Args:
            user_id: Unique identifier for the user
            epsilon: Amount of budget to consume
            query_type: Type of query being performed
            
        Returns:
            True if budget was available and consumed, False otherwise
        """
        current_budget = self.user_budgets[user_id]
        remaining = current_budget['total_epsilon'] - current_budget['consumed_epsilon']
        
        if epsilon <= remaining:
            current_budget['consumed_epsilon'] += epsilon
            current_budget['queries'].append({
                'query_type': query_type,
                'epsilon': epsilon,
                'timestamp': time.time()
            })
            current_budget['updated_at'] = time.time()
            return True
        else:
            return False
    
    def reset_budget(self, user_id: str) -> None:
        """
        Reset a user's privacy budget.
        
        Args:
            user_id: Unique identifier for the user
        """
        if user_id in self.user_budgets:
            self.user_budgets[user_id]['consumed_epsilon'] = 0.0
            self.user_budgets[user_id]['queries'] = []
            self.user_budgets[user_id]['reset_at'] = time.time()
    
    def get_budget_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """
        Get the history of privacy budget usage for a user.
        
        Args:
            user_id: Unique identifier for the user
            limit: Maximum number of entries to return
            
        Returns:
            List of budget usage entries
        """
        if user_id in self.user_budgets:
            return self.user_budgets[user_id]['queries'][-limit:]
        return []
    
    def suggest_epsilon(self, user_id: str, sensitivity: float = 1.0) -> Dict:
        """
        Suggest an appropriate epsilon value based on remaining budget.
        
        Args:
            user_id: Unique identifier for the user
            sensitivity: Sensitivity of the query (default 1.0 for counting)
            
        Returns:
            Dictionary with suggested epsilon and explanation
        """
        budget_info = self.get_user_budget(user_id)
        remaining = budget_info['remaining_epsilon']
        
        # Suggest different levels based on remaining budget
        suggestions = {
            'conservative': min(0.1, remaining / 10),  # Very private
            'moderate': min(0.5, remaining / 3),       # Moderately private
            'liberal': min(1.0, remaining / 2)         # Less private
        }
        
        return {
            'suggestions': suggestions,
            'remaining_budget': remaining,
            'explanation': (
                f"You have {remaining:.4f} epsilon remaining. "
                f"Conservative suggestion: {suggestions['conservative']:.4f}, "
                f"Moderate suggestion: {suggestions['moderate']:.4f}, "
                f"Liberal suggestion: {suggestions['liberal']:.4f}"
            )
        }


# Global instance for the application
privacy_budget_manager = PrivacyBudgetManager()


def add_privacy_budget_routes():
    """
    Add privacy budget management API routes.
    """
    from ..server import route, json_response
    from ..utils.validation import validate_json
    
    @route('/api/privacy/budget')
    def get_budget_handler(request):
        """
        Get current privacy budget status for the authenticated user.
        """
        # In a real implementation, you would get the user_id from the authentication
        # For this example, we'll use a default user ID
        user = getattr(request, 'user', None)
        if user is not None:
            user_id = user.get('user_id', 'default_user')
        else:
            user_id = 'default_user'
        
        budget_info = privacy_budget_manager.get_user_budget(user_id)
        return json_response(budget_info)
    
    @route('/api/privacy/budget/history')
    def get_budget_history_handler(request):
        """
        Get privacy budget usage history for the authenticated user.
        """
        user = getattr(request, 'user', None)
        if user is not None:
            user_id = user.get('user_id', 'default_user')
        else:
            user_id = 'default_user'
        
        history = privacy_budget_manager.get_budget_history(user_id)
        return json_response({'history': history})
    
    @route('/api/privacy/budget/suggest')
    @validate_json({
        'sensitivity': {'type': 'float', 'required': False, 'default': 1.0}
    })
    def suggest_epsilon_handler(request):
        """
        Get suggestions for epsilon values based on remaining budget.
        """
        user = getattr(request, 'user', None)
        if user is not None:
            user_id = user.get('user_id', 'default_user')
        else:
            user_id = 'default_user'
        sensitivity = request.data.get('sensitivity', 1.0)
        
        suggestions = privacy_budget_manager.suggest_epsilon(user_id, sensitivity)
        return json_response(suggestions)
    
    @route('/api/privacy/budget/reset')
    def reset_budget_handler(request):
        """
        Reset privacy budget for the authenticated user.
        """
        user = getattr(request, 'user', None)
        if user is not None:
            user_id = user.get('user_id', 'default_user')
        else:
            user_id = 'default_user'
        
        privacy_budget_manager.reset_budget(user_id)
        return json_response({
            'message': 'Privacy budget has been reset',
            'status': 'success'
        })
    
    @route('/api/privacy/budget/consume')
    @validate_json({
        'epsilon': {'type': 'float', 'required': True, 'min': 0.001, 'max': 10.0},
        'query_type': {'type': 'string', 'required': True}
    })
    def consume_budget_handler(request):
        """
        Manually consume a portion of the privacy budget.
        """
        user = getattr(request, 'user', None)
        if user is not None:
            user_id = user.get('user_id', 'default_user')
        else:
            user_id = 'default_user'
        epsilon = request.data['epsilon']
        query_type = request.data['query_type']
        
        success = privacy_budget_manager.consume_budget(user_id, epsilon, query_type)
        
        if success:
            return json_response({
                'message': f'Successfully consumed {epsilon} epsilon',
                'remaining_budget': (
                    privacy_budget_manager.get_user_budget(user_id)['remaining_epsilon']
                ),
                'status': 'success'
            })
        else:
            budget_info = privacy_budget_manager.get_user_budget(user_id)
            return json_response({
                'error': 'Insufficient privacy budget',
                'requested': epsilon,
                'available': budget_info['remaining_epsilon'],
                'total': budget_info['total_epsilon']
            }, status='400 Bad Request')


# For backward compatibility
PrivacyBudget = PrivacyBudgetManager