# Federated Learning Example

This example demonstrates how to use the federated learning features of Nexus HTTP Server.

## Overview

Federated learning allows machine learning models to be trained across decentralized devices without sharing raw data. The server coordinates training rounds where:
1. Server sends global model to clients
2. Clients train on local data and send updates
3. Server aggregates updates to improve global model
4. Process repeats for multiple rounds

## Python Client Example

```python
import requests
import json
import numpy as np

# Server URL
BASE_URL = "http://localhost:8000"

def initialize_global_model(model_structure):
    """Initialize the global federated learning model."""
    response = requests.post(
        f"{BASE_URL}/api/fl/initialize",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"model_structure": model_structure})
    )
    return response.json()

def start_training_round(round_id):
    """Start a new federated learning round."""
    response = requests.post(
        f"{BASE_URL}/api/fl/start-round",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"round_id": round_id})
    )
    return response.json()

def submit_client_update(client_id, round_id, model_update):
    """Submit a client's model update for a training round."""
    response = requests.post(
        f"{BASE_URL}/api/fl/submit-update",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "client_id": client_id,
            "round_id": round_id,
            "model_update": model_update
        })
    )
    return response.json()

def aggregate_updates(round_id, aggregation_method="fedavg"):
    """Aggregate client updates to improve the global model."""
    response = requests.post(
        f"{BASE_URL}/api/fl/aggregate",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "round_id": round_id,
            "aggregation_method": aggregation_method
        })
    )
    return response.json()

def get_round_status(round_id):
    """Get the status of a federated learning round."""
    response = requests.post(
        f"{BASE_URL}/api/fl/round-status",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"round_id": round_id})
    )
    return response.json()

def get_client_statistics():
    """Get statistics about client participation."""
    response = requests.get(f"{BASE_URL}/api/fl/client-stats")
    return response.json()

# Example usage
if __name__ == "__main__":
    # Initialize a simple linear model
    model_structure = {
        "weights": [0.0, 0.0, 0.0],  # 3 weights
        "bias": 0.0
    }
    
    # Initialize the global model
    init_result = initialize_global_model(model_structure)
    print(f"Model initialized: {init_result}")
    
    # Start a training round
    round_id = "round_1"
    start_result = start_training_round(round_id)
    print(f"Round started: {start_result}")
    
    # Simulate client updates (in a real scenario, clients would train on their local data)
    client_updates = [
        {
            "client_id": "client_1",
            "model_update": {
                "weights": [0.1, 0.2, 0.3],
                "bias": 0.05
            }
        },
        {
            "client_id": "client_2",
            "model_update": {
                "weights": [0.15, 0.25, 0.35],
                "bias": 0.08
            }
        },
        {
            "client_id": "client_3",
            "model_update": {
                "weights": [0.05, 0.15, 0.25],
                "bias": 0.02
            }
        }
    ]
    
    # Submit client updates
    for update in client_updates:
        submit_result = submit_client_update(
            update["client_id"],
            round_id,
            update["model_update"]
        )
        print(f"Client {update['client_id']} update submitted: {submit_result}")
    
    # Aggregate updates
    aggregate_result = aggregate_updates(round_id)
    print(f"Updates aggregated: {aggregate_result}")
    
    # Check round status
    status_result = get_round_status(round_id)
    print(f"Round status: {status_result}")
    
    # Get client statistics
    stats_result = get_client_statistics()
    print(f"Client statistics: {stats_result}")
```

## JavaScript Client Example

```javascript
// Example usage of federated learning endpoints

const BASE_URL = 'http://localhost:8000';

async function initializeGlobalModel(modelStructure) {
  const response = await fetch(`${BASE_URL}/api/fl/initialize`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ model_structure: modelStructure }),
  });
  return response.json();
}

async function startTrainingRound(roundId) {
  const response = await fetch(`${BASE_URL}/api/fl/start-round`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ round_id: roundId }),
  });
  return response.json();
}

async function submitClientUpdate(clientId, roundId, modelUpdate) {
  const response = await fetch(`${BASE_URL}/api/fl/submit-update`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      client_id: clientId,
      round_id: roundId,
      model_update: modelUpdate
    }),
  });
  return response.json();
}

async function aggregateUpdates(roundId, aggregationMethod = 'fedavg') {
  const response = await fetch(`${BASE_URL}/api/fl/aggregate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      round_id: roundId,
      aggregation_method: aggregationMethod
    }),
  });
  return response.json();
}

async function getRoundStatus(roundId) {
  const response = await fetch(`${BASE_URL}/api/fl/round-status`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ round_id: roundId }),
  });
  return response.json();
}

async function getClientStatistics() {
  const response = await fetch(`${BASE_URL}/api/fl/client-stats`);
  return response.json();
}

// Example usage
(async () => {
  try {
    // Initialize a simple linear model
    const modelStructure = {
      weights: [0.0, 0.0, 0.0],  // 3 weights
      bias: 0.0
    };
    
    // Initialize the global model
    const initResult = await initializeGlobalModel(modelStructure);
    console.log('Model initialized:', initResult);
    
    // Start a training round
    const roundId = 'round_1';
    const startResult = await startTrainingRound(roundId);
    console.log('Round started:', startResult);
    
    // Simulate client updates (in a real scenario, clients would train on their local data)
    const clientUpdates = [
      {
        client_id: 'client_1',
        model_update: {
          weights: [0.1, 0.2, 0.3],
          bias: 0.05
        }
      },
      {
        client_id: 'client_2',
        model_update: {
          weights: [0.15, 0.25, 0.35],
          bias: 0.08
        }
      },
      {
        client_id: 'client_3',
        model_update: {
          weights: [0.05, 0.15, 0.25],
          bias: 0.02
        }
      }
    ];
    
    // Submit client updates
    for (const update of clientUpdates) {
      const submitResult = await submitClientUpdate(
        update.client_id,
        roundId,
        update.model_update
      );
      console.log(`Client ${update.client_id} update submitted:`, submitResult);
    }
    
    // Aggregate updates
    const aggregateResult = await aggregateUpdates(roundId);
    console.log('Updates aggregated:', aggregateResult);
    
    // Check round status
    const statusResult = await getRoundStatus(roundId);
    console.log('Round status:', statusResult);
    
    // Get client statistics
    const statsResult = await getClientStatistics();
    console.log('Client statistics:', statsResult);
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

## cURL Examples

### Initialize Global Model

```bash
# Initialize a simple linear model
curl -X POST http://localhost:8000/api/fl/initialize \
  -H "Content-Type: application/json" \
  -d '{
    "model_structure": {
      "weights": [0.0, 0.0, 0.0],
      "bias": 0.0
    }
  }'
```

### Start Training Round

```bash
# Start a new federated learning round
curl -X POST http://localhost:8000/api/fl/start-round \
  -H "Content-Type: application/json" \
  -d '{
    "round_id": "round_1"
  }'
```

### Submit Client Update

```bash
# Submit a client's model update
curl -X POST http://localhost:8000/api/fl/submit-update \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "client_1",
    "round_id": "round_1",
    "model_update": {
      "weights": [0.1, 0.2, 0.3],
      "bias": 0.05
    }
  }'
```

### Aggregate Updates

```bash
# Aggregate client updates to improve the global model
curl -X POST http://localhost:8000/api/fl/aggregate \
  -H "Content-Type: application/json" \
  -d '{
    "round_id": "round_1",
    "aggregation_method": "fedavg"
  }'
```

### Get Round Status

```bash
# Get the status of a federated learning round
curl -X POST http://localhost:8000/api/fl/round-status \
  -H "Content-Type: application/json" \
  -d '{
    "round_id": "round_1"
  }'
```

### Get Client Statistics

```bash
# Get statistics about client participation
curl http://localhost:8000/api/fl/client-stats
```

## Best Practices

1. **Secure Communication**: Always use HTTPS in production environments
2. **Model Validation**: Validate client model updates to prevent malicious contributions
3. **Differential Privacy**: Consider adding differential privacy to model updates
4. **Client Authentication**: Authenticate clients to prevent unauthorized participation
5. **Monitoring**: Monitor training rounds and client participation for anomalies
6. **Data Minimization**: Only collect the minimum necessary information for model updates