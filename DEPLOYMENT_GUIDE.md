# 🚀 Nazava Analytics Platform - Deployment Guide

## 📋 Prerequisites

### 1. Shopee API Credentials
You need to register as a Shopee Partner to get:
- `partner_id` - Your Shopee partner ID
- `partner_key` - Your API secret key
- `shop_id` - Your shop identifier
- `access_token` - OAuth access token

**How to get credentials:**
1. Go to https://open.shopee.com/
2. Register as a Shopee Partner
3. Create a new app
4. Get your credentials from the dashboard

### 2. AWS Account
- AWS account with appropriate permissions
- AWS CLI installed and configured
- IAM role with necessary permissions

### 3. Database (Optional but Recommended)
- PostgreSQL database (AWS RDS recommended)
- Redis cache (AWS ElastiCache recommended)

---

## 🔧 Step 1: Environment Configuration

### Create `.env` file

```bash
# Shopee API Credentials
SHOPEE_PARTNER_ID=your_partner_id_here
SHOPEE_PARTNER_KEY=your_partner_key_here
SHOPEE_SHOP_ID=your_shop_id_here
SHOPEE_ACCESS_TOKEN=your_access_token_here

# Database Configuration (Optional)
DATABASE_URL=postgresql://user:password@host:5432/nazava_db
REDIS_URL=redis://host:6379

# AWS Configuration
AWS_REGION=ap-southeast-1
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret

# Application Settings
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=your_secret_key_here
```

### Update API Client Configuration

Edit `automation/shopee_api_client.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize with environment variables
api_client = ShopeeAPIClient(
    partner_id=os.getenv('SHOPEE_PARTNER_ID'),
    partner_key=os.getenv('SHOPEE_PARTNER_KEY'),
    shop_id=os.getenv('SHOPEE_SHOP_ID')
)
api_client.access_token = os.getenv('SHOPEE_ACCESS_TOKEN')
```

---

## 🐳 Step 2: Docker Deployment (Recommended)

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  dashboard:
    build: .
    ports:
      - "8501:8501"
    environment:
      - SHOPEE_PARTNER_ID=${SHOPEE_PARTNER_ID}
      - SHOPEE_PARTNER_KEY=${SHOPEE_PARTNER_KEY}
      - SHOPEE_SHOP_ID=${SHOPEE_SHOP_ID}
      - SHOPEE_ACCESS_TOKEN=${SHOPEE_ACCESS_TOKEN}
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  automation-bot:
    build: .
    command: python automation/bot_scheduler.py
    environment:
      - SHOPEE_PARTNER_ID=${SHOPEE_PARTNER_ID}
      - SHOPEE_PARTNER_KEY=${SHOPEE_PARTNER_KEY}
      - SHOPEE_SHOP_ID=${SHOPEE_SHOP_ID}
      - SHOPEE_ACCESS_TOKEN=${SHOPEE_ACCESS_TOKEN}
    restart: unless-stopped

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=nazava_db
      - POSTGRES_USER=nazava
      - POSTGRES_PASSWORD=secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Build and Run

```bash
# Build Docker image
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## ☁️ Step 3: AWS Deployment

### Option A: AWS EC2 Deployment

#### 1. Launch EC2 Instance

```bash
# Launch Ubuntu instance (t3.medium recommended)
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.medium \
  --key-name your-key-pair \
  --security-group-ids sg-xxxxx \
  --subnet-id subnet-xxxxx \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=Nazava-Analytics}]'
```

#### 2. Connect and Setup

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository
git clone your-repo-url
cd shopee-analytics-platform

# Create .env file
nano .env
# (Add your credentials)

# Start services
docker-compose up -d
```

#### 3. Configure Security Group

Allow inbound traffic:
- Port 8501 (Streamlit dashboard)
- Port 22 (SSH)
- Port 443 (HTTPS - if using SSL)

### Option B: AWS ECS (Elastic Container Service)

#### 1. Create ECR Repository

```bash
# Create repository
aws ecr create-repository --repository-name nazava-analytics

# Login to ECR
aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin your-account-id.dkr.ecr.ap-southeast-1.amazonaws.com

# Build and push image
docker build -t nazava-analytics .
docker tag nazava-analytics:latest your-account-id.dkr.ecr.ap-southeast-1.amazonaws.com/nazava-analytics:latest
docker push your-account-id.dkr.ecr.ap-southeast-1.amazonaws.com/nazava-analytics:latest
```

#### 2. Create ECS Task Definition

```json
{
  "family": "nazava-analytics",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "dashboard",
      "image": "your-account-id.dkr.ecr.ap-southeast-1.amazonaws.com/nazava-analytics:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "SHOPEE_PARTNER_ID", "value": "your_partner_id"},
        {"name": "SHOPEE_PARTNER_KEY", "value": "your_partner_key"},
        {"name": "SHOPEE_SHOP_ID", "value": "your_shop_id"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/nazava-analytics",
          "awslogs-region": "ap-southeast-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### 3. Create ECS Service

```bash
aws ecs create-service \
  --cluster nazava-cluster \
  --service-name nazava-analytics \
  --task-definition nazava-analytics:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}"
```

### Option C: AWS Lambda + API Gateway (For Bot)

#### 1. Create Lambda Function

```python
# lambda_function.py
import json
import os
from automation.shopee_api_client import AutomatedRecommendationBot, ShopeeAPIClient

def lambda_handler(event, context):
    # Initialize API client
    api_client = ShopeeAPIClient(
        partner_id=os.environ['SHOPEE_PARTNER_ID'],
        partner_key=os.environ['SHOPEE_PARTNER_KEY'],
        shop_id=os.environ['SHOPEE_SHOP_ID']
    )
    
    # Initialize bot
    bot = AutomatedRecommendationBot(api_client)
    
    # Execute automated actions
    # (Your automation logic here)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Automation executed successfully')
    }
```

#### 2. Deploy Lambda

```bash
# Create deployment package
zip -r function.zip lambda_function.py automation/ ml_models/

# Create Lambda function
aws lambda create-function \
  --function-name nazava-automation-bot \
  --runtime python3.11 \
  --role arn:aws:iam::account-id:role/lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip \
  --timeout 300 \
  --memory-size 1024
```

#### 3. Schedule with EventBridge

```bash
# Create rule to run daily
aws events put-rule \
  --name nazava-daily-automation \
  --schedule-expression "cron(0 2 * * ? *)"

# Add Lambda as target
aws events put-targets \
  --rule nazava-daily-automation \
  --targets "Id"="1","Arn"="arn:aws:lambda:region:account-id:function:nazava-automation-bot"
```

---

## 🗄️ Step 4: Database Setup

### PostgreSQL on AWS RDS

```bash
# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier nazava-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username nazava \
  --master-user-password SecurePassword123 \
  --allocated-storage 20 \
  --vpc-security-group-ids sg-xxxxx \
  --db-subnet-group-name your-subnet-group
```

### Initialize Database Schema

```sql
-- Create tables for storing analytics data
CREATE TABLE sales_data (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    total_sales DECIMAL(15,2),
    total_orders INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customer_segments (
    id SERIAL PRIMARY KEY,
    segment_id INTEGER,
    segment_name VARCHAR(100),
    customer_count INTEGER,
    avg_order_value DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE automation_log (
    id SERIAL PRIMARY KEY,
    action_type VARCHAR(50),
    action_details JSONB,
    status VARCHAR(20),
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_sales_date ON sales_data(date);
CREATE INDEX idx_automation_executed ON automation_log(executed_at);
```

---

## 🔐 Step 5: Security Configuration

### 1. AWS Secrets Manager

```bash
# Store Shopee credentials
aws secretsmanager create-secret \
  --name nazava/shopee/credentials \
  --secret-string '{
    "partner_id":"your_partner_id",
    "partner_key":"your_partner_key",
    "shop_id":"your_shop_id",
    "access_token":"your_access_token"
  }'

# Retrieve in application
import boto3
import json

def get_shopee_credentials():
    client = boto3.client('secretsmanager', region_name='ap-southeast-1')
    response = client.get_secret_value(SecretId='nazava/shopee/credentials')
    return json.loads(response['SecretString'])
```

### 2. SSL/TLS Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d analytics.nazava.com

# Auto-renewal
sudo certbot renew --dry-run
```

### 3. Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name analytics.nazava.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name analytics.nazava.com;

    ssl_certificate /etc/letsencrypt/live/analytics.nazava.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/analytics.nazava.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 📊 Step 6: Monitoring & Logging

### CloudWatch Setup

```bash
# Create log group
aws logs create-log-group --log-group-name /nazava/analytics

# Create metric alarm
aws cloudwatch put-metric-alarm \
  --alarm-name nazava-high-cpu \
  --alarm-description "Alert when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

### Application Monitoring

```python
# Add to your application
import logging
import boto3

# Configure CloudWatch logging
cloudwatch = boto3.client('logs', region_name='ap-southeast-1')

def log_to_cloudwatch(message, level='INFO'):
    cloudwatch.put_log_events(
        logGroupName='/nazava/analytics',
        logStreamName='application',
        logEvents=[{
            'timestamp': int(time.time() * 1000),
            'message': f'[{level}] {message}'
        }]
    )
```

---

## 🔄 Step 7: Continuous Deployment

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to AWS

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ap-southeast-1
    
    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1
    
    - name: Build and push Docker image
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        ECR_REPOSITORY: nazava-analytics
        IMAGE_TAG: ${{ github.sha }}
      run: |
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
    
    - name: Deploy to ECS
      run: |
        aws ecs update-service \
          --cluster nazava-cluster \
          --service nazava-analytics \
          --force-new-deployment
```

---

## ✅ Step 8: Testing Production Deployment

### 1. Health Check Endpoint

```python
# Add to dashboard/app.py
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
```

### 2. Test Shopee API Connection

```bash
# Test API connectivity
curl -X GET "https://your-domain.com/api/test-shopee-connection"
```

### 3. Monitor Logs

```bash
# View CloudWatch logs
aws logs tail /nazava/analytics --follow

# View Docker logs
docker-compose logs -f
```

---

## 📝 Post-Deployment Checklist

- [ ] Shopee API credentials configured
- [ ] Database connected and initialized
- [ ] SSL certificate installed
- [ ] Monitoring and alerts configured
- [ ] Backup strategy implemented
- [ ] Security groups configured
- [ ] Domain name configured
- [ ] Bot scheduler running
- [ ] Health checks passing
- [ ] Documentation updated

---

## 🆘 Troubleshooting

### Common Issues

**Issue: Shopee API authentication fails**
```bash
# Verify credentials
echo $SHOPEE_PARTNER_ID
echo $SHOPEE_SHOP_ID

# Test API connection
python -c "from automation.shopee_api_client import ShopeeAPIClient; print('OK')"
```

**Issue: Dashboard won't start**
```bash
# Check logs
docker-compose logs dashboard

# Restart service
docker-compose restart dashboard
```

**Issue: Database connection fails**
```bash
# Test connection
psql -h your-rds-endpoint -U nazava -d nazava_db

# Check security group
aws ec2 describe-security-groups --group-ids sg-xxxxx
```

---

## 📞 Support

For deployment assistance:
- Check logs: `docker-compose logs -f`
- Review AWS CloudWatch
- Verify environment variables
- Test API connectivity

---

**Deployment Guide Version**: 1.0  
**Last Updated**: November 2025  
**Platform**: Nazava Analytics & Automation Platform
