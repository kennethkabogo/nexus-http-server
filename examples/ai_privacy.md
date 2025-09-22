# AI Training Data Opt-Out Example

This example demonstrates how to use the AI training data opt-out features of Nexus HTTP Server.

## Overview

AI training data opt-out allows users to prevent their data from being used for AI model training. This example shows how to set opt-out preferences, check opt-out status, and work with AI privacy headers.

## Python Client Example

```python
import requests
import json

# Server URL
BASE_URL = "http://localhost:8000"

def set_ai_opt_out(token, opt_out=True):
    \"\"\"Set AI training data opt-out preference.\"\"\"
    response = requests.post(
        f"{BASE_URL}/api/ai/opt-out",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        data=json.dumps({"opt_out": opt_out})
    )
    return response.json()

def get_ai_opt_out_status(token):
    \"\"\"Get AI training data opt-out status.\"\"\"
    response = requests.get(
        f"{BASE_URL}/api/ai/opt-out/status",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()

def start_ai_training_job(token, job_id, model_type, data_sources):
    \"\"\"Start an AI model training job with privacy controls.\"\"\"
    response = requests.post(
        f"{BASE_URL}/api/ai/training-job",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "job_id": job_id,
            "model_type": model_type,
            "data_sources": data_sources
        })
    )
    return response.json()

def get_ai_training_jobs(token):
    \"\"\"Get information about all AI training jobs.\"\"\"
    response = requests.get(
        f"{BASE_URL}/api/ai/training-jobs",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()

def get_ai_privacy_report(token):
    \"\"\"Get AI privacy report for the authenticated user.\"\"\"
    response = requests.get(
        f"{BASE_URL}/api/ai/privacy-report",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()

# Example usage
if __name__ == "__main__":
    # You need a valid JWT token for these operations
    jwt_token = "YOUR_JWT_TOKEN"
    
    # Set AI opt-out preference
    opt_out_result = set_ai_opt_out(jwt_token, True)
    print(f"AI opt-out set: {opt_out_result}")
    
    # Get AI opt-out status
    status_result = get_ai_opt_out_status(jwt_token)
    print(f"AI opt-out status: {status_result}")
    
    # Start an AI training job
    job_result = start_ai_training_job(
        jwt_token,
        "job_123",
        "recommendation_model",
        ["user_data_1", "user_data_2", "user_data_3"]
    )
    print(f"AI training job started: {job_result}")
    
    # Get all AI training jobs
    jobs_result = get_ai_training_jobs(jwt_token)
    print(f"AI training jobs: {jobs_result}")
    
    # Get AI privacy report
    report_result = get_ai_privacy_report(jwt_token)
    print(f"AI privacy report: {report_result}")
```

## JavaScript Client Example

```javascript
// Example usage of AI privacy endpoints

const BASE_URL = 'http://localhost:8000';

async function setAIOptOut(token, optOut = true) {
  const response = await fetch(`${BASE_URL}/api/ai/opt-out`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ opt_out: optOut }),
  });
  return response.json();
}

async function getAIOptOutStatus(token) {
  const response = await fetch(`${BASE_URL}/api/ai/opt-out/status`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  return response.json();
}

async function startAITrainingJob(token, jobId, modelType, dataSources) {
  const response = await fetch(`${BASE_URL}/api/ai/training-job`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ job_id: jobId, model_type: modelType, data_sources: dataSources }),
  });
  return response.json();
}

async function getAITrainingJobs(token) {
  const response = await fetch(`${BASE_URL}/api/ai/training-jobs`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  return response.json();
}

async function getAIPrivacyReport(token) {
  const response = await fetch(`${BASE_URL}/api/ai/privacy-report`, {
    method: 'GET',
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
    
    // Set AI opt-out preference
    const optOutResult = await setAIOptOut(jwtToken, true);
    console.log('AI opt-out set:', optOutResult);
    
    // Get AI opt-out status
    const statusResult = await getAIOptOutStatus(jwtToken);
    console.log('AI opt-out status:', statusResult);
    
    // Start an AI training job
    const jobResult = await startAITrainingJob(
      jwtToken,
      "job_123",
      "recommendation_model",
      ["user_data_1", "user_data_2", "user_data_3"]
    );
    console.log('AI training job started:', jobResult);
    
    // Get all AI training jobs
    const jobsResult = await getAITrainingJobs(jwtToken);
    console.log('AI training jobs:', jobsResult);
    
    // Get AI privacy report
    const reportResult = await getAIPrivacyReport(jwtToken);
    console.log('AI privacy report:', reportResult);
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

## cURL Examples

### Set AI Opt-Out Preference

```bash
# Set AI training data opt-out preference (requires authentication)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -X POST http://localhost:8000/api/ai/opt-out \
  -H "Content-Type: application/json" \
  -d '{"opt_out": true}'
```

### Get AI Opt-Out Status

```bash
# Get AI training data opt-out status (requires authentication)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:8000/api/ai/opt-out/status
```

### Start AI Training Job

```bash
# Start an AI model training job with privacy controls (requires authentication)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -X POST http://localhost:8000/api/ai/training-job \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "job_123",
    "model_type": "recommendation_model",
    "data_sources": ["user_data_1", "user_data_2", "user_data_3"]
  }'
```

### Get AI Training Jobs

```bash
# Get information about all AI training jobs (requires authentication)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:8000/api/ai/training-jobs
```

### Get AI Privacy Report

```bash
# Get AI privacy report for the authenticated user (requires authentication)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:8000/api/ai/privacy-report
```

## AI Privacy Headers

The server automatically adds the following AI privacy headers to all responses:

- `X-AI-Training-Opt-Out: true` - Opt-out of AI training
- `X-No-AI-Model-Training: true` - No AI model training on this data
- `X-No-Machine-Learning: true` - Data should not be used for machine learning
- `X-AI-Respect-Privacy: true` - Request that AI systems respect privacy
- `X-Do-Not-Train: true` - Do Not Train header (emerging standard)
- `X-Do-Not-Profile: true` - Do Not Profile header

## Best Practices

1. **User Consent**: Always obtain explicit consent before collecting data for AI training
2. **Clear Opt-Out**: Provide clear and accessible opt-out mechanisms
3. **Transparency**: Be transparent about how data is used for AI purposes
4. **Data Minimization**: Collect only the minimum necessary data for AI training
5. **Regular Audits**: Regularly audit AI data usage and compliance
6. **Privacy by Design**: Implement privacy controls by default
7. **Compliance**: Ensure compliance with privacy regulations like GDPR and CCPA
8. **User Control**: Give users granular control over their data usage