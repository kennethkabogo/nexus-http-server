"""
Federated Learning Utilities for Privacy-Preserving Machine Learning

This module provides utilities for implementing federated learning,
where machine learning models are trained across decentralized devices
without sharing raw data.
"""

import json
import time
from typing import Dict, List, Any
from collections import defaultdict


class FederatedLearningCoordinator:
    """
    Coordinates federated learning rounds across multiple clients.
    
    This class manages the federated learning process where:
    1. Server sends global model to clients
    2. Clients train on local data and send updates
    3. Server aggregates updates to improve global model
    4. Process repeats for multiple rounds
    """
    
    def __init__(self):
        self.global_model = {}
        self.client_updates = defaultdict(list)
        self.round_history = []
        self.client_participation = defaultdict(int)
        
    def initialize_model(self, model_structure: Dict[str, Any]) -> None:
        """
        Initialize the global model with a structure.
        
        Args:
            model_structure: Dictionary representing model structure
        """
        self.global_model = model_structure.copy()
        
    def start_training_round(self, round_id: str) -> Dict[str, Any]:
        """
        Start a new federated learning round.
        
        Args:
            round_id: Unique identifier for this training round
            
        Returns:
            Dictionary with global model and round information
        """
        round_info = {
            'round_id': round_id,
            'global_model': self.global_model,
            'started_at': time.time(),
            'status': 'active'
        }
        
        self.round_history.append(round_info)
        return round_info
        
    def submit_client_update(self, client_id: str, round_id: str, 
                           model_update: Dict[str, Any]) -> bool:
        """
        Submit a client's model update for a training round.
        
        Args:
            client_id: Unique identifier for the client
            round_id: Identifier for the training round
            model_update: Client's model update (gradients, weights, etc.)
            
        Returns:
            True if update was accepted, False otherwise
        """
        # Validate that the round exists and is active
        round_info = None
        for r in self.round_history:
            if r['round_id'] == round_id and r['status'] == 'active':
                round_info = r
                break
                
        if not round_info:
            return False
            
        # Store the client update
        update_record = {
            'client_id': client_id,
            'timestamp': time.time(),
            'model_update': model_update
        }
        
        self.client_updates[round_id].append(update_record)
        self.client_participation[client_id] += 1
        return True
        
    def aggregate_updates(self, round_id: str, aggregation_method: str = 'fedavg') -> Dict[str, Any]:
        """
        Aggregate client updates to improve the global model.
        
        Args:
            round_id: Identifier for the training round
            aggregation_method: Method to use for aggregation ('fedavg', 'fedavg_weighted')
            
        Returns:
            Updated global model
        """
        updates = self.client_updates.get(round_id, [])
        if not updates:
            return self.global_model
            
        # Find the round info and mark it as completed
        round_info = None
        for r in self.round_history:
            if r['round_id'] == round_id:
                r['status'] = 'completed'
                r['completed_at'] = time.time()
                r['participant_count'] = len(updates)
                round_info = r
                break
                
        if aggregation_method == 'fedavg':
            # Simple federated averaging
            aggregated_update = {}
            
            # Initialize with zeros
            if updates:
                sample_update = updates[0]['model_update']
                for key in sample_update:
                    if isinstance(sample_update[key], (int, float)):
                        aggregated_update[key] = 0.0
                    elif isinstance(sample_update[key], list):
                        aggregated_update[key] = [0.0] * len(sample_update[key])
                        
            # Sum all updates
            for update in updates:
                client_update = update['model_update']
                for key in client_update:
                    if isinstance(client_update[key], (int, float)):
                        aggregated_update[key] += client_update[key]
                    elif isinstance(client_update[key], list):
                        for i, val in enumerate(client_update[key]):
                            aggregated_update[key][i] += val
                            
            # Average the updates
            num_clients = len(updates)
            for key in aggregated_update:
                if isinstance(aggregated_update[key], (int, float)):
                    aggregated_update[key] /= num_clients
                elif isinstance(aggregated_update[key], list):
                    for i in range(len(aggregated_update[key])):
                        aggregated_update[key][i] /= num_clients
                        
            # Update global model
            for key in aggregated_update:
                if key in self.global_model:
                    if isinstance(self.global_model[key], (int, float)):
                        self.global_model[key] += aggregated_update[key]
                    elif isinstance(self.global_model[key], list):
                        for i in range(len(self.global_model[key])):
                            self.global_model[key][i] += aggregated_update[key][i]
                            
        return self.global_model
        
    def get_round_status(self, round_id: str) -> Dict[str, Any]:
        """
        Get the status of a federated learning round.
        
        Args:
            round_id: Identifier for the training round
            
        Returns:
            Dictionary with round status information
        """
        for r in self.round_history:
            if r['round_id'] == round_id:
                return r
        return {'error': 'Round not found'}
        
    def get_client_statistics(self) -> Dict[str, int]:
        """
        Get statistics about client participation.
        
        Returns:
            Dictionary mapping client IDs to participation counts
        """
        return dict(self.client_participation)


# Global instance for the application
fl_coordinator = FederatedLearningCoordinator()


def add_federated_learning_routes():
    """
    Add federated learning API routes.
    """
    from ..server import route, json_response
    from ..utils.validation import validate_json
    
    @route('/api/fl/initialize')
    @validate_json({
        'model_structure': {'type': 'dict', 'required': True}
    })
    def initialize_model_handler(request):
        """
        Initialize the global federated learning model.
        """
        try:
            model_structure = request.data['model_structure']
            fl_coordinator.initialize_model(model_structure)
            
            return json_response({
                'message': 'Global model initialized successfully',
                'model_structure': model_structure
            })
        except Exception as e:
            return json_response({
                'error': f'Model initialization failed: {str(e)}'
            }, status='400 Bad Request')
    
    @route('/api/fl/start-round')
    @validate_json({
        'round_id': {'type': 'string', 'required': True}
    })
    def start_round_handler(request):
        """
        Start a new federated learning round.
        """
        try:
            round_id = request.data['round_id']
            round_info = fl_coordinator.start_training_round(round_id)
            
            return json_response({
                'message': f'Training round {round_id} started',
                'round_info': round_info
            })
        except Exception as e:
            return json_response({
                'error': f'Failed to start training round: {str(e)}'
            }, status='400 Bad Request')
    
    @route('/api/fl/submit-update')
    @validate_json({
        'client_id': {'type': 'string', 'required': True},
        'round_id': {'type': 'string', 'required': True},
        'model_update': {'type': 'dict', 'required': True}
    })
    def submit_update_handler(request):
        """
        Submit a client's model update for a training round.
        """
        try:
            client_id = request.data['client_id']
            round_id = request.data['round_id']
            model_update = request.data['model_update']
            
            success = fl_coordinator.submit_client_update(client_id, round_id, model_update)
            
            if success:
                return json_response({
                    'message': 'Model update submitted successfully',
                    'client_id': client_id,
                    'round_id': round_id
                })
            else:
                return json_response({
                    'error': 'Failed to submit model update - invalid round or round not active'
                }, status='400 Bad Request')
        except Exception as e:
            return json_response({
                'error': f'Failed to submit model update: {str(e)}'
            }, status='400 Bad Request')
    
    @route('/api/fl/aggregate')
    @validate_json({
        'round_id': {'type': 'string', 'required': True},
        'aggregation_method': {'type': 'string', 'required': False, 'default': 'fedavg'}
    })
    def aggregate_handler(request):
        """
        Aggregate client updates to improve the global model.
        """
        try:
            round_id = request.data['round_id']
            method = request.data.get('aggregation_method', 'fedavg')
            
            updated_model = fl_coordinator.aggregate_updates(round_id, method)
            
            return json_response({
                'message': f'Updates aggregated for round {round_id}',
                'updated_model': updated_model,
                'aggregation_method': method
            })
        except Exception as e:
            return json_response({
                'error': f'Failed to aggregate updates: {str(e)}'
            }, status='400 Bad Request')
    
    @route('/api/fl/round-status')
    @validate_json({
        'round_id': {'type': 'string', 'required': True}
    })
    def round_status_handler(request):
        """
        Get the status of a federated learning round.
        """
        try:
            round_id = request.data['round_id']
            status = fl_coordinator.get_round_status(round_id)
            
            return json_response({
                'round_id': round_id,
                'status': status
            })
        except Exception as e:
            return json_response({
                'error': f'Failed to get round status: {str(e)}'
            }, status='400 Bad Request')
    
    @route('/api/fl/client-stats')
    def client_stats_handler(request):
        """
        Get statistics about client participation.
        """
        try:
            stats = fl_coordinator.get_client_statistics()
            
            return json_response({
                'client_statistics': stats
            })
        except Exception as e:
            return json_response({
                'error': f'Failed to get client statistics: {str(e)}'
            }, status='400 Bad Request')