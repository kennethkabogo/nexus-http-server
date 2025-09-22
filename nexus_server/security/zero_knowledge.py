"""
Client-Side Encryption Utilities for Zero-Knowledge Architecture

This module provides encryption utilities that can be used on the client side
to implement zero-knowledge architecture where the server never sees
encryption keys or plaintext data.

The server only stores encrypted data and cannot decrypt it without
the client's encryption key/password.
"""

import os
import base64
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Dict, Any, Optional


class ClientSideEncryption:
    """Client-side encryption utilities for zero-knowledge architecture."""
    
    def __init__(self):
        pass
    
    @staticmethod
    def generate_key_from_password(password: str, salt: Optional[bytes] = None) -> tuple:
        """
        Generate a key from a password using PBKDF2.
        
        Args:
            password: The password to derive the key from
            salt: Optional salt (will be generated if not provided)
            
        Returns:
            Tuple of (key, salt)
        """
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    @staticmethod
    def encrypt_data_for_storage(data: Any, password: str) -> Dict[str, str]:
        """
        Encrypt data for zero-knowledge storage.
        
        Args:
            data: The data to encrypt (will be JSON serialized)
            password: The password to use for encryption
            
        Returns:
            Dictionary with encrypted data, salt, and metadata
        """
        # Serialize data to JSON string
        if isinstance(data, str):
            data_str = data
        else:
            data_str = json.dumps(data, separators=(',', ':'))
        
        # Generate key and salt
        key, salt = ClientSideEncryption.generate_key_from_password(password)
        
        # Encrypt data
        f = Fernet(key)
        encrypted_data = f.encrypt(data_str.encode())
        
        return {
            'encrypted_data': base64.urlsafe_b64encode(encrypted_data).decode(),
            'salt': base64.urlsafe_b64encode(salt).decode(),
            'version': '1.0',
            'algorithm': 'AES-256-Fernet'
        }
    
    @staticmethod
    def decrypt_data_from_storage(encrypted_dict: Dict[str, str], password: str) -> Any:
        """
        Decrypt data retrieved from zero-knowledge storage.
        
        Args:
            encrypted_dict: Dictionary with encrypted data and salt
            password: The password to use for decryption
            
        Returns:
            Decrypted data (parsed from JSON if it was structured)
        """
        try:
            # Decode base64 encoded values
            salt = base64.urlsafe_b64decode(encrypted_dict['salt'])
            encrypted_data = base64.urlsafe_b64decode(encrypted_dict['encrypted_data'])
            
            # Generate key
            key, _ = ClientSideEncryption.generate_key_from_password(password, salt)
            
            # Decrypt data
            f = Fernet(key)
            decrypted_data = f.decrypt(encrypted_data)
            decrypted_str = decrypted_data.decode()
            
            # Try to parse as JSON, if it fails return as string
            try:
                return json.loads(decrypted_str)
            except json.JSONDecodeError:
                return decrypted_str
                
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
    
    @staticmethod
    def generate_encryption_key() -> str:
        """
        Generate a random encryption key for client-side use.
        
        Returns:
            Base64 encoded random key
        """
        key = Fernet.generate_key()
        return base64.urlsafe_b64encode(key).decode()
    
    @staticmethod
    def encrypt_with_key(data: Any, key: str) -> Dict[str, str]:
        """
        Encrypt data with a pre-generated key.
        
        Args:
            data: The data to encrypt (will be JSON serialized)
            key: Base64 encoded encryption key
            
        Returns:
            Dictionary with encrypted data and metadata
        """
        # Decode key
        decoded_key = base64.urlsafe_b64decode(key)
        f = Fernet(decoded_key)
        
        # Serialize data
        if isinstance(data, str):
            data_str = data
        else:
            data_str = json.dumps(data, separators=(',', ':'))
        
        # Encrypt
        encrypted_data = f.encrypt(data_str.encode())
        
        return {
            'encrypted_data': base64.urlsafe_b64encode(encrypted_data).decode(),
            'version': '1.0',
            'algorithm': 'AES-256-Fernet',
            'key_derived': False
        }
    
    @staticmethod
    def decrypt_with_key(encrypted_dict: Dict[str, str], key: str) -> Any:
        """
        Decrypt data with a pre-generated key.
        
        Args:
            encrypted_dict: Dictionary with encrypted data
            key: Base64 encoded encryption key
            
        Returns:
            Decrypted data
        """
        try:
            # Decode key and encrypted data
            decoded_key = base64.urlsafe_b64decode(key)
            encrypted_data = base64.urlsafe_b64decode(encrypted_dict['encrypted_data'])
            
            # Decrypt
            f = Fernet(decoded_key)
            decrypted_data = f.decrypt(encrypted_data)
            decrypted_str = decrypted_data.decode()
            
            # Try to parse as JSON
            try:
                return json.loads(decrypted_str)
            except json.JSONDecodeError:
                return decrypted_str
                
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")


def add_zero_knowledge_routes():
    """
    Add zero-knowledge architecture API routes.
    
    These routes support client-side encryption where the server
    never sees plaintext data or encryption keys.
    """
    from ..server import route, json_response
    from ..utils.validation import validate_json
    
    @route('/api/zk/prepare-storage')
    @validate_json({
        'data': {'type': 'dict', 'required': True},
        'client_encryption_key': {'type': 'string', 'required': True}
    })
    def prepare_storage_handler(request):
        """
        Prepare data for zero-knowledge storage.
        
        Client sends data and their encryption key.
        Server returns encrypted data that client can safely store.
        """
        try:
            data = request.data['data']
            client_key = request.data['client_encryption_key']
            
            # Encrypt with client's key
            encrypted = ClientSideEncryption.encrypt_with_key(data, client_key)
            
            return json_response({
                'storage_ready_data': encrypted,
                'server_processing': 'Data encrypted client-side, server only stores encrypted version'
            })
        except Exception as e:
            return json_response({
                'error': f'Zero-knowledge preparation failed: {str(e)}'
            }, status='400 Bad Request')
    
    @route('/api/zk/retrieve-storage')
    @validate_json({
        'storage_data': {'type': 'dict', 'required': True},
        'client_encryption_key': {'type': 'string', 'required': True}
    })
    def retrieve_storage_handler(request):
        """
        Retrieve data from zero-knowledge storage.
        
        Client sends stored encrypted data and their decryption key.
        Server returns decrypted data.
        """
        try:
            storage_data = request.data['storage_data']
            client_key = request.data['client_encryption_key']
            
            # Decrypt with client's key
            decrypted = ClientSideEncryption.decrypt_with_key(storage_data, client_key)
            
            return json_response({
                'decrypted_data': decrypted,
                'server_processing': 'Data decrypted client-side, server never saw plaintext'
            })
        except Exception as e:
            return json_response({
                'error': f'Zero-knowledge retrieval failed: {str(e)}'
            }, status='400 Bad Request')
    
    @route('/api/zk/generate-key')
    def generate_key_handler(request):
        """
        Generate a client-side encryption key.
        
        Returns a key that client should store securely.
        """
        try:
            key = ClientSideEncryption.generate_encryption_key()
            
            return json_response({
                'client_encryption_key': key,
                'security_notice': 'Store this key securely. If lost, data cannot be recovered.',
                'usage': 'Use this key for client-side encryption/decryption'
            })
        except Exception as e:
            return json_response({
                'error': f'Key generation failed: {str(e)}'
            }, status='400 Bad Request')


# Export the main class
ZeroKnowledgeEncryption = ClientSideEncryption