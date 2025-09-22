# Privacy Budget Management Example

This example demonstrates how to use the privacy budget management features of Nexus HTTP Server.

## Overview

Privacy budget management allows users to track and control their differential privacy consumption. Each user has a privacy budget (epsilon) that gets consumed with each differentially private query.

## Python Client Example

```python
import requests
import json

# Server URL
BASE_URL = "http://localhost:8000"

def get_privacy_budget(token):
    \"\"\"Get current privacy budget status.\"\"\"
    response = requests.get(
        f"{BASE_URL}/api/privacy/budget",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()

def get_privacy_budget_history(token):
    \"\"\"Get privacy budget usage history.\"\"\"
    response = requests.get(
        f"{BASE_URL}/api/privacy/budget/history",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()

def get_epsilon_suggestions(token, sensitivity=1.0):
    \"\"\"Get suggestions for epsilon values based on remaining budget.\"\"\"
    response = requests.post(
        f"{BASE_URL}/api/privacy/budget/suggest",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        data=json.dumps({"sensitivity": sensitivity})
    )
    return response.json()

def consume_privacy_budget(token, epsilon, query_type):
    \"\"\"Manually consume a portion of the privacy budget.\"\"\"
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

def reset_privacy_budget(token):
    \"\"\"Reset privacy budget.\"\"\"
    response = requests.post(
        f"{BASE_URL}/api/privacy/budget/reset",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()

# Example usage
if __name__ == "__main__":
    # You need a valid JWT token for these operations
    jwt_token = "YOUR_JWT_TOKEN"
    
    # Get current privacy budget status
    budget_info = get_privacy_budget(jwt_token)
    print(f"Privacy Budget: {budget_info}")
    
    # Get privacy budget usage history
    history = get_privacy_budget_history(jwt_token)
    print(f"Budget History: {history}")
    
    # Get epsilon value suggestions
    suggestions = get_epsilon_suggestions(jwt_token, sensitivity=1.0)
    print(f"Epsilon Suggestions: {suggestions}")
    
    # Consume some privacy budget
    consume_result = consume_privacy_budget(jwt_token, 0.1, "example_query")
    print(f"Consumed Budget: {consume_result}")
    
    # Get updated budget status
    updated_budget = get_privacy_budget(jwt_token)
    print(f"Updated Budget: {updated_budget}")
    
    # Reset privacy budget (use with caution)
    # reset_result = reset_privacy_budget(jwt_token)
    # print(f"Reset Budget: {reset_result}")
```

## JavaScript Client Example

```javascript
// Example usage of privacy budget management endpoints

const BASE_URL = 'http://localhost:8000';

async function getPrivacyBudget(token) {
  const response = await fetch(`${BASE_URL}/api/privacy/budget`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  return response.json();
}

async function getPrivacyBudgetHistory(token) {
  const response = await fetch(`${BASE_URL}/api/privacy/budget/history`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  return response.json();
}

async function getEpsilonSuggestions(token, sensitivity = 1.0) {
  const response = await fetch(`${BASE_URL}/api/privacy/budget/suggest`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ sensitivity }),
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

async function resetPrivacyBudget(token) {
  const response = await fetch(`${BASE_URL}/api/privacy/budget/reset`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  return response.json();
}

// Example usage
(async () => {
  try {
    // You need a valid JWT token for these operations
    const jwtToken = "YOUR_JWT_TOKEN";
    
    // Get current privacy budget status
    const budgetInfo = await getPrivacyBudget(jwtToken);
    console.log('Privacy Budget:', budgetInfo);
    
    // Get privacy budget usage history
    const history = await getPrivacyBudgetHistory(jwtToken);
    console.log('Budget History:', history);
    
    // Get epsilon value suggestions
    const suggestions = await getEpsilonSuggestions(jwtToken, 1.0);
    console.log('Epsilon Suggestions:', suggestions);
    
    // Consume some privacy budget
    const consumeResult = await consumePrivacyBudget(jwtToken, 0.1, "example_query");
    console.log('Consumed Budget:', consumeResult);
    
    // Get updated budget status
    const updatedBudget = await getPrivacyBudget(jwtToken);
    console.log('Updated Budget:', updatedBudget);
    
    // Reset privacy budget (use with caution)
    // const resetResult = await resetPrivacyBudget(jwtToken);
    // console.log('Reset Budget:', resetResult);
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

## cURL Examples

### Get Current Privacy Budget Status

```bash
# Get privacy budget status (requires authentication)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:8000/api/privacy/budget
```

### Get Privacy Budget Usage History

```bash
# Get privacy budget usage history (requires authentication)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:8000/api/privacy/budget/history
```

### Get Epsilon Value Suggestions

```bash
# Get suggestions for epsilon values (requires authentication)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -X POST http://localhost:8000/api/privacy/budget/suggest \
  -H "Content-Type: application/json" \
  -d '{"sensitivity": 1.0}'
```

### Manually Consume Privacy Budget

```bash
# Manually consume a portion of the privacy budget (requires authentication)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -X POST http://localhost:8000/api/privacy/budget/consume \
  -H "Content-Type: application/json" \
  -d '{
    "epsilon": 0.5,
    "query_type": "custom_analysis"
  }'
```

### Reset Privacy Budget

```bash
# Reset privacy budget (requires authentication)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -X POST http://localhost:8000/api/privacy/budget/reset
```

## Best Practices

1. **Monitor Budget Usage**: Regularly check your privacy budget to understand how much you've consumed
2. **Use Conservative Epsilon Values**: Start with smaller epsilon values for stronger privacy
3. **Plan Budget Consumption**: Plan your queries to make efficient use of your privacy budget
4. **Reset Judiciously**: Only reset your privacy budget when you're sure it's appropriate
5. **Track Query Types**: Use descriptive query types to help track what's consuming your budget