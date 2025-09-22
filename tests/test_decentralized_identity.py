"""
Unit tests for the decentralized identity module.
"""

import unittest
import time
from nexus_server.security.decentralized_identity import DIDManager


class TestDIDManager(unittest.TestCase):
    """Test cases for the DIDManager class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.did_manager = DIDManager()

    def test_generate_did_keypair(self):
        """Test generating a DID keypair."""
        keypair = self.did_manager.generate_did_keypair()
        
        self.assertIn('private_key', keypair)
        self.assertIn('public_key', keypair)
        self.assertIn('did', keypair)
        self.assertTrue(keypair['did'].startswith('did:nexus:'))
        self.assertIn('-----BEGIN PRIVATE KEY-----', keypair['private_key'])
        self.assertIn('-----BEGIN PUBLIC KEY-----', keypair['public_key'])

    def test_create_did_document(self):
        """Test creating a DID document."""
        # First generate a keypair
        keypair = self.did_manager.generate_did_keypair()
        did = keypair['did']
        public_key = keypair['public_key']
        
        # Create DID document
        did_document = self.did_manager.create_did_document(did, public_key)
        
        self.assertEqual(did_document['id'], did)
        self.assertIn('verificationMethod', did_document)
        self.assertIn('authentication', did_document)
        self.assertIn('assertionMethod', did_document)

    def test_issue_and_verify_credential(self):
        """Test issuing and verifying a verifiable credential."""
        # Create issuer and subject DIDs
        issuer_keypair = self.did_manager.generate_did_keypair()
        issuer_did = issuer_keypair['did']
        
        subject_keypair = self.did_manager.generate_did_keypair()
        subject_did = subject_keypair['did']
        
        # Issue credential
        claims = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'age': 30
        }
        
        credential = self.did_manager.issue_verifiable_credential(
            issuer_did, subject_did, claims
        )
        
        self.assertIn('id', credential)
        self.assertIn('type', credential)
        self.assertEqual(credential['issuer'], issuer_did)
        self.assertEqual(credential['credentialSubject']['id'], subject_did)
        self.assertEqual(credential['credentialSubject']['name'], 'John Doe')
        
        # Verify credential
        verification_result = self.did_manager.verify_credential(credential)
        self.assertTrue(verification_result['valid'])

    def test_verify_expired_credential(self):
        """Test verifying an expired credential."""
        # Create issuer and subject DIDs
        issuer_keypair = self.did_manager.generate_did_keypair()
        issuer_did = issuer_keypair['did']
        
        subject_keypair = self.did_manager.generate_did_keypair()
        subject_did = subject_keypair['did']
        
        # Issue credential with short expiration
        claims = {'name': 'John Doe'}
        
        credential = self.did_manager.issue_verifiable_credential(
            issuer_did, subject_did, claims, expiration_days=-1  # Expired
        )
        
        # Verify credential
        verification_result = self.did_manager.verify_credential(credential)
        self.assertFalse(verification_result['valid'])
        self.assertIn('expired', verification_result['error'])

    def test_revoke_credential(self):
        """Test revoking a credential."""
        # Create issuer and subject DIDs
        issuer_keypair = self.did_manager.generate_did_keypair()
        issuer_did = issuer_keypair['did']
        
        subject_keypair = self.did_manager.generate_did_keypair()
        subject_did = subject_keypair['did']
        
        # Issue credential
        claims = {'name': 'John Doe'}
        credential = self.did_manager.issue_verifiable_credential(
            issuer_did, subject_did, claims
        )
        
        # Revoke credential
        credential_id = credential['id']
        result = self.did_manager.revoke_credential(credential_id)
        self.assertTrue(result)
        
        # Try to verify revoked credential
        verification_result = self.did_manager.verify_credential(credential)
        self.assertFalse(verification_result['valid'])
        self.assertIn('not found', verification_result['error'])

    def test_get_did_document(self):
        """Test getting a DID document."""
        # Create a DID document
        keypair = self.did_manager.generate_did_keypair()
        did = keypair['did']
        public_key = keypair['public_key']
        
        self.did_manager.create_did_document(did, public_key)
        
        # Get the DID document
        did_document = self.did_manager.get_did_document(did)
        self.assertIsNotNone(did_document)
        self.assertEqual(did_document['id'], did)

    def test_get_nonexistent_did_document(self):
        """Test getting a non-existent DID document."""
        did_document = self.did_manager.get_did_document('did:nexus:nonexistent')
        self.assertIsNone(did_document)


if __name__ == '__main__':
    unittest.main()