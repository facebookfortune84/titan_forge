# TitanForge Secrets Management Guide

**CRITICAL:** Never commit `.env` files with real credentials to version control. This guide explains how to securely manage secrets.

---

## Option 1: AWS Secrets Manager (Recommended for Production)

### Setup

1. **Install AWS CLI:**
   ```bash
   pip install boto3
   ```

2. **Create secret in AWS:**
   ```bash
   aws secretsmanager create-secret \
     --name titanforge/prod \
     --secret-string file://secrets.json
   ```

3. **Secrets JSON format:**
   ```json
   {
     "DATABASE_URL": "postgresql://user:password@host/db",
     "STRIPE_API_KEY": "sk_live_...",
     "OPENAI_API_KEY": "sk-...",
     "SECRET_KEY": "your-jwt-secret"
   }
   ```

### Load in Application

**File:** `titanforge_backend/app/core/config.py`

```python
import boto3
import json
from functools import lru_cache

@lru_cache()
def get_secrets():
    client = boto3.client('secretsmanager')
    try:
        response = client.get_secret_value(SecretId='titanforge/prod')
        return json.loads(response['SecretString'])
    except Exception as e:
        print(f"Error loading secrets: {e}")
        return {}

# Use in settings
secrets = get_secrets()
DATABASE_URL = secrets.get('DATABASE_URL')
STRIPE_API_KEY = secrets.get('STRIPE_API_KEY')
```

---

## Option 2: HashiCorp Vault (Flexible, Open Source)

### Setup (Docker)

```bash
# Start Vault
docker run --cap-add=IPC_LOCK -d \
  -p 8200:8200 \
  -e VAULT_DEV_ROOT_TOKEN_ID=dev-token \
  vault:latest

# Set Vault address
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='dev-token'

# Store secret
vault kv put secret/titanforge/prod \
  DATABASE_URL="postgresql://..." \
  STRIPE_API_KEY="sk_live_..." \
  OPENAI_API_KEY="sk-..."
```

### Load in Application

```python
import hvac

@lru_cache()
def get_secrets():
    client = hvac.Client(url='http://vault:8200', token='your-token')
    response = client.secrets.kv.read_secret_version(path='titanforge/prod')
    return response['data']['data']

secrets = get_secrets()
```

---

## Option 3: Environment File per Environment (Development)

### Setup

Create separate `.env` files:

```
.env.local       # Local development (never commit)
.env.staging     # Staging environment
.env.production  # Production (never commit)
```

### Load in Application

**File:** `titanforge_backend/app/core/config.py`

```python
from pathlib import Path
from dotenv import load_dotenv
import os

env = os.getenv('ENV', 'development')
env_file = Path(f'.env.{env}')

if env_file.exists():
    load_dotenv(env_file)
else:
    load_dotenv('.env.example')  # Use example as fallback

DATABASE_URL = os.getenv('DATABASE_URL')
STRIPE_API_KEY = os.getenv('STRIPE_API_KEY')
```

### .gitignore (prevent accidental commits)

```
.env
.env.local
.env.*.local
!.env.example
```

---

## Option 4: Docker Secrets (For Docker Swarm/Compose)

### Setup

**File:** `docker-compose.prod.yml`

```yaml
version: '3.8'

services:
  backend:
    image: titanforge-backend:prod
    environment:
      DATABASE_URL: /run/secrets/db_url
      STRIPE_API_KEY: /run/secrets/stripe_key
    secrets:
      - db_url
      - stripe_key

secrets:
  db_url:
    file: ./secrets/DATABASE_URL
  stripe_key:
    file: ./secrets/STRIPE_API_KEY
```

### Load in Application

```python
def load_secret(secret_name):
    try:
        with open(f'/run/secrets/{secret_name}') as f:
            return f.read().strip()
    except FileNotFoundError:
        return os.getenv(secret_name)

DATABASE_URL = load_secret('db_url')
STRIPE_API_KEY = load_secret('stripe_key')
```

---

## Implementation Checklist

### Before Development
- [ ] Copy `.env.example` to `.env`
- [ ] Fill in development values
- [ ] Add `.env` to `.gitignore`
- [ ] Never commit `.env`
- [ ] Use test credentials (Stripe test keys, etc.)

### Before Staging
- [ ] Set up AWS Secrets Manager or Vault
- [ ] Store staging credentials securely
- [ ] Configure application to load from vault
- [ ] Test credential loading works
- [ ] Document credential rotation process

### Before Production
- [ ] Set up production vault
- [ ] Use live credentials (Stripe live keys, etc.)
- [ ] Enable audit logging on vault
- [ ] Implement credential rotation (90-day rotation recommended)
- [ ] Set up monitoring/alerts for unauthorized access
- [ ] Document backup/recovery procedures

---

## Rotating Credentials

### Weekly Checklist

```bash
# Check last rotation date
aws secretsmanager describe-secret --secret-id titanforge/prod

# Rotate if needed
aws secretsmanager rotate-secret --secret-id titanforge/prod

# Verify new credentials work
pytest tests/test_stripe_integration.py
pytest tests/test_database_connection.py
```

### Process

1. Generate new credentials in target service (Stripe, AWS, etc.)
2. Update secret in vault
3. Deploy application with config reload
4. Monitor for errors
5. Revoke old credentials

---

## Security Best Practices

### Credential Management

- ✅ **Do:**
  - Store credentials in vault, not code
  - Rotate credentials regularly (90 days)
  - Use service accounts with minimal permissions
  - Audit all credential access
  - Use different credentials per environment
  - Enable MFA on vault access

- ❌ **Don't:**
  - Commit credentials to git
  - Hardcode secrets in code
  - Share credentials via Slack/email
  - Use same credentials across environments
  - Store credentials in logs
  - Use production credentials in development

### Local Development

```bash
# Securely generate strong passwords
openssl rand -base64 32

# Generate JWT secret
python -c "import secrets; print(secrets.token_hex(32))"

# Never log credentials
export SECRET_KEY=$(openssl rand -hex 32)
echo "SECRET_KEY=***" > .env  # Mask in logs
```

### Production Deployment

```bash
# Load from vault before starting
export VAULT_ADDR=https://vault.yourdomain.com
export VAULT_TOKEN=$(aws secretsmanager get-secret-value \
  --secret-id vault-token \
  --query SecretString \
  --output text)

# Start application
uvicorn app.main:app
```

---

## Testing with Secrets

### Unit Tests (use mock/test credentials)

```python
import os
os.environ['STRIPE_API_KEY'] = 'sk_test_fake_key_for_testing'
os.environ['DATABASE_URL'] = 'sqlite:///test.db'

def test_stripe_integration():
    # Use test key - no real charges
    assert settings.STRIPE_API_KEY.startswith('sk_test_')
```

### Integration Tests (use separate test vault)

```bash
# Create test secret
vault kv put secret/titanforge/test \
  STRIPE_API_KEY="sk_test_..." \
  DATABASE_URL="postgresql://test:test@localhost/test_db"

# Run tests with test credentials
ENV=test pytest tests/
```

---

## Troubleshooting

### "Permission denied" accessing vault

```
Solution:
1. Verify IAM role/policy has secretsmanager:GetSecretValue
2. Check IP whitelist in vault
3. Verify token hasn't expired
4. Check CloudTrail for denied requests
```

### "Secret not found"

```
Solution:
1. Verify secret name matches exactly
2. Check correct AWS region: aws secretsmanager list-secrets --region us-east-1
3. Verify secret path in code
4. Check IAM permissions
```

### "Connection refused" to vault

```
Solution:
1. Verify Vault is running: curl http://vault:8200/v1/sys/health
2. Check network connectivity: ping vault
3. Verify VAULT_ADDR is correct
4. Check firewall rules
```

---

## Recommended Setup for TitanForge

### Development
- Use `.env.local` with test credentials
- Use Stripe test mode
- Use local PostgreSQL

### Staging
- Use AWS Secrets Manager
- Use Stripe test mode
- Rotate credentials monthly
- Enable audit logging

### Production
- Use AWS Secrets Manager with encryption
- Use Stripe live mode
- Rotate credentials every 90 days
- Enable CloudTrail logging
- Set up alerts for unauthorized access

---

## Resources

- **AWS Secrets Manager:** https://aws.amazon.com/secrets-manager/
- **HashiCorp Vault:** https://www.vaultproject.io/
- **12-Factor App (Config):** https://12factor.net/config
- **OWASP Secrets Management:** https://cheatsheetseries.owasp.org/

---

## Questions?

For credential management questions, consult:
1. Your organization's security team
2. The service provider's documentation
3. OWASP secrets management best practices
4. Security engineers on your team
