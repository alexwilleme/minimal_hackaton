# Backend Services

AWS Lambda-based backend API with Cognito authentication.

To install:
```
poetry config virtualenvs.in-project true
poetry install
poetry run pre-commit install
```


## Structure

```
backend/
└── api/              # REST API Lambda function
    ├── lambda_function.py    # Entry point
    ├── router.py             # HTTP routing
    ├── config.py             # Configuration
    ├── constants.py          # Shared constants
    ├── models.py             # Data models
    ├── utils.py              # Utilities
    ├── validation.py         # Validation helpers
    ├── mock_handler.py       # Generic mock endpoint factory
    ├── mock_config.json      # Mock endpoint to S3 mapping
    ├── openapi_spec.py       # OpenAPI 3.0 spec generator
    ├── handlers/             # Endpoint handlers
    │   ├── status.py         # GET /status
    │   ├── chat.py           # POST /chat
    │   └── openapi.py        # GET /openapi.json
    ├── middleware/           # Middleware
    │   ├── error_handler.py
    │   └── logging.py
    ├── mock_data/            # Mock data (uploaded to S3)
    │   ├── users.json
    │   ├── products.json
    │   └── orders.json
    ├── tests/                # Unit tests
    │   ├── test_handlers.py
    │   └── test_validation.py
    ├── requirements.txt
    ├── test_api.sh
    └── README.md
```

## Technology Stack

- **Runtime**: Python 3.12
- **Platform**: AWS Lambda (serverless)
- **API**: AWS API Gateway (REST API)
- **Authentication**: AWS Cognito User Pools (JWT)
- **Logging**: CloudWatch Logs
- **Deployment**: Terraform

## API Service

### Endpoints

The API provides the following authenticated endpoints:

**Core Endpoints**:
- **GET /status** - Health check and authentication test
- **POST /chat** - Chat with AI using AWS Bedrock

**Mock Data Endpoints** (MCP-Ready):
- **GET /users** - List of mock users with roles
- **GET /products** - Mock product catalog
- **GET /orders** - Mock orders with line items
- **GET /openapi.json** - OpenAPI 3.0 specification

All endpoints require authentication via Cognito JWT token in the Authorization header.

**Example Response** (GET /status):
```json
{
  "status": "ok",
  "timestamp": "2025-11-15T12:34:56.789+00:00",
  "version": "1.0",
  "service": "hackathon-api",
  "environment": "demo",
  "user": "username"
}
```

See [api/README.md](api/README.md) for complete API documentation with all endpoints, request/response examples, and MCP integration details.

## Local Development

### Testing Lambda Locally

```bash
cd api/
python3 lambda_function.py
```

Or test with mock event:
```python
import lambda_function

event = {
    'httpMethod': 'GET',
    'path': '/status',
    'requestContext': {
        'authorizer': {
            'claims': {
                'cognito:username': 'testuser'
            }
        }
    }
}

result = lambda_function.lambda_handler(event, None)
print(result)
```

### Dependencies

Python dependencies are defined in `requirements.txt`. Terraform automatically packages them during deployment.

## Deployment

Lambda functions are deployed via Terraform:

```bash
cd ../infra/apps
terraform apply
```

Terraform:
1. Creates Lambda function
2. Packages code with dependencies
3. Configures API Gateway integration
4. Sets up Cognito authorizer
5. Configures IAM roles and policies

## Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTPS + JWT
       ▼
┌─────────────┐
│ API Gateway │
│  (REST API) │
└──────┬──────┘
       │ Cognito JWT validation
       ▼
┌─────────────┐
│   Cognito   │
│  Authorizer │
└──────┬──────┘
       │ Validated request
       ▼
┌─────────────┐
│   Lambda    │
│  Function   │
└──────┬──────┘
       │ Logs
       ▼
┌─────────────┐
│ CloudWatch  │
│    Logs     │
└─────────────┘
```

## Environment Configuration

Lambda receives environment variables from Terraform:
- `ENV` - Environment name (dev, staging, production)
- `CORS_ALLOW_ORIGINS` - Allowed origins for CORS

## Error Handling

The Lambda function includes comprehensive error handling:
- Try-catch blocks for all operations
- Structured JSON error responses
- Detailed error logging
- Appropriate HTTP status codes

Error response format:
```json
{
  "error": "Error Type",
  "message": "Descriptive error message"
}
```

## Security

- **Authentication**: Cognito JWT tokens required
- **CORS**: Configurable allowed origins
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, X-XSS-Protection
- **Encryption**: CloudWatch logs encrypted at rest
- **IAM**: Least privilege execution role

## Logging

Logs are sent to CloudWatch Logs with structured JSON format including:
- Request details (method, path, user)
- Execution time
- Errors with stack traces

View logs:
```bash
# Get log group name from Terraform
cd ../infra/apps
LOG_GROUP=$(terraform output -raw lambda_log_group 2>/dev/null || echo "/aws/lambda/hackathon-api")

# Tail logs
aws logs tail $LOG_GROUP --follow

# Recent logs
aws logs tail $LOG_GROUP --since 10m
```

## Testing

Use the provided test script:
```bash
cd api/
./test_api.sh
```

The script:
1. Gets configuration from Terraform
2. Creates test user (if needed)
3. Authenticates with Cognito
4. Calls API with token
5. Displays response

## Performance

- **Memory**: 256 MB (configurable in Terraform)
- **Timeout**: 30 seconds
- **Cold Start**: ~500ms
- **Warm Execution**: ~10-20ms

## Monitoring

### CloudWatch Metrics
- Invocations
- Duration
- Errors
- Throttles
- Concurrent executions

### CloudWatch Alarms
Configure in Terraform for:
- High error rate
- Increased latency
- Throttling

## Adding New Endpoints

1. **Create handler file** in `handlers/` directory:
```python
# handlers/my_endpoint.py
from models import StatusResponse
from config import config

def handle_my_endpoint(event, username):
    """Handle my custom endpoint"""
    return StatusResponse.create(
        environment=config.ENV,
        user=username
    )
```

2. **Register route** in `lambda_function.py`:
```python
from handlers.my_endpoint import handle_my_endpoint

# Add after other route registrations
router.get('/my-endpoint', handle_my_endpoint)
```

3. **Deploy**:
```bash
cd ../../infra/apps
terraform apply
```

## Best Practices

1. **Stateless Functions**: Don't rely on local storage
2. **Idempotent Operations**: Safe to retry
3. **Environment Variables**: For configuration
4. **Structured Logging**: JSON format with context
5. **Error Handling**: Comprehensive try-catch
6. **Type Hints**: Use Python type annotations
7. **Docstrings**: Document all functions
8. **Small Functions**: Single responsibility

## Common Issues

### Authentication Errors
- Verify JWT token is IdToken (not AccessToken)
- Check token hasn't expired
- Confirm user exists and is confirmed in Cognito

### CORS Errors
- Update `CORS_ALLOW_ORIGINS` in Terraform
- Ensure preflight OPTIONS requests are handled

### Import Errors
- Verify all dependencies in requirements.txt
- Check Python version compatibility

### Timeout Errors
- Increase timeout in Terraform module
- Optimize slow operations
- Consider async processing for long tasks

## Resources

- [Lambda Python Documentation](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)
- [API Gateway Proxy Integration](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html)
- [Cognito JWT Tokens](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-with-identity-providers.html)
