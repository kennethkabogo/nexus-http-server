# Nexus HTTP Server Security Documentation

This document provides detailed information about the security and privacy features implemented in the Nexus HTTP Server, with a particular focus on the privacy-preserving capabilities.

## Table of Contents

1. [Overview](#overview)
2. [Encryption Features](#encryption-features)
3. [Differential Privacy Features](#differential-privacy-features)
4. [Zero-Knowledge Architecture](#zero-knowledge-architecture)
5. [Decentralized Identity](#decentralized-identity)
6. [Homomorphic Encryption](#homomorphic-encryption)
7. [AI Privacy Protection](#ai-privacy-protection)
8. [Privacy Budget Management](#privacy-budget-management)
9. [Data Expiration](#data-expiration)
10. [Traditional Security Features](#traditional-security-features)
11. [API Endpoints](#api-endpoints)
12. [Best Practices](#best-practices)

## Overview

Nexus HTTP Server implements cutting-edge privacy-preserving technologies alongside traditional security measures to protect both data in transit and at rest. The server incorporates:

- End-to-end encryption for sensitive data
- Differential privacy for statistical analysis
- Zero-knowledge architecture for client-controlled encryption
- Decentralized identity for self-sovereign identity
- Homomorphic encryption for computations on encrypted data
- AI privacy protection with opt-out mechanisms
- Traditional security measures like JWT authentication and rate limiting

## Encryption Features

### End-to-End Encryption

The server implements robust end-to-end encryption using industry-standard cryptographic algorithms:

- **PBKDF2** for key derivation from passwords
- **AES-256** via **Fernet** for symmetric encryption
- **Base64** encoding for safe transmission

#### Key Features:

1. **Password-Based Key Derivation**: Uses PBKDF2 with 100,000 iterations to derive strong cryptographic keys from user passwords
2. **Salt Generation**: Automatically generates unique 16-byte salts for each encryption operation to prevent rainbow table attacks
3. **Symmetric Encryption**: Uses Fernet (AES 128 in CBC mode with HMAC for authentication)
4. **Safe Encoding**: Base64 encodes encrypted data and salts for safe JSON transmission

#### Usage Example:

```bash
# Encrypt data
curl -X POST http://localhost:8000/api/encrypt -H "Content-Type: application/json" -d '{"data": "Secret Message", "password": "strongpassword123"}'

# Decrypt data
curl -X POST http://localhost:8000/api/decrypt -H "Content-Type: application/json" -d '{"encrypted_data": "eyJkYXRhIjogIk15IGVuY3J5cHRlZCBkYXRhIiwgInNhbHQiOiAiTVdVek1EST0ifQ==", "salt": "TVdVek1EST0=", "password": "strongpassword123"}'
```

## Differential Privacy Features

Differential privacy is a mathematical framework that provides strong privacy guarantees for statistical analysis. The server implements:

### Laplace Mechanism

The core of differential privacy in Nexus is the Laplace mechanism, which adds calibrated noise to statistical queries.

#### Key Concepts:

1. **ε (Epsilon)**: Privacy budget parameter
   - Smaller ε = stronger privacy, more noise
   - Larger ε = weaker privacy, less noise
   - Typical values: 0.01-10.0

2. **Sensitivity**: Maximum change in query output when one record is added/removed
   - For counting queries: 1
   - For sum queries: Depends on data range

3. **Noise Scale**: Determined by sensitivity/ε

#### Implemented Algorithms:

1. **DP Count**: Differentially private count of records
2. **DP Mean**: Differentially private mean calculation with ε budget splitting

#### Usage Example:

```bash
# Differentially private count
curl -X POST http://localhost:8000/api/dp/count -H "Content-Type: application/json" -d '{"values": [1, 2, 3, 4, 5], "epsilon": 1.0}'

# Differentially private mean
curl -X POST http://localhost:8000/api/dp/mean -H "Content-Type: application/json" -d '{"values": [10, 20, 30, 40, 50], "epsilon": 1.0}'
```

## Zero-Knowledge Architecture

Zero-knowledge architecture ensures that the server never sees plaintext data or encryption keys, providing the strongest possible privacy guarantees.

### Key Features:

1. **Client-Controlled Keys**: Users generate and control their own encryption keys
2. **Server-Blind Storage**: Server only stores encrypted data and never sees plaintext
3. **Forward Secrecy**: Compromised server doesn't compromise user data
4. **End-to-End Encryption**: Data is encrypted before leaving the client

### API Endpoints:

- `/api/zk/generate-key` - Generate client-side encryption keys
- `/api/zk/prepare-storage` - Prepare data for zero-knowledge storage
- `/api/zk/retrieve-storage` - Retrieve and decrypt data from storage

### Usage Example:

```bash
# Generate encryption key
curl http://localhost:8000/api/zk/generate-key

# Prepare data for storage
curl -X POST http://localhost:8000/api/zk/prepare-storage -H "Content-Type: application/json" -d '{"data": {"ssn": "123-45-6789", "credit_card": "4111-1111-1111-1111"}, "client_encryption_key": "CLIENT_GENERATED_KEY"}'

# Retrieve and decrypt data
curl -X POST http://localhost:8000/api/zk/retrieve-storage -H "Content-Type: application/json" -d '{"storage_data": {"encrypted_data": "ENCRYPTED_DATA"}, "client_encryption_key": "CLIENT_GENERATED_KEY"}'
```

## Decentralized Identity

Decentralized identity (DID) enables self-sovereign identity without relying on centralized identity providers.

### Key Features:

1. **Self-Sovereign Identity**: Users control their own identity
2. **Verifiable Credentials**: Issue and verify cryptographically secure credentials
3. **DID Documents**: Standardized identity documents following W3C specifications
4. **Key Pair Management**: Secure generation and management of cryptographic keys

### API Endpoints:

- `/api/did/generate` - Generate DID key pairs
- `/api/did/document` - Create and manage DID documents
- `/api/did/credential/issue` - Issue verifiable credentials
- `/api/did/credential/verify` - Verify verifiable credentials

### Usage Example:

```bash
# Generate a DID
curl http://localhost:8000/api/did/generate

# Create a DID document
curl -X POST http://localhost:8000/api/did/document -H "Content-Type: application/json" -d '{"did": "did:nexus:user123", "public_key": "PUBLIC_KEY_PEM"}'

# Issue a verifiable credential
curl -X POST http://localhost:8000/api/did/credential/issue -H "Content-Type: application/json" -d '{"issuer_did": "did:nexus:issuer123", "subject_did": "did:nexus:user123", "claims": {"name": "John Doe", "email": "john@example.com"}}'
```

## Homomorphic Encryption

Homomorphic encryption allows computations to be performed on encrypted data without decrypting it first.

### Key Features:

1. **Encrypted Computation**: Perform operations on encrypted data
2. **Privacy-Preserving Analytics**: Analyze data without exposing it
3. **Mathematical Security**: Based on hard mathematical problems
4. **Scalable Operations**: Support for various homomorphic operations

### API Endpoints:

- `/api/he/generate-keys` - Generate homomorphic encryption keys
- `/api/he/encrypt/int` - Encrypt integer values
- `/api/he/encrypt/float` - Encrypt float values
- `/api/he/decrypt` - Decrypt homomorphically encrypted values
- `/api/he/add` - Perform homomorphic addition
- `/api/he/multiply` - Perform homomorphic multiplication

### Usage Example:

```bash
# Generate keys
curl http://localhost:8000/api/he/generate-keys

# Encrypt values
curl -X POST http://localhost:8000/api/he/encrypt/int -H "Content-Type: application/json" -d '{"value": 15, "public_key": "PUBLIC_KEY"}'

# Perform homomorphic addition
curl -X POST http://localhost:8000/api/he/add -H "Content-Type: application/json" -d '{"encrypted_a": {"encrypted_value": "ENC_VALUE_A"}, "encrypted_b": {"encrypted_value": "ENC_VALUE_B"}}'

# Decrypt result
curl -X POST http://localhost:8000/api/he/decrypt -H "Content-Type: application/json" -d '{"encrypted_value": {"encrypted_value": "ENC_RESULT"}, "private_key": "PRIVATE_KEY"}'
```

## AI Privacy Protection

AI privacy protection features help users opt out of AI training data harvesting and protect against AI-based data analysis.

### Key Features:

1. **AI Training Opt-Out**: Prevent data from being used for AI model training
2. **Privacy Headers**: HTTP headers that signal AI systems to respect privacy
3. **Data Usage Controls**: Granular control over how data is used for AI
4. **Privacy Reporting**: Track and audit AI data usage

### API Endpoints:

- `/api/ai/opt-out` - Set AI training data opt-out preference
- `/api/ai/opt-out/status` - Get AI training data opt-out status
- `/api/ai/privacy-report` - Get AI privacy report
- `/api/ai/training-job` - Start AI training jobs with privacy controls

### Privacy Headers:

The server automatically adds these headers to all responses:
- `X-AI-Training-Opt-Out: true`
- `X-No-AI-Model-Training: true`
- `X-No-Machine-Learning: true`
- `X-AI-Respect-Privacy: true`
- `X-Do-Not-Train: true`
- `X-Do-Not-Profile: true`

### Usage Example:

```bash
# Set AI opt-out preference
curl -H "Authorization: Bearer JWT_TOKEN" -X POST http://localhost:8000/api/ai/opt-out -H "Content-Type: application/json" -d '{"opt_out": true}'

# Get AI opt-out status
curl -H "Authorization: Bearer JWT_TOKEN" http://localhost:8000/api/ai/opt-out/status

# Get AI privacy report
curl -H "Authorization: Bearer JWT_TOKEN" http://localhost:8000/api/ai/privacy-report
```

## Privacy Budget Management

Privacy budget management allows users to track and control their differential privacy consumption.

### Key Features:

1. **Budget Tracking**: Monitor privacy consumption across queries
2. **Usage History**: Track all privacy-consuming operations
3. **Budget Suggestions**: Get recommendations for optimal epsilon values
4. **Budget Reset**: Reset privacy budget when appropriate

### API Endpoints:

- `/api/privacy/budget` - Get current privacy budget status
- `/api/privacy/budget/history` - Get privacy budget usage history
- `/api/privacy/budget/suggest` - Get epsilon value suggestions
- `/api/privacy/budget/reset` - Reset privacy budget
- `/api/privacy/budget/consume` - Manually consume privacy budget

### Usage Example:

```bash
# Get current privacy budget
curl -H "Authorization: Bearer JWT_TOKEN" http://localhost:8000/api/privacy/budget

# Get epsilon suggestions
curl -H "Authorization: Bearer JWT_TOKEN" -X POST http://localhost:8000/api/privacy/budget/suggest -H "Content-Type: application/json" -d '{"sensitivity": 1.0}'

# Manually consume privacy budget
curl -H "Authorization: Bearer JWT_TOKEN" -X POST http://localhost:8000/api/privacy/budget/consume -H "Content-Type: application/json" -d '{"epsilon": 0.1, "query_type": "statistical_analysis"}'
```

## Data Expiration

Data expiration features ensure that sensitive data doesn't persist longer than necessary.

### Key Features:

1. **Automatic Cleanup**: Data automatically expires after a set time
2. **Timer-Based Expiration**: Configurable time-to-live for data items
3. **Extension Options**: Extend expiration time when needed
4. **Cancellation**: Cancel expiration for data that needs to be retained

### API Endpoints:

- `/api/data/expiration` - Get information about all expiring data
- `/api/data/expiration/<data_id>` - Get expiration info for specific data
- `/api/data/expiration/<data_id>/cancel` - Cancel expiration for data
- `/api/data/expiration/<data_id>/extend` - Extend expiration time

### Usage Example:

```bash
# Get all expiring data
curl http://localhost:8000/api/data/expiration

# Extend expiration time
curl -X POST http://localhost:8000/api/data/expiration/data123/extend -H "Content-Type: application/json" -d '{"additional_seconds": 3600}'

# Cancel expiration
curl -X POST http://localhost:8000/api/data/expiration/data123/cancel
```

## Traditional Security Features

### Authentication and Authorization

- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: Fine-grained access control
- **Session Management**: Secure session handling

### Input Sanitization and Validation

- **Recursive Sanitization**: Cleans all user inputs to prevent XSS, SQLi, and path traversal
- **Schema Validation**: Validates JSON request bodies against defined schemas
- **Content-Type Checking**: Validates content types for proper handling

### Rate Limiting

- **IP-Based Rate Limiting**: Prevents abuse from single sources
- **User-Based Rate Limiting**: Applies limits to authenticated users
- **Adaptive Throttling**: Adjusts limits based on server load

### Security Headers

Automatically adds crucial HTTP security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: no-referrer-when-downgrade`
- Configurable `Content-Security-Policy`

### Intrusion Detection

- **Pattern Matching**: Detects common attack patterns
- **Suspicious Activity Logging**: Logs potential security incidents
- **Real-Time Blocking**: Blocks detected threats

### Logging and Auditing

- **Separate Security Logs**: Dedicated `security.log` for security events
- **PII Redaction**: Automatically removes sensitive information from logs
- **Comprehensive Audit Trail**: Tracks all server activities

## API Endpoints

### Encryption Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/encrypt` | POST | Encrypts data with end-to-end encryption |
| `/api/decrypt` | POST | Decrypts data with end-to-end encryption |

### Differential Privacy Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/dp/count` | POST | Provides differentially private count |
| `/api/dp/mean` | POST | Provides differentially private mean |

### Zero-Knowledge Encryption Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/zk/generate-key` | GET | Generate client-side encryption key |
| `/api/zk/prepare-storage` | POST | Prepare data for zero-knowledge storage |
| `/api/zk/retrieve-storage` | POST | Retrieve and decrypt data from storage |

### Decentralized Identity Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/did/generate` | GET | Generate DID key pair |
| `/api/did/document` | POST | Create DID document |
| `/api/did/document/<did>` | GET | Get DID document |
| `/api/did/credential/issue` | POST | Issue verifiable credential |
| `/api/did/credential/verify` | POST | Verify verifiable credential |

### Homomorphic Encryption Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/he/generate-keys` | GET | Generate homomorphic encryption keys |
| `/api/he/encrypt/int` | POST | Encrypt integer value |
| `/api/he/encrypt/float` | POST | Encrypt float value |
| `/api/he/decrypt` | POST | Decrypt homomorphically encrypted value |
| `/api/he/add` | POST | Perform homomorphic addition |
| `/api/he/multiply` | POST | Perform homomorphic multiplication |

### AI Privacy Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/ai/opt-out` | POST | Set AI training data opt-out |
| `/api/ai/opt-out/status` | GET | Get AI training data opt-out status |
| `/api/ai/privacy-report` | GET | Get AI privacy report |
| `/api/ai/training-job` | POST | Start AI training job with privacy controls |
| `/api/ai/training-jobs` | GET | Get all AI training jobs |

### Privacy Budget Management Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/privacy/budget` | GET | Get current privacy budget status |
| `/api/privacy/budget/history` | GET | Get privacy budget usage history |
| `/api/privacy/budget/suggest` | POST | Get epsilon value suggestions |
| `/api/privacy/budget/reset` | POST | Reset privacy budget |
| `/api/privacy/budget/consume` | POST | Manually consume privacy budget |

### Data Expiration Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/data/expiration` | GET | Get information about all expiring data |
| `/api/data/expiration/<data_id>` | GET | Get expiration info for specific data |
| `/api/data/expiration/<data_id>/cancel` | POST | Cancel expiration for data |
| `/api/data/expiration/<data_id>/extend` | POST | Extend expiration time |

### Federated Learning Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/fl/initialize` | POST | Initialize global federated learning model |
| `/api/fl/start-round` | POST | Start new federated learning round |
| `/api/fl/submit-update` | POST | Submit client model update |
| `/api/fl/aggregate` | POST | Aggregate client updates |
| `/api/fl/round-status` | POST | Get federated learning round status |
| `/api/fl/client-stats` | GET | Get client participation statistics |

### Authentication Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/login` | POST | JWT authentication endpoint |
| `/api/users` | GET | Protected user data endpoint |

### Utility Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/routes` | GET | Lists all registered API routes |
| `/api/stats` | GET | Provides server statistics |
| `/api/logs` | GET | Accesses server logs (dev mode only) |
| `/api/echo` | POST | Echoes validated JSON payload |

## Best Practices

### For Application Developers

1. **Always Use HTTPS**: Ensure all communications are encrypted in transit
2. **Strong Password Policies**: Encourage users to use strong passwords for encryption
3. **Appropriate Epsilon Values**: Choose epsilon values based on privacy requirements
4. **Input Validation**: Always validate inputs before processing
5. **Regular Updates**: Keep the server updated with security patches

### For Data Protection

1. **Minimize Data Collection**: Only collect data that is absolutely necessary
2. **Data Retention Policies**: Implement clear policies for data retention and deletion
3. **Access Controls**: Implement strict access controls for sensitive data
4. **Regular Audits**: Conduct regular security audits and penetration testing
5. **Incident Response**: Have a plan for responding to security incidents

### For Privacy Preservation

1. **Differential Privacy Budgeting**: Carefully manage epsilon budgets across queries
2. **Data Minimization**: Apply differential privacy to aggregated statistics only
3. **User Consent**: Obtain proper consent for data processing activities
4. **Transparency**: Be transparent about data processing and privacy measures
5. **Privacy Impact Assessments**: Conduct assessments for new features

### For AI Privacy

1. **Respect User Opt-Outs**: Always honor AI training data opt-out preferences
2. **Use Privacy Headers**: Implement and respect AI privacy headers
3. **Minimize AI Data Usage**: Only use necessary data for AI training
4. **Regular Privacy Audits**: Audit AI data usage regularly
5. **Compliance**: Ensure compliance with AI-related privacy regulations

## Conclusion

Nexus HTTP Server provides a comprehensive suite of security and privacy features designed to protect both traditional security concerns and modern privacy requirements. The implementation of end-to-end encryption, differential privacy, zero-knowledge architecture, decentralized identity, homomorphic encryption, and AI privacy protection makes it suitable for applications that require strong privacy guarantees while maintaining usability.