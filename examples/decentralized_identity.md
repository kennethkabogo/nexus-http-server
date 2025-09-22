# Decentralized Identity Example

This example demonstrates how to use the decentralized identity features of Nexus HTTP Server.

## Overview

Decentralized identity (DID) allows users to have self-sovereign identity without relying on centralized identity providers. This example shows how to generate DIDs, create DID documents, and issue verifiable credentials.

## Python Client Example

```python
import requests
import json

# Server URL
BASE_URL = "http://localhost:8000"

def generate_did():
    """Generate a new DID key pair."""
    response = requests.get(f"{BASE_URL}/api/did/generate")
    return response.json()

def create_did_document(did, public_key):
    """Create a DID document."""
    response = requests.post(
        f"{BASE_URL}/api/did/document",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "did": did,
            "public_key": public_key
        })
    )
    return response.json()

def issue_credential(issuer_did, subject_did, claims):
    """Issue a verifiable credential."""
    response = requests.post(
        f"{BASE_URL}/api/did/credential/issue",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "issuer_did": issuer_did,
            "subject_did": subject_did,
            "claims": claims
        })
    )
    return response.json()

def verify_credential(credential):
    """Verify a verifiable credential."""
    response = requests.post(
        f"{BASE_URL}/api/did/credential/verify",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "credential": credential
        })
    )
    return response.json()

def get_did_document(did):
    """Get a DID document."""
    response = requests.get(f"{BASE_URL}/api/did/document/{did}")
    return response.json()

# Example usage
if __name__ == "__main__":
    # Generate a DID for the issuer
    issuer_result = generate_did()
    print(f"Issuer DID generated: {issuer_result}")
    
    issuer_did = issuer_result['did']
    issuer_public_key = issuer_result['public_key']
    
    # Create DID document for issuer
    issuer_doc = create_did_document(issuer_did, issuer_public_key)
    print(f"Issuer DID document: {issuer_doc}")
    
    # Generate a DID for the subject
    subject_result = generate_did()
    print(f"Subject DID generated: {subject_result}")
    
    subject_did = subject_result['did']
    subject_public_key = subject_result['public_key']
    
    # Create DID document for subject
    subject_doc = create_did_document(subject_did, subject_public_key)
    print(f"Subject DID document: {subject_doc}")
    
    # Issue a verifiable credential
    claims = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30,
        "nationality": "US"
    }
    
    credential_result = issue_credential(issuer_did, subject_did, claims)
    print(f"Verifiable credential issued: {credential_result}")
    
    # Verify the credential
    credential = credential_result['credential']
    verification_result = verify_credential(credential)
    print(f"Credential verification: {verification_result}")
    
    # Get DID document
    did_doc = get_did_document(subject_did)
    print(f"Retrieved DID document: {did_doc}")
```

## JavaScript Client Example

```javascript
// Example usage of decentralized identity endpoints

const BASE_URL = 'http://localhost:8000';

async function generateDID() {
  const response = await fetch(`${BASE_URL}/api/did/generate`);
  return response.json();
}

async function createDIDDocument(did, publicKey) {
  const response = await fetch(`${BASE_URL}/api/did/document`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ did, public_key: publicKey }),
  });
  return response.json();
}

async function issueCredential(issuerDID, subjectDID, claims) {
  const response = await fetch(`${BASE_URL}/api/did/credential/issue`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ issuer_did: issuerDID, subject_did: subjectDID, claims }),
  });
  return response.json();
}

async function verifyCredential(credential) {
  const response = await fetch(`${BASE_URL}/api/did/credential/verify`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ credential }),
  });
  return response.json();
}

async function getDIDDocument(did) {
  const response = await fetch(`${BASE_URL}/api/did/document/${did}`);
  return response.json();
}

// Example usage
(async () => {
  try {
    // Generate a DID for the issuer
    const issuerResult = await generateDID();
    console.log('Issuer DID generated:', issuerResult);
    
    const issuerDID = issuerResult.did;
    const issuerPublicKey = issuerResult.public_key;
    
    // Create DID document for issuer
    const issuerDoc = await createDIDDocument(issuerDID, issuerPublicKey);
    console.log('Issuer DID document:', issuerDoc);
    
    // Generate a DID for the subject
    const subjectResult = await generateDID();
    console.log('Subject DID generated:', subjectResult);
    
    const subjectDID = subjectResult.did;
    const subjectPublicKey = subjectResult.public_key;
    
    // Create DID document for subject
    const subjectDoc = await createDIDDocument(subjectDID, subjectPublicKey);
    console.log('Subject DID document:', subjectDoc);
    
    // Issue a verifiable credential
    const claims = {
      name: "John Doe",
      email: "john.doe@example.com",
      age: 30,
      nationality: "US"
    };
    
    const credentialResult = await issueCredential(issuerDID, subjectDID, claims);
    console.log('Verifiable credential issued:', credentialResult);
    
    // Verify the credential
    const credential = credentialResult.credential;
    const verificationResult = await verifyCredential(credential);
    console.log('Credential verification:', verificationResult);
    
    // Get DID document
    const didDoc = await getDIDDocument(subjectDID);
    console.log('Retrieved DID document:', didDoc);
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

## cURL Examples

### Generate a DID

```bash
# Generate a new DID key pair
curl http://localhost:8000/api/did/generate
```

### Create a DID Document

```bash
# Create a DID document
curl -X POST http://localhost:8000/api/did/document \
  -H "Content-Type: application/json" \
  -d '{
    "did": "did:nexus:example",
    "public_key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA..."
  }'
```

### Issue a Verifiable Credential

```bash
# Issue a verifiable credential
curl -X POST http://localhost:8000/api/did/credential/issue \
  -H "Content-Type: application/json" \
  -d '{
    "issuer_did": "did:nexus:issuer123",
    "subject_did": "did:nexus:subject456",
    "claims": {
      "name": "John Doe",
      "email": "john.doe@example.com",
      "age": 30
    }
  }'
```

### Verify a Verifiable Credential

```bash
# Verify a verifiable credential
curl -X POST http://localhost:8000/api/did/credential/verify \
  -H "Content-Type: application/json" \
  -d '{
    "credential": {
      "@context": ["https://www.w3.org/2018/credentials/v1"],
      "id": "urn:uuid:example",
      "type": ["VerifiableCredential"],
      "issuer": "did:nexus:issuer123",
      "issuanceDate": "2023-01-01T00:00:00Z",
      "credentialSubject": {
        "id": "did:nexus:subject456",
        "name": "John Doe"
      }
    }
  }'
```

### Get a DID Document

```bash
# Get a DID document
curl http://localhost:8000/api/did/document/did:nexus:example
```

## Best Practices

1. **Secure Key Storage**: Store private keys securely and never expose them
2. **DID Rotation**: Rotate DIDs periodically for enhanced security
3. **Credential Expiration**: Set appropriate expiration dates for credentials
4. **Revocation Mechanisms**: Implement credential revocation when necessary
5. **Audit Trails**: Keep logs of DID and credential operations
6. **Standards Compliance**: Follow W3C DID and Verifiable Credentials standards