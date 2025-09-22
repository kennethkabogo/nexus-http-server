"""
Data Expiration and Self-Destruction Features

This module provides utilities for automatically expiring and destroying data
after a specified time period, enhancing privacy by ensuring sensitive data
doesn't persist longer than necessary.
"""

import time
import threading
import json
from typing import Dict, Optional, Callable
from collections import defaultdict
from threading import Timer


class DataExpirationManager:
    """
    Manages automatic expiration and destruction of data.
    
    This class tracks data items with expiration times and automatically
    removes them when their time is up.
    """
    
    def __init__(self):
        # Store expiration information for data items
        self.expiring_data: Dict[str, Dict] = {}
        # Store destruction callbacks
        self.destruction_callbacks: Dict[str, Callable] = {}
        # Store timers for automatic cleanup
        self.timers: Dict[str, Timer] = {}
        # Lock for thread safety
        self.lock = threading.Lock()
    
    def set_data_expiration(self, data_id: str, ttl_seconds: int, 
                          destruction_callback: Optional[Callable] = None) -> bool:
        """
        Set an expiration time for a data item.
        
        Args:
            data_id: Unique identifier for the data item
            ttl_seconds: Time to live in seconds
            destruction_callback: Optional callback function to call when data is destroyed
            
        Returns:
            True if expiration was set successfully, False otherwise
        """
        with self.lock:
            expiration_time = time.time() + ttl_seconds
            
            self.expiring_data[data_id] = {
                'created_at': time.time(),
                'expires_at': expiration_time,
                'ttl_seconds': ttl_seconds
            }
            
            if destruction_callback:
                self.destruction_callbacks[data_id] = destruction_callback
            
            # Cancel any existing timer for this data_id
            if data_id in self.timers:
                self.timers[data_id].cancel()
            
            # Create a timer to automatically destroy the data
            timer = Timer(ttl_seconds, self._destroy_expired_data, [data_id])
            timer.daemon = True
            timer.start()
            self.timers[data_id] = timer
            
            return True
    
    def get_expiration_info(self, data_id: str) -> Optional[Dict]:
        """
        Get expiration information for a data item.
        
        Args:
            data_id: Unique identifier for the data item
            
        Returns:
            Dictionary with expiration information or None if not found
        """
        with self.lock:
            if data_id in self.expiring_data:
                info = self.expiring_data[data_id].copy()
                info['time_remaining'] = max(0, info['expires_at'] - time.time())
                info['is_expired'] = info['time_remaining'] <= 0
                return info
            return None
    
    def cancel_expiration(self, data_id: str) -> bool:
        """
        Cancel expiration for a data item.
        
        Args:
            data_id: Unique identifier for the data item
            
        Returns:
            True if expiration was canceled, False if data_id not found
        """
        with self.lock:
            if data_id in self.expiring_data:
                # Cancel the timer
                if data_id in self.timers:
                    self.timers[data_id].cancel()
                    del self.timers[data_id]
                
                # Remove from tracking
                del self.expiring_data[data_id]
                if data_id in self.destruction_callbacks:
                    del self.destruction_callbacks[data_id]
                
                return True
            return False
    
    def extend_expiration(self, data_id: str, additional_seconds: int) -> bool:
        """
        Extend the expiration time for a data item.
        
        Args:
            data_id: Unique identifier for the data item
            additional_seconds: Additional time to add to expiration
            
        Returns:
            True if expiration was extended, False if data_id not found
        """
        with self.lock:
            if data_id in self.expiring_data:
                # Cancel existing timer
                if data_id in self.timers:
                    self.timers[data_id].cancel()
                
                # Update expiration time
                self.expiring_data[data_id]['expires_at'] += additional_seconds
                self.expiring_data[data_id]['ttl_seconds'] += additional_seconds
                
                # Create new timer
                time_remaining = self.expiring_data[data_id]['expires_at'] - time.time()
                if time_remaining > 0:
                    timer = Timer(time_remaining, self._destroy_expired_data, [data_id])
                    timer.daemon = True
                    timer.start()
                    self.timers[data_id] = timer
                
                return True
            return False
    
    def get_all_expiring_data(self) -> Dict:
        """
        Get information about all expiring data items.
        
        Returns:
            Dictionary with information about all expiring data
        """
        with self.lock:
            result = {}
            current_time = time.time()
            
            for data_id, info in self.expiring_data.items():
                info_copy = info.copy()
                info_copy['time_remaining'] = max(0, info_copy['expires_at'] - current_time)
                info_copy['is_expired'] = info_copy['time_remaining'] <= 0
                result[data_id] = info_copy
            
            return result
    
    def _destroy_expired_data(self, data_id: str) -> None:
        """
        Internal method to destroy expired data.
        
        Args:
            data_id: Unique identifier for the data item
        """
        with self.lock:
            # Remove from tracking
            if data_id in self.expiring_data:
                del self.expiring_data[data_id]
            
            # Cancel timer
            if data_id in self.timers:
                del self.timers[data_id]
            
            # Call destruction callback if provided
            if data_id in self.destruction_callbacks:
                callback = self.destruction_callbacks[data_id]
                del self.destruction_callbacks[data_id]
                try:
                    callback(data_id)
                except Exception as e:
                    # Log error but don't let it stop the process
                    print(f"Error in destruction callback for {data_id}: {e}")


# Global instance for the application
data_expiration_manager = DataExpirationManager()


def secure_delete_data(data_id: str) -> None:
    """
    Securely delete data by overwriting it with zeros.
    
    This is a conceptual implementation. In a real system, you would
    need to work with the actual data storage mechanism.
    
    Args:
        data_id: Identifier for the data to delete
    """
    print(f"Securely deleting data: {data_id}")
    # In a real implementation, you would:
    # 1. Locate the actual data in storage
    # 2. Overwrite it with zeros or random data
    # 3. Remove references to it
    # 4. Trigger garbage collection if necessary


def add_data_expiration_routes():
    """
    Add data expiration and self-destruction API routes.
    """
    from ..server import route, json_response
    from ..utils.validation import validate_json
    
    @route('/api/data/expiration')
    def get_all_expiration_handler(request):
        """
        Get information about all expiring data items.
        """
        expiration_info = data_expiration_manager.get_all_expiring_data()
        return json_response({'expiring_data': expiration_info})
    
    @route('/api/data/expiration/<data_id>')
    def get_expiration_handler(request):
        """
        Get expiration information for a specific data item.
        """
        # Extract data_id from path (this is a simplified approach)
        # In a real implementation, you'd use proper routing
        data_id = request.path.split('/')[-1]
        
        expiration_info = data_expiration_manager.get_expiration_info(data_id)
        if expiration_info:
            return json_response(expiration_info)
        else:
            return json_response({
                'error': 'Data item not found or has no expiration set'
            }, status='404 Not Found')
    
    @route('/api/data/expiration/<data_id>/cancel')
    def cancel_expiration_handler(request):
        """
        Cancel expiration for a data item.
        """
        data_id = request.path.split('/')[-2]  # Get data_id from path
        
        success = data_expiration_manager.cancel_expiration(data_id)
        if success:
            return json_response({
                'message': f'Expiration canceled for data item {data_id}',
                'status': 'success'
            })
        else:
            return json_response({
                'error': 'Data item not found or has no expiration set'
            }, status='404 Not Found')
    
    @route('/api/data/expiration/<data_id>/extend')
    @validate_json({
        'additional_seconds': {'type': 'integer', 'required': True, 'min': 1}
    })
    def extend_expiration_handler(request):
        """
        Extend expiration time for a data item.
        """
        data_id = request.path.split('/')[-2]  # Get data_id from path
        additional_seconds = request.data['additional_seconds']
        
        success = data_expiration_manager.extend_expiration(data_id, additional_seconds)
        if success:
            expiration_info = data_expiration_manager.get_expiration_info(data_id)
            return json_response({
                'message': f'Expiration extended for data item {data_id}',
                'expiration_info': expiration_info,
                'status': 'success'
            })
        else:
            return json_response({
                'error': 'Data item not found or has no expiration set'
            }, status='404 Not Found')


# For backward compatibility
DataExpiration = DataExpirationManager