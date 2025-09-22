"""
Lightweight encryption utilities for privacy-focused applications.
"""
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_key_from_password(password: str, salt: bytes = None) -> tuple:
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


def encrypt_data(data: str, password: str) -> dict:
    """
    Encrypt data with a password.
    
    Args:
        data: The data to encrypt
        password: The password to use for encryption
        
    Returns:
        Dictionary with encrypted data and salt
    """
    key, salt = generate_key_from_password(password)
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    
    return {
        'data': base64.urlsafe_b64encode(encrypted_data).decode(),
        'salt': base64.urlsafe_b64encode(salt).decode()
    }


def decrypt_data(encrypted_dict: dict, password: str) -> str:
    """
    Decrypt data with a password.
    
    Args:
        encrypted_dict: Dictionary with encrypted data and salt
        password: The password to use for decryption
        
    Returns:
        Decrypted data as string
    """
    salt = base64.urlsafe_b64decode(encrypted_dict['salt'])
    key, _ = generate_key_from_password(password, salt)
    f = Fernet(key)
    encrypted_data = base64.urlsafe_b64decode(encrypted_dict['data'])
    decrypted_data = f.decrypt(encrypted_data)
    
    return decrypted_data.decode()


def add_encryption_routes():
    """
    Add encryption-related API routes.
    """
    from ..server import route, json_response
    from ..utils.validation import validate_json
    
    @route('/api/encrypt')
    @validate_json({
        'data': {'type': 'string', 'required': True},
        'password': {'type': 'string', 'required': True}
    })
    def encrypt_handler(request):
        try:
            encrypted = encrypt_data(
                request.data['data'], 
                request.data['password']
            )
            return json_response({
                'encrypted_data': encrypted['data'],
                'salt': encrypted['salt']
            })
        except Exception as e:
            return json_response({
                'error': f'Encryption failed: {str(e)}'
            }, status='400 Bad Request')
    
    @route('/api/decrypt')
    @validate_json({
        'encrypted_data': {'type': 'string', 'required': True},
        'salt': {'type': 'string', 'required': True},
        'password': {'type': 'string', 'required': True}
    })
    def decrypt_handler(request):
        try:
            encrypted_dict = {
                'data': request.data['encrypted_data'],
                'salt': request.data['salt']
            }
            decrypted = decrypt_data(encrypted_dict, request.data['password'])
            return json_response({'decrypted_data': decrypted})
        except Exception as e:
            return json_response({
                'error': f'Decryption failed: {str(e)}'
            }, status='400 Bad Request')