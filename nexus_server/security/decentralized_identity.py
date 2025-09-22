"""
Decentralized Identity (DID) and Verifiable Credentials Integration

This module provides utilities for working with Decentralized Identifiers (DIDs)
and Verifiable Credentials, enabling self-sovereign identity for users.
"""

import json
import time
import hashlib
import base64
from typing import Dict, List, Optional, Any
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization


class DIDManager:
    """
    Manages Decentralized Identifiers (DIDs) and Verifiable Credentials.
    
    This class provides functionality for:
    1. Generating DID key pairs
    2. Creating and verifying DIDs
    3. Issuing and verifying verifiable credentials
    4. Managing DID documents
    """
    
    def __init__(self):
        self.dids = {}
        self.credentials = {}
        self.did_documents = {}
    
    def generate_did_keypair(self) -> Dict[str, str]:
        """
        Generate a new DID key pair for self-sovereign identity.
        
        Returns:
            Dictionary with private key, public key, and DID identifier
        """
        # Generate RSA key pair
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        public_key = private_key.public_key()
        
        # Serialize keys
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        # Create DID identifier (simplified for demo)
        public_key_hash = hashlib.sha256(public_pem).digest()
        did_identifier = f"did:nexus:{base64.urlsafe_b64encode(public_key_hash[:16]).decode()}"
        
        return {
            'private_key': private_pem.decode(),
            'public_key': public_pem.decode(),
            'did': did_identifier
        }
    
    def create_did_document(self, did: str, public_key: str) -> Dict[str, Any]:
        """
        Create a DID document for a given DID.
        
        Args:
            did: The DID identifier
            public_key: The public key in PEM format
            
        Returns:
            DID document as dictionary
        """
        did_document = {
            "@context": [
                "https://www.w3.org/ns/did/v1",
                "https://w3id.org/security/suites/jws-2020/v1"
            ],
            "id": did,
            "verificationMethod": [{
                "id": f"{did}#key-1",
                "type": "JsonWebKey2020",
                "controller": did,
                "publicKeyJwk": self._public_key_to_jwk(public_key)
            }],
            "authentication": [f"{did}#key-1"],
            "assertionMethod": [f"{did}#key-1"]
        }
        
        self.did_documents[did] = did_document
        return did_document
    
    def _public_key_to_jwk(self, public_key_pem: str) -> Dict[str, Any]:
        """
        Convert PEM public key to JWK format (simplified).
        
        Args:
            public_key_pem: Public key in PEM format
            
        Returns:
            JWK representation of the public key
        """
        # This is a simplified implementation for demo purposes
        # In a real implementation, you would parse the actual key components
        return {
            "kty": "RSA",
            "alg": "RS256",
            "use": "sig"
        }
    
    def issue_verifiable_credential(self, issuer_did: str, subject_did: str, 
                                  claims: Dict[str, Any], expiration_days: int = 365) -> Dict[str, Any]:
        """
        Issue a verifiable credential to a subject.
        
        Args:
            issuer_did: DID of the credential issuer
            subject_did: DID of the credential subject
            claims: Claims about the subject
            expiration_days: Number of days until credential expires
            
        Returns:
            Verifiable credential as dictionary
        """
        credential = {
            "@context": [
                "https://www.w3.org/2018/credentials/v1",
                "https://www.w3.org/2018/credentials/examples/v1"
            ],
            "id": f"urn:uuid:{hashlib.md5(f'{issuer_did}{subject_did}{time.time()}'.encode()).hexdigest()}",
            "type": ["VerifiableCredential", "PersonalIdentityCredential"],
            "issuer": issuer_did,
            "issuanceDate": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "expirationDate": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", 
                time.gmtime(time.time() + expiration_days * 24 * 60 * 60)
            ),
            "credentialSubject": {
                "id": subject_did,
                **claims
            }
        }
        
        # In a real implementation, you would sign the credential
        # For this demo, we'll just store it
        cred_id = credential["id"]
        self.credentials[cred_id] = credential
        
        return credential
    
    def verify_credential(self, credential: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify a verifiable credential.
        
        Args:
            credential: The credential to verify
            
        Returns:
            Verification result
        """
        # Check if credential exists
        cred_id = credential.get("id")
        if cred_id not in self.credentials:
            return {
                "valid": False,
                "error": "Credential not found or has been revoked"
            }
        
        # Check expiration
        exp_date = credential.get("expirationDate")
        if exp_date:
            exp_timestamp = time.mktime(time.strptime(exp_date, "%Y-%m-%dT%H:%M:%SZ"))
            if time.time() > exp_timestamp:
                return {
                    "valid": False,
                    "error": "Credential has expired"
                }
        
        # In a real implementation, you would verify the signature
        # For this demo, we'll just return success
        return {
            "valid": True,
            "verified_by": "nexus_demo",
            "verification_date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
    
    def get_did_document(self, did: str) -> Optional[Dict[str, Any]]:
        """
        Get the DID document for a given DID.
        
        Args:
            did: The DID identifier
            
        Returns:
            DID document or None if not found
        """
        return self.did_documents.get(did)
    
    def revoke_credential(self, credential_id: str) -> bool:
        """
        Revoke a verifiable credential.
        
        Args:
            credential_id: ID of the credential to revoke
            
        Returns:
            True if revoked, False if not found
        """
        if credential_id in self.credentials:
            del self.credentials[credential_id]
            return True
        return False


# Global instance for the application
did_manager = DIDManager()


def add_decentralized_identity_routes():
    """
    Add decentralized identity API routes.
    """
    from ..server import route, json_response
    from ..utils.validation import validate_json
    
    @route('/api/did/generate')
    def generate_did_handler(request):
        """
        Generate a new DID key pair.
        """
        try:
            keypair = did_manager.generate_did_keypair()
            
            return json_response({
                'message': 'DID keypair generated successfully',
                'did': keypair['did'],
                'public_key': keypair['public_key'],
                'instructions': 'Store your private key securely. It cannot be recovered.'
            })
        except Exception as e:
            return json_response({
                'error': f'Failed to generate DID: {str(e)}'
            }, status='400 Bad Request')
    
    @route('/api/did/document')
    @validate_json({
        'did': {'type': 'string', 'required': True},
        'public_key': {'type': 'string', 'required': True}
    })
    def create_did_document_handler(request):
        """
        Create a DID document.
        """
        try:
            did = request.data['did']
            public_key = request.data['public_key']
            
            did_document = did_manager.create_did_document(did, public_key)
            
            return json_response({
                'message': 'DID document created successfully',
                'did_document': did_document
            })
        except Exception as e:
            return json_response({
                'error': f'Failed to create DID document: {str(e)}'
            }, status='400 Bad Request')
    
    @route('/api/did/credential/issue')
    @validate_json({
        'issuer_did': {'type': 'string', 'required': True},
        'subject_did': {'type': 'string', 'required': True},
        'claims': {'type': 'dict', 'required': True},
        'expiration_days': {'type': 'integer', 'required': False, 'default': 365}
    })
    def issue_credential_handler(request):
        """
        Issue a verifiable credential.
        """
        try:
            issuer_did = request.data['issuer_did']
            subject_did = request.data['subject_did']
            claims = request.data['claims']
            expiration_days = request.data.get('expiration_days', 365)
            
            credential = did_manager.issue_verifiable_credential(
                issuer_did, subject_did, claims, expiration_days
            )
            
            return json_response({
                'message': 'Verifiable credential issued successfully',
                'credential': credential
            })
        except Exception as e:
            return json_response({
                'error': f'Failed to issue credential: {str(e)}'
            }, status='400 Bad Request')
    
    @route('/api/did/credential/verify')
    @validate_json({
        'credential': {'type': 'dict', 'required': True}
    })
    def verify_credential_handler(request):
        """
        Verify a verifiable credential.
        """
        try:
            credential = request.data['credential']
            
            verification_result = did_manager.verify_credential(credential)
            
            return json_response({
                'verification_result': verification_result
            })
        except Exception as e:
            return json_response({
                'error': f'Failed to verify credential: {str(e)}'
            }, status='400 Bad Request')
    
    @route('/api/did/document/<did>')
    def get_did_document_handler(request):
        """
        Get a DID document.
        """
        try:
            # Extract DID from path
            path_parts = request.path.split('/')
            did = path_parts[-1]
            
            did_document = did_manager.get_did_document(did)
            
            if did_document:
                return json_response({
                    'did_document': did_document
                })
            else:
                return json_response({
                    'error': 'DID document not found'
                }, status='404 Not Found')
        except Exception as e:
            return json_response({
                'error': f'Failed to retrieve DID document: {str(e)}'
            }, status='400 Bad Request')


# For backward compatibility
DecentralizedIdentity = DIDManager