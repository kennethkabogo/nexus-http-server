# Zero-Knowledge Encryption Example

This example demonstrates how to use the zero-knowledge encryption features of Nexus HTTP Server.

## Client-Side Usage

The zero-knowledge architecture ensures that the server never sees plaintext data or encryption keys.

### JavaScript Client Example

```javascript
// Client-side encryption example
const BASE_URL = 'http://localhost:8000';

// Step 1: Generate a client-side encryption key
async function generateEncryptionKey() {
  const response = await fetch(`${BASE_URL}/api/zk/generate-key`);
  const data = await response.json();
  return data.client_encryption_key;
}

// Step 2: Prepare data for zero-knowledge storage
async function prepareForStorage(data, encryptionKey) {
  const response = await fetch(`${BASE_URL}/api/zk/prepare-storage`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      data: data,
      client_encryption_key: encryptionKey
    }),
  });
  return response.json();
}

// Step 3: Retrieve and decrypt data from storage
async function retrieveFromStorage(storageData, encryptionKey) {
  const response = await fetch(`${BASE_URL}/api/zk/retrieve-storage`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      storage_data: storageData,
      client_encryption_key: encryptionKey
    }),
  });
  return response.json();
}

// Example usage
(async () => {
  try {
    // Generate encryption key (client-side only)
    const encryptionKey = await generateEncryptionKey();
    console.log('Generated encryption key:', encryptionKey);
    
    // Sensitive data that should never be seen by the server
    const sensitiveData = {
      ssn: "123-45-6789",
      credit_card: "4111-1111-1111-1111",
      personal_notes: "This is my private information"
    };
    
    // Prepare data for storage (encrypted client-side)
    const storageReady = await prepareForStorage(sensitiveData, encryptionKey);
    console.log('Storage-ready encrypted data:', storageReady);
    
    // Store the encrypted data on the server
    // (In a real app, you would send this to your storage API)
    const serverStoredData = storageReady.storage_ready_data;
    
    // Later, retrieve and decrypt the data
    const retrieved = await retrieveFromStorage(serverStoredData, encryptionKey);
    console.log('Retrieved and decrypted data:', retrieved.decrypted_data);
    
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

### Python Client Example

```python
import requests
import json

# Server URL
BASE_URL = "http://localhost:8000"

def generate_encryption_key():
    """Generate a client-side encryption key."""
    response = requests.get(f"{BASE_URL}/api/zk/generate-key")
    return response.json()['client_encryption_key']

def prepare_for_storage(data, encryption_key):
    """Prepare data for zero-knowledge storage."""
    response = requests.post(
        f"{BASE_URL}/api/zk/prepare-storage",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "data": data,
            "client_encryption_key": encryption_key
        })
    )
    return response.json()

def retrieve_from_storage(storage_data, encryption_key):
    """Retrieve and decrypt data from storage."""
    response = requests.post(
        f"{BASE_URL}/api/zk/retrieve-storage",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "storage_data": storage_data,
            "client_encryption_key": encryption_key
        })
    )
    return response.json()

# Example usage
if __name__ == "__main__":
    # Generate encryption key (client-side only)
    encryption_key = generate_encryption_key()
    print(f"Generated encryption key: {encryption_key}")
    
    # Sensitive data that should never be seen by the server
    sensitive_data = {
        "ssn": "123-45-6789",
        "credit_card": "4111-1111-1111-1111",
        "personal_notes": "This is my private information"
    }
    
    # Prepare data for storage (encrypted client-side)
    storage_ready = prepare_for_storage(sensitive_data, encryption_key)
    print(f"Storage-ready encrypted data: {storage_ready}")
    
    # Store the encrypted data on the server
    # (In a real app, you would send this to your storage API)
    server_stored_data = storage_ready['storage_ready_data']
    
    # Later, retrieve and decrypt the data
    retrieved = retrieve_from_storage(server_stored_data, encryption_key)
    print(f"Retrieved and decrypted data: {retrieved['decrypted_data']}")
```

## Security Benefits

1. **Zero-Knowledge**: The server never sees plaintext data
2. **Client-Controlled Keys**: Users control their encryption keys
3. **End-to-End Encryption**: Data is encrypted before leaving the client
4. **No Key Storage**: Server never stores encryption keys
5. **Forward Secrecy**: Compromised server doesn't compromise data

## Best Practices

1. **Key Management**: Store encryption keys securely (e.g., in secure keychain)
2. **Key Backup**: Provide mechanisms for key recovery without compromising security
3. **User Education**: Educate users about the importance of key security
4. **Regular Rotation**: Implement key rotation for long-term security
5. **Secure Deletion**: Implement secure deletion of keys and data when needed

This zero-knowledge approach provides strong privacy guarantees that are essential in the AI-dominant age where data harvesting is prevalent.