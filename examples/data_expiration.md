# Data Expiration and Self-Destruction Example

This example demonstrates how to use the data expiration and self-destruction features of Nexus HTTP Server.

## Overview

Data expiration and self-destruction features ensure that sensitive data doesn't persist longer than necessary, enhancing privacy by automatically removing data after a specified time period.

## Python Client Example

```python
import requests
import json

# Server URL
BASE_URL = "http://localhost:8000"

def get_all_expiring_data():
    \"\"\"Get information about all expiring data items.\"\"\"
    response = requests.get(f"{BASE_URL}/api/data/expiration")
    return response.json()

def get_data_expiration_info(data_id):
    \"\"\"Get expiration information for a specific data item.\"\"\"
    response = requests.get(f"{BASE_URL}/api/data/expiration/{data_id}")
    return response.json()

def extend_data_expiration(data_id, additional_seconds):
    \"\"\"Extend expiration time for a data item.\"\"\"
    response = requests.post(
        f"{BASE_URL}/api/data/expiration/{data_id}/extend",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"additional_seconds": additional_seconds})
    )
    return response.json()

def cancel_data_expiration(data_id):
    \"\"\"Cancel expiration for a data item.\"\"\"
    response = requests.post(f"{BASE_URL}/api/data/expiration/{data_id}/cancel")
    return response.json()

# Example usage
if __name__ == "__main__":
    # Get information about all expiring data
    all_expiring = get_all_expiring_data()
    print(f"All Expiring Data: {all_expiring}")
    
    # If you have a specific data item ID, you can work with it
    # data_id = "your_data_item_id"
    
    # Get expiration information for a specific data item
    # expiration_info = get_data_expiration_info(data_id)
    # print(f"Expiration Info: {expiration_info}")
    
    # Extend expiration time for a data item
    # extend_result = extend_data_expiration(data_id, 3600)  # Extend by 1 hour
    # print(f"Extended Expiration: {extend_result}")
    
    # Cancel expiration for a data item
    # cancel_result = cancel_data_expiration(data_id)
    # print(f"Cancelled Expiration: {cancel_result}")
```

## JavaScript Client Example

```javascript
// Example usage of data expiration endpoints

const BASE_URL = 'http://localhost:8000';

async function getAllExpiringData() {
  const response = await fetch(`${BASE_URL}/api/data/expiration`);
  return response.json();
}

async function getDataExpirationInfo(dataId) {
  const response = await fetch(`${BASE_URL}/api/data/expiration/${dataId}`);
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

async function cancelDataExpiration(dataId) {
  const response = await fetch(`${BASE_URL}/api/data/expiration/${dataId}/cancel`, {
    method: 'POST',
  });
  return response.json();
}

// Example usage
(async () => {
  try {
    // Get information about all expiring data
    const allExpiring = await getAllExpiringData();
    console.log('All Expiring Data:', allExpiring);
    
    // If you have a specific data item ID, you can work with it
    // const dataId = "your_data_item_id";
    
    // Get expiration information for a specific data item
    // const expirationInfo = await getDataExpirationInfo(dataId);
    // console.log('Expiration Info:', expirationInfo);
    
    // Extend expiration time for a data item
    // const extendResult = await extendDataExpiration(dataId, 3600);  // Extend by 1 hour
    // console.log('Extended Expiration:', extendResult);
    
    // Cancel expiration for a data item
    // const cancelResult = await cancelDataExpiration(dataId);
    // console.log('Cancelled Expiration:', cancelResult);
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

## cURL Examples

### Get Information About All Expiring Data

```bash
# Get information about all expiring data
curl http://localhost:8000/api/data/expiration
```

### Get Expiration Information for a Specific Data Item

```bash
# Get expiration information for a specific data item
curl http://localhost:8000/api/data/expiration/data_item_123
```

### Extend Expiration Time for a Data Item

```bash
# Extend expiration time for a data item
curl -X POST http://localhost:8000/api/data/expiration/data_item_123/extend \\
  -H "Content-Type: application/json" \\
  -d '{"additional_seconds": 3600}'
```

### Cancel Expiration for a Data Item

```bash
# Cancel expiration for a data item
curl -X POST http://localhost:8000/api/data/expiration/data_item_123/cancel
```

## Best Practices

1. **Set Appropriate TTL Values**: Choose TTL values that balance data utility with privacy requirements
2. **Monitor Expiring Data**: Regularly check which data items are scheduled for expiration
3. **Extend When Necessary**: Extend expiration times for data that still needs to be retained
4. **Cancel Expiration Carefully**: Only cancel expiration for data that truly needs to be retained long-term
5. **Combine with Encryption**: Use data expiration in combination with encryption for maximum privacy protection