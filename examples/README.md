# Examples

This directory contains example usage of the privacy-preserving features in Nexus HTTP Server.

## 1. End-to-End Encryption Example

### Encrypting Data

```bash
# Encrypt a message
curl -X POST http://localhost:8000/api/encrypt 
  -H "Content-Type: application/json" 
  -d '{"data": "This is a secret message", "password": "mysecretpassword"}'
```

### Decrypting Data

```bash
# Decrypt the message using the encrypted data and salt from the previous response
curl -X POST http://localhost:8000/api/decrypt 
  -H "Content-Type: application/json" 
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
curl -X POST http://localhost:8000/api/dp/count 
  -H "Content-Type: application/json" 
  -d '{
    "values": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
    "epsilon": 1.0
  }'
```

### Differentially Private Mean

```bash
# Get a differentially private mean of values
curl -X POST http://localhost:8000/api/dp/mean 
  -H "Content-Type: application/json" 
  -d '{
    "values": [10, 20, 30, 40, 50], 
    "epsilon": 1.0
  }'
```

## 3. Zero-Knowledge Encryption Example

See the detailed example in [zero_knowledge.md](zero_knowledge.md) for comprehensive usage of the zero-knowledge encryption features.

## 4. Privacy Budget Management Example

See the detailed example in [privacy_budget.md](privacy_budget.md) for comprehensive usage of the privacy budget management features.

## 5. Data Expiration Example

See the detailed example in [data_expiration.md](data_expiration.md) for comprehensive usage of the data expiration features.

## 6. Federated Learning Example

See the detailed example in [federated_learning.md](federated_learning.md) for comprehensive usage of the federated learning features.

## 7. Decentralized Identity Example

See the detailed example in [decentralized_identity.md](decentralized_identity.md) for comprehensive usage of the decentralized identity features.

## 8. Homomorphic Encryption Example

See the detailed example in [homomorphic_encryption.md](homomorphic_encryption.md) for comprehensive usage of the homomorphic encryption features.

## 9. AI Training Data Opt-Out Example

See the detailed example in [ai_privacy.md](ai_privacy.md) for comprehensive usage of the AI privacy features.

## 10. Python Client Example

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

def get_privacy_budget(token):
    """Get current privacy budget status."""
    response = requests.get(
        f"{BASE_URL}/api/privacy/budget",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()

def consume_privacy_budget(token, epsilon, query_type):
    """Manually consume a portion of the privacy budget."""
    response = requests.post(
        f"{BASE_URL}/api/privacy/budget/consume",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "epsilon": epsilon,
            "query_type": query_type
        })
    )
    return response.json()

def get_data_expiration_info():
    """Get information about all expiring data."""
    response = requests.get(f"{BASE_URL}/api/data/expiration")
    return response.json()

def extend_data_expiration(data_id, additional_seconds):
    """Extend expiration time for a data item."""
    response = requests.post(
        f"{BASE_URL}/api/data/expiration/{data_id}/extend",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"additional_seconds": additional_seconds})
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
    
    # Example 3: Privacy Budget Management (requires authentication)
    # jwt_token = "YOUR_JWT_TOKEN"
    # budget_info = get_privacy_budget(jwt_token)
    # print(f"Privacy Budget: {budget_info}")
    # 
    # # Consume some privacy budget
    # consume_result = consume_privacy_budget(jwt_token, 0.1, "example_query")
    # print(f"Consumed Budget: {consume_result}")
    
    # Example 4: Data Expiration
    # expiration_info = get_data_expiration_info()
    # print(f"Expiring Data: {expiration_info}")
    # 
    # # Extend expiration for a data item (if any exist)
    # # extend_result = extend_data_expiration("data_item_123", 3600)
    # # print(f"Extended Expiration: {extend_result}")
```

## 11. JavaScript Client Example

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

async function getPrivacyBudget(token) {
  const response = await fetch(`${BASE_URL}/api/privacy/budget`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  return response.json();
}

async function consumePrivacyBudget(token, epsilon, queryType) {
  const response = await fetch(`${BASE_URL}/api/privacy/budget/consume`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ epsilon, query_type: queryType }),
  });
  return response.json();
}

async function getDataExpirationInfo() {
  const response = await fetch(`${BASE_URL}/api/data/expiration`);
  return response.json();
}

async function extendDataExpiration(dataId, additionalSeconds) {
  const response = await fetch(`${BASE_URL}/api/data/expiration/${dataId}/extend`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ additional_seconds: additionalSeconds }),
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
    
    // Example 3: Privacy Budget Management (requires authentication)
    // const jwtToken = "YOUR_JWT_TOKEN";
    // const budgetInfo = await getPrivacyBudget(jwtToken);
    // console.log('Privacy Budget:', budgetInfo);
    // 
    // // Consume some privacy budget
    // const consumeResult = await consumePrivacyBudget(jwtToken, 0.1, "example_query");
    // console.log('Consumed Budget:', consumeResult);
    
    // Example 4: Data Expiration
    // const expirationInfo = await getDataExpirationInfo();
    // console.log('Expiring Data:', expirationInfo);
    // 
    // // Extend expiration for a data item (if any exist)
    // // const extendResult = await extendDataExpiration("data_item_123", 3600);
    // // console.log('Extended Expiration:', extendResult);
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

These examples demonstrate how to use the privacy-preserving features of Nexus HTTP Server to:

1. Encrypt and decrypt sensitive data
2. Perform differentially private statistical analysis
3. Implement zero-knowledge encryption where the server never sees plaintext data
4. Manage privacy budgets to control differential privacy consumption
5. Set up automatic data expiration and self-destruction
6. Coordinate federated learning across decentralized devices
7. Work with decentralized identities and verifiable credentials
8. Perform homomorphic computations on encrypted data
9. Opt out of AI training data harvesting

The encryption endpoints provide end-to-end encryption that ensures only those with the password can access the original data. The differential privacy endpoints allow you to perform statistical analysis on datasets while protecting the privacy of individuals in the dataset. The zero-knowledge encryption endpoints implement a client-side encryption model where the server only stores encrypted data and never sees encryption keys or plaintext. The privacy budget management endpoints allow users to track and control their privacy consumption. The data expiration endpoints provide automatic cleanup of sensitive data. The federated learning endpoints enable privacy-preserving machine learning across decentralized devices. The decentralized identity endpoints enable self-sovereign identity. The homomorphic encryption endpoints allow computations on encrypted data. The AI privacy endpoints provide opt-out mechanisms for AI training data harvesting.