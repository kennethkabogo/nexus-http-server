# Homomorphic Encryption Example

This example demonstrates how to use the homomorphic encryption features of Nexus HTTP Server.

## Overview

Homomorphic encryption allows computations to be performed on encrypted data without decrypting it first. This example shows how to encrypt values, perform homomorphic operations, and decrypt results.

## Python Client Example

```python
import requests
import json

# Server URL
BASE_URL = "http://localhost:8000"

def generate_keys():
    """Generate homomorphic encryption keys."""
    response = requests.get(f"{BASE_URL}/api/he/generate-keys")
    return response.json()

def encrypt_int(value, public_key):
    """Encrypt an integer value."""
    response = requests.post(
        f"{BASE_URL}/api/he/encrypt/int",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "value": value,
            "public_key": public_key
        })
    )
    return response.json()

def encrypt_float(value, public_key):
    """Encrypt a float value."""
    response = requests.post(
        f"{BASE_URL}/api/he/encrypt/float",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "value": value,
            "public_key": public_key
        })
    )
    return response.json()

def decrypt_value(encrypted_value, private_key):
    """Decrypt a homomorphically encrypted value."""
    response = requests.post(
        f"{BASE_URL}/api/he/decrypt",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "encrypted_value": encrypted_value,
            "private_key": private_key
        })
    )
    return response.json()

def homomorphic_add(encrypted_a, encrypted_b):
    """Perform homomorphic addition on two encrypted values."""
    response = requests.post(
        f"{BASE_URL}/api/he/add",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "encrypted_a": encrypted_a,
            "encrypted_b": encrypted_b
        })
    )
    return response.json()

def homomorphic_multiply(encrypted_value, scalar):
    """Perform homomorphic multiplication of an encrypted value by a scalar."""
    response = requests.post(
        f"{BASE_URL}/api/he/multiply",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "encrypted_value": encrypted_value,
            "scalar": scalar
        })
    )
    return response.json()

# Example usage
if __name__ == "__main__":
    # Generate keys
    keys_result = generate_keys()
    print(f"Keys generated: {keys_result}")
    
    public_key = keys_result['public_key']
    private_key = keys_result['private_key']  # In practice, store this securely
    
    # Encrypt some values
    value1 = 15
    value2 = 25
    
    encrypted1_result = encrypt_int(value1, public_key)
    encrypted2_result = encrypt_int(value2, public_key)
    
    encrypted1 = encrypted1_result['encrypted_value']
    encrypted2 = encrypted2_result['encrypted_value']
    
    print(f"Encrypted {value1}: {encrypted1}")
    print(f"Encrypted {value2}: {encrypted2}")
    
    # Perform homomorphic addition
    add_result = homomorphic_add(encrypted1, encrypted2)
    encrypted_sum = add_result['result']
    print(f"Homomorphic addition result: {encrypted_sum}")
    
    # Decrypt the result
    decrypted_sum_result = decrypt_value(encrypted_sum, private_key)
    decrypted_sum = decrypted_sum_result['decrypted_value']
    print(f"Decrypted sum: {decrypted_sum}")
    print(f"Expected sum: {value1 + value2}")
    
    # Perform homomorphic multiplication
    scalar = 3
    mult_result = homomorphic_multiply(encrypted1, scalar)
    encrypted_product = mult_result['result']
    print(f"Homomorphic multiplication result: {encrypted_product}")
    
    # Decrypt the result
    decrypted_product_result = decrypt_value(encrypted_product, private_key)
    decrypted_product = decrypted_product_result['decrypted_value']
    print(f"Decrypted product: {decrypted_product}")
    print(f"Expected product: {value1 * scalar}")
```

## JavaScript Client Example

```javascript
// Example usage of homomorphic encryption endpoints

const BASE_URL = 'http://localhost:8000';

async function generateKeys() {
  const response = await fetch(`${BASE_URL}/api/he/generate-keys`);
  return response.json();
}

async function encryptInt(value, publicKey) {
  const response = await fetch(`${BASE_URL}/api/he/encrypt/int`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ value, public_key: publicKey }),
  });
  return response.json();
}

async function encryptFloat(value, publicKey) {
  const response = await fetch(`${BASE_URL}/api/he/encrypt/float`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ value, public_key: publicKey }),
  });
  return response.json();
}

async function decryptValue(encryptedValue, privateKey) {
  const response = await fetch(`${BASE_URL}/api/he/decrypt`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ encrypted_value: encryptedValue, private_key: privateKey }),
  });
  return response.json();
}

async function homomorphicAdd(encryptedA, encryptedB) {
  const response = await fetch(`${BASE_URL}/api/he/add`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ encrypted_a: encryptedA, encrypted_b: encryptedB }),
  });
  return response.json();
}

async function homomorphicMultiply(encryptedValue, scalar) {
  const response = await fetch(`${BASE_URL}/api/he/multiply`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ encrypted_value: encryptedValue, scalar }),
  });
  return response.json();
}

// Example usage
(async () => {
  try {
    // Generate keys
    const keysResult = await generateKeys();
    console.log('Keys generated:', keysResult);
    
    const publicKey = keysResult.public_key;
    const privateKey = keysResult.private_key;  // In practice, store this securely
    
    // Encrypt some values
    const value1 = 15;
    const value2 = 25;
    
    const encrypted1Result = await encryptInt(value1, publicKey);
    const encrypted2Result = await encryptInt(value2, publicKey);
    
    const encrypted1 = encrypted1Result.encrypted_value;
    const encrypted2 = encrypted2Result.encrypted_value;
    
    console.log(`Encrypted ${value1}:`, encrypted1);
    console.log(`Encrypted ${value2}:`, encrypted2);
    
    // Perform homomorphic addition
    const addResult = await homomorphicAdd(encrypted1, encrypted2);
    const encryptedSum = addResult.result;
    console.log('Homomorphic addition result:', encryptedSum);
    
    // Decrypt the result
    const decryptedSumResult = await decryptValue(encryptedSum, privateKey);
    const decryptedSum = decryptedSumResult.decrypted_value;
    console.log('Decrypted sum:', decryptedSum);
    console.log('Expected sum:', value1 + value2);
    
    // Perform homomorphic multiplication
    const scalar = 3;
    const multResult = await homomorphicMultiply(encrypted1, scalar);
    const encryptedProduct = multResult.result;
    console.log('Homomorphic multiplication result:', encryptedProduct);
    
    // Decrypt the result
    const decryptedProductResult = await decryptValue(encryptedProduct, privateKey);
    const decryptedProduct = decryptedProductResult.decrypted_value;
    console.log('Decrypted product:', decryptedProduct);
    console.log('Expected product:', value1 * scalar);
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

## cURL Examples

### Generate Keys

```bash
# Generate homomorphic encryption keys
curl http://localhost:8000/api/he/generate-keys
```

### Encrypt an Integer

```bash
# Encrypt an integer value
curl -X POST http://localhost:8000/api/he/encrypt/int \
  -H "Content-Type: application/json" \
  -d '{
    "value": 42,
    "public_key": "public_key_placeholder"
  }'
```

### Encrypt a Float

```bash
# Encrypt a float value
curl -X POST http://localhost:8000/api/he/encrypt/float \
  -H "Content-Type: application/json" \
  -d '{
    "value": 3.14159,
    "public_key": "public_key_placeholder"
  }'
```

### Decrypt a Value

```bash
# Decrypt a homomorphically encrypted value
curl -X POST http://localhost:8000/api/he/decrypt \
  -H "Content-Type: application/json" \
  -d '{
    "encrypted_value": {
      "encrypted_value": "enc_example",
      "type": "integer",
      "encryption_scheme": "demo_homomorphic"
    },
    "private_key": "private_key_placeholder"
  }'
```

### Homomorphic Addition

```bash
# Perform homomorphic addition on two encrypted values
curl -X POST http://localhost:8000/api/he/add \
  -H "Content-Type: application/json" \
  -d '{
    "encrypted_a": {
      "encrypted_value": "enc_value1",
      "type": "integer",
      "encryption_scheme": "demo_homomorphic"
    },
    "encrypted_b": {
      "encrypted_value": "enc_value2",
      "type": "integer",
      "encryption_scheme": "demo_homomorphic"
    }
  }'
```

### Homomorphic Multiplication

```bash
# Perform homomorphic multiplication of an encrypted value by a scalar
curl -X POST http://localhost:8000/api/he/multiply \
  -H "Content-Type: application/json" \
  -d '{
    "encrypted_value": {
      "encrypted_value": "enc_value",
      "type": "integer",
      "encryption_scheme": "demo_homomorphic"
    },
    "scalar": 5
  }'
```

## Best Practices

1. **Key Management**: Store private keys securely and never expose them in client code
2. **Performance Considerations**: Homomorphic encryption is computationally expensive
3. **Data Types**: Be aware of precision limitations with floating-point homomorphic operations
4. **Security**: Use production-grade homomorphic encryption libraries in real applications
5. **Auditing**: Log homomorphic operations for security auditing
6. **Limitations**: Understand that this is a demo implementation - production systems need proper cryptographic libraries