# Examples

This directory contains example usage of the privacy-preserving features in Nexus HTTP Server.

## 1. End-to-End Encryption Example

### Encrypting Data

```bash
# Encrypt a message
curl -X POST http://localhost:8000/api/encrypt \
  -H "Content-Type: application/json" \
  -d '{"data": "This is a secret message", "password": "mysecretpassword"}'
```

### Decrypting Data

```bash
# Decrypt the message using the encrypted data and salt from the previous response
curl -X POST http://localhost:8000/api/decrypt \
  -H "Content-Type: application/json" \
  -d '{
    "encrypted_data": "ENCRYPTED_DATA_FROM_PREVIOUS_RESPONSE", 
    "salt": "SALT_FROM_PREVIOUS_RESPONSE", 
    "password": "mysecretpassword"
  }'
```

## 2. Differential Privacy Example

### Differentially Private Count

```bash
# Get a differentially private count of items
curl -X POST http://localhost:8000/api/dp/count \
  -H "Content-Type: application/json" \
  -d '{
    "values": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
    "epsilon": 1.0
  }'
```

### Differentially Private Mean

```bash
# Get a differentially private mean of values
curl -X POST http://localhost:8000/api/dp/mean \
  -H "Content-Type: application/json" \
  -d '{
    "values": [10, 20, 30, 40, 50], 
    "epsilon": 1.0
  }'
```

## 3. Python Client Example

```python
import requests
import json

# Server URL
BASE_URL = "http://localhost:8000"

def encrypt_data(data, password):
    """Encrypt data using the server's encryption endpoint."""
    response = requests.post(
        f"{BASE_URL}/api/encrypt",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"data": data, "password": password})
    )
    return response.json()

def decrypt_data(encrypted_data, salt, password):
    """Decrypt data using the server's decryption endpoint."""
    response = requests.post(
        f"{BASE_URL}/api/decrypt",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "encrypted_data": encrypted_data,
            "salt": salt,
            "password": password
        })
    )
    return response.json()

def dp_count(values, epsilon):
    """Get a differentially private count."""
    response = requests.post(
        f"{BASE_URL}/api/dp/count",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"values": values, "epsilon": epsilon})
    )
    return response.json()

def dp_mean(values, epsilon):
    """Get a differentially private mean."""
    response = requests.post(
        f"{BASE_URL}/api/dp/mean",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"values": values, "epsilon": epsilon})
    )
    return response.json()

# Example usage
if __name__ == "__main__":
    # Example 1: Encryption/Decryption
    secret_message = "This is a confidential message"
    password = "strongpassword123"
    
    # Encrypt the message
    encrypted_result = encrypt_data(secret_message, password)
    print(f"Encrypted: {encrypted_result}")
    
    # Decrypt the message
    decrypted_result = decrypt_data(
        encrypted_result["encrypted_data"],
        encrypted_result["salt"],
        password
    )
    print(f"Decrypted: {decrypted_result['decrypted_data']}")
    
    # Example 2: Differential Privacy
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Get differentially private count
    dp_count_result = dp_count(data, epsilon=1.0)
    print(f"DP Count: {dp_count_result}")
    
    # Get differentially private mean
    dp_mean_result = dp_mean(data, epsilon=1.0)
    print(f"DP Mean: {dp_mean_result}")
```

## 4. JavaScript Client Example

```javascript
// Example usage of privacy-preserving endpoints from a browser or Node.js

const BASE_URL = 'http://localhost:8000';

async function encryptData(data, password) {
  const response = await fetch(`${BASE_URL}/api/encrypt`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ data, password }),
  });
  return response.json();
}

async function decryptData(encryptedData, salt, password) {
  const response = await fetch(`${BASE_URL}/api/decrypt`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ encrypted_data: encryptedData, salt, password }),
  });
  return response.json();
}

async function dpCount(values, epsilon) {
  const response = await fetch(`${BASE_URL}/api/dp/count`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ values, epsilon }),
  });
  return response.json();
}

async function dpMean(values, epsilon) {
  const response = await fetch(`${BASE_URL}/api/dp/mean`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ values, epsilon }),
  });
  return response.json();
}

// Example usage
(async () => {
  try {
    // Example 1: Encryption/Decryption
    const secretMessage = "This is a confidential message";
    const password = "strongpassword123";
    
    // Encrypt the message
    const encryptedResult = await encryptData(secretMessage, password);
    console.log('Encrypted:', encryptedResult);
    
    // Decrypt the message
    const decryptedResult = await decryptData(
      encryptedResult.encrypted_data,
      encryptedResult.salt,
      password
    );
    console.log('Decrypted:', decryptedResult.decrypted_data);
    
    // Example 2: Differential Privacy
    const data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    
    // Get differentially private count
    const dpCountResult = await dpCount(data, 1.0);
    console.log('DP Count:', dpCountResult);
    
    // Get differentially private mean
    const dpMeanResult = await dpMean(data, 1.0);
    console.log('DP Mean:', dpMeanResult);
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

These examples demonstrate how to use the privacy-preserving features of Nexus HTTP Server to:

1. Encrypt and decrypt sensitive data
2. Perform differentially private statistical analysis

The encryption endpoints provide end-to-end encryption that ensures only those with the password can access the original data. The differential privacy endpoints allow you to perform statistical analysis on datasets while protecting the privacy of individuals in the dataset.