"""
AI Training Data Opt-Out and Privacy Headers

This module provides utilities for opting out of AI training data harvesting
and adding privacy-preserving headers to HTTP responses.
"""

import time
from typing import Dict, List, Optional, Any
from collections import defaultdict


class AIPrivacyManager:
    """
    Manages AI training data opt-out and privacy-preserving headers.
    
    This class provides functionality for:
    1. Adding AI training opt-out headers
    2. Managing AI data harvesting preferences
    3. Tracking AI model training requests
    4. Providing AI privacy controls
    """
    
    def __init__(self):
        self.ai_opt_out_preferences = defaultdict(dict)
        self.ai_training_requests = []
        self.model_training_jobs = {}
    
    def set_ai_opt_out(self, user_id: str, opt_out: bool = True) -> Dict[str, Any]:
        """
        Set AI training data opt-out preference for a user.
        
        Args:
            user_id: Unique identifier for the user
            opt_out: Whether to opt out of AI training (default True)
            
        Returns:
            Confirmation of opt-out status
        """
        self.ai_opt_out_preferences[user_id] = {
            'opt_out': opt_out,
            'set_at': time.time(),
            'user_id': user_id
        }
        
        status = "opted out" if opt_out else "opted in"
        return {
            'message': f'User {user_id} has {status} of AI training data harvesting',
            'opt_out': opt_out,
            'timestamp': time.time()
        }
    
    def is_ai_opt_out(self, user_id: str) -> bool:
        """
        Check if a user has opted out of AI training data harvesting.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            True if user has opted out, False otherwise
        """
        preference = self.ai_opt_out_preferences.get(user_id, {})
        return preference.get('opt_out', False)
    
    def get_ai_opt_out_status(self, user_id: str) -> Dict[str, Any]:
        """
        Get AI training data opt-out status for a user.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Opt-out status information
        """
        preference = self.ai_opt_out_preferences.get(user_id, {})
        opt_out = preference.get('opt_out', False)
        
        return {
            'user_id': user_id,
            'opt_out': opt_out,
            'set_at': preference.get('set_at', None),
            'status': 'opted_out' if opt_out else 'opted_in'
        }
    
    def add_ai_privacy_headers(self, headers: List[tuple]) -> List[tuple]:
        """
        Add AI privacy headers to HTTP response headers.
        
        Args:
            headers: Existing HTTP response headers
            
        Returns:
            Updated headers with AI privacy headers added
        """
        ai_headers = [
            # Opt-out of AI training
            ('X-AI-Training-Opt-Out', 'true'),
            # No AI model training on this data
            ('X-No-AI-Model-Training', 'true'),
            # Data should not be used for machine learning
            ('X-No-Machine-Learning', 'true'),
            # Request that AI systems respect privacy
            ('X-AI-Respect-Privacy', 'true'),
            # Do Not Train header (emerging standard)
            ('X-Do-Not-Train', 'true'),
            # Do Not Profile header
            ('X-Do-Not-Profile', 'true')
        ]
        
        # Add the AI privacy headers to the existing headers
        updated_headers = headers.copy()
        updated_headers.extend(ai_headers)
        
        return updated_headers
    
    def log_ai_training_request(self, request_info: Dict[str, Any]) -> str:
        """
        Log an AI model training request for auditing.
        
        Args:
            request_info: Information about the AI training request
            
        Returns:
            Request ID for tracking
        """
        request_id = f"ai_train_{int(time.time() * 1000000)}"
        request_log = {
            'request_id': request_id,
            'timestamp': time.time(),
            'request_info': request_info
        }
        
        self.ai_training_requests.append(request_log)
        return request_id
    
    def start_model_training_job(self, job_id: str, model_type: str, 
                               data_sources: List[str]) -> Dict[str, Any]:
        """
        Start an AI model training job with privacy controls.
        
        Args:
            job_id: Unique identifier for the training job
            model_type: Type of model being trained
            data_sources: List of data sources for training
            
        Returns:
            Training job information
        """
        # Check if any data sources have AI opt-out
        opted_out_sources = []
        for source in data_sources:
            # In a real implementation, you would check actual user preferences
            # For this demo, we'll simulate checking
            if source.startswith("user_") and self.is_ai_opt_out(source):
                opted_out_sources.append(source)
        
        job_info = {
            'job_id': job_id,
            'model_type': model_type,
            'data_sources': data_sources,
            'opted_out_sources': opted_out_sources,
            'excluded_sources': len(opted_out_sources),
            'included_sources': len(data_sources) - len(opted_out_sources),
            'started_at': time.time(),
            'status': 'running' if not opted_out_sources else 'partially_running'
        }
        
        self.model_training_jobs[job_id] = job_info
        return job_info
    
    def get_ai_training_jobs(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all AI training jobs.
        
        Returns:
            Dictionary of training jobs
        """
        return self.model_training_jobs.copy()
    
    def get_ai_privacy_report(self, user_id: str) -> Dict[str, Any]:
        """
        Get AI privacy report for a user.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            AI privacy report
        """
        opt_out_status = self.get_ai_opt_out_status(user_id)
        
        # In a real implementation, you would track actual AI usage
        # For this demo, we'll provide a sample report
        report = {
            'user_id': user_id,
            'opt_out_status': opt_out_status,
            'ai_interactions': {
                'data_scraping_attempts': 0,
                'model_training_inclusion': 0,
                'profile_building_attempts': 0
            },
            'protection_status': 'active' if opt_out_status['opt_out'] else 'inactive',
            'report_generated_at': time.time()
        }
        
        return report


# Global instance for the application
ai_privacy_manager = AIPrivacyManager()


def add_ai_privacy_middleware(handler):
    """
    Middleware to add AI privacy headers to all responses.
    """
    def middleware_handler(request):
        response = handler(request)
        
        # Add AI privacy headers to all responses
        if hasattr(response, 'headers'):
            ai_privacy_manager.add_ai_privacy_headers(response.headers)
        
        return response
    return middleware_handler


def add_ai_privacy_routes():
    """
    Add AI privacy API routes.
    """
    from ..server import route, json_response
    from ..utils.validation import validate_json
    
    @route('/api/ai/opt-out')
    @validate_json({
        'opt_out': {'type': 'boolean', 'required': False, 'default': True}
    })
    def set_ai_opt_out_handler(request):
        """
        Set AI training data opt-out preference.
        """
        try:
            # Get user from authentication (simplified)
            user = getattr(request, 'user', None)
            if user is not None:
                user_id = user.get('user_id', 'anonymous')
            else:
                user_id = 'anonymous'
            
            opt_out = request.data.get('opt_out', True)
            
            result = ai_privacy_manager.set_ai_opt_out(user_id, opt_out)
            
            return json_response(result)
        except Exception as e:
            return json_response({
                'error': f'Failed to set AI opt-out preference: {str(e)}'
            }, status='400 Bad Request')
    
    @route('/api/ai/opt-out/status')
    def get_ai_opt_out_status_handler(request):
        """
        Get AI training data opt-out status.
        """
        try:
            # Get user from authentication (simplified)
            user = getattr(request, 'user', None)
            if user is not None:
                user_id = user.get('user_id', 'anonymous')
            else:
                user_id = 'anonymous'
            
            status = ai_privacy_manager.get_ai_opt_out_status(user_id)
            
            return json_response(status)
        except Exception as e:
            return json_response({
                'error': f'Failed to get AI opt-out status: {str(e)}'
            }, status='400 Bad Request')
    
    @route('/api/ai/training-job')
    @validate_json({
        'job_id': {'type': 'string', 'required': True},
        'model_type': {'type': 'string', 'required': True},
        'data_sources': {'type': 'list', 'required': True}
    })
    def start_training_job_handler(request):
        """
        Start an AI model training job with privacy controls.
        """
        try:
            job_id = request.data['job_id']
            model_type = request.data['model_type']
            data_sources = request.data['data_sources']
            
            job_info = ai_privacy_manager.start_model_training_job(
                job_id, model_type, data_sources
            )
            
            return json_response({
                'message': 'AI training job started with privacy controls',
                'job_info': job_info
            })
        except Exception as e:
            return json_response({
                'error': f'Failed to start AI training job: {str(e)}'
            }, status='400 Bad Request')
    
    @route('/api/ai/training-jobs')
    def get_training_jobs_handler(request):
        """
        Get information about all AI training jobs.
        """
        try:
            jobs = ai_privacy_manager.get_ai_training_jobs()
            
            return json_response({
                'training_jobs': jobs
            })
        except Exception as e:
            return json_response({
                'error': f'Failed to get AI training jobs: {str(e)}'
            }, status='400 Bad Request')
    
    @route('/api/ai/privacy-report')
    def get_ai_privacy_report_handler(request):
        """
        Get AI privacy report for the authenticated user.
        """
        try:
            # Get user from authentication (simplified)
            user = getattr(request, 'user', None)
            if user is not None:
                user_id = user.get('user_id', 'anonymous')
            else:
                user_id = 'anonymous'
            
            report = ai_privacy_manager.get_ai_privacy_report(user_id)
            
            return json_response(report)
        except Exception as e:
            return json_response({
                'error': f'Failed to generate AI privacy report: {str(e)}'
            }, status='400 Bad Request')


# For backward compatibility
AIPrivacy = AIPrivacyManager