# PAANY RAG Reverse Proxy

A FastAPI reverse proxy server designed to be deployed on Render.com that forwards requests to your PAANY RAG system running on AWS Lightsail.

## 🚀 Quick Deploy to Render

### Step 1: Prepare Your Repository
1. Upload this `reverse render` folder to a GitHub repository
2. Make sure all files are in the root of the repository

### Step 2: Deploy on Render
1. Go to [Render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `paany-rag-proxy` (or any name you prefer)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Port**: Leave empty (Render will auto-detect)

### Step 3: Configure Environment Variables
In Render's Environment section, add these variables:

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `AWS_LIGHTSAIL_URL` | `http://YOUR_AWS_IP:8000` | Replace with your AWS Lightsail public IP |
| `PROXY_TOKEN` | `6e8b43cca9d29b261843a3b1c53382bdaa5b2c9e96db92da679278c6dc0042ca` | API token for AWS instance |
| `TIMEOUT_SECONDS` | `120` | Request timeout in seconds |

**Important**: Replace `YOUR_AWS_IP` with your actual AWS Lightsail public IP address.

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait for deployment to complete (usually 2-5 minutes)
3. Your proxy will be available at: `https://your-service-name.onrender.com`

## 📡 API Endpoints

Once deployed, your Render proxy will provide these endpoints:

### Main RAG API
```bash
POST https://your-service-name.onrender.com/api/v1/hackrx/run
```

**Request Body:**
```json
{
  "documents": "Your document text here...",
  "questions": [
    "What is this document about?",
    "What are the key points?"
  ]
}
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer 6e8b43cca9d29b261843a3b1c53382bdaa5b2c9e96db92da679278c6dc0042ca
```

### Health Check Endpoints
- `GET /health` - Basic health check
- `GET /api/health` - Comprehensive health check
- `GET /proxy/health` - Proxy-specific health check

### Status Endpoints
- `GET /redis-status` - Redis connection status
- `GET /performance/stats` - Performance statistics
- `GET /performance/system-info` - System information

### Documentation
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

## 🧪 Testing Your Deployment

### Test 1: Basic Health Check
```bash
curl https://your-service-name.onrender.com/health
```

### Test 2: Proxy Health Check
```bash
curl https://your-service-name.onrender.com/proxy/health
```

### Test 3: Main RAG API
```bash
curl -X POST https://your-service-name.onrender.com/api/v1/hackrx/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 6e8b43cca9d29b261843a3b1c53382bdaa5b2c9e96db92da679278c6dc0042ca" \
  -d '{
    "documents": "Artificial intelligence is a branch of computer science.",
    "questions": ["What is AI?"]
  }'
```

## 🔧 Local Development

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your AWS instance details
# Set AWS_LIGHTSAIL_URL to your AWS instance IP
```

### Run Locally
```bash
python main.py
```

The server will start on `http://localhost:8080`

## 🌍 Architecture

```
Client Request
     ↓
Render Proxy (FastAPI)
     ↓
AWS Lightsail (PAANY RAG System)
     ↓
Response back to Client
```

## 🔐 Security Features

- **Token Authentication**: All requests include proper authorization headers
- **CORS Support**: Configured for cross-origin requests
- **Error Handling**: Comprehensive error handling and logging
- **Timeout Protection**: Configurable request timeouts

## 🚨 Troubleshooting

### Common Issues

1. **502 Bad Gateway**: 
   - Check if your AWS Lightsail instance is running
   - Verify the AWS IP address in environment variables
   - Ensure port 8000 is open in AWS Security Groups

2. **504 Gateway Timeout**:
   - Increase `TIMEOUT_SECONDS` environment variable
   - Check AWS instance performance

3. **401 Unauthorized**:
   - Verify the `PROXY_TOKEN` matches your AWS instance token

4. **Connection Refused**:
   - Ensure AWS Security Group allows inbound traffic on port 8000
   - Check if AWS instance is running: `sudo docker-compose ps`

### Checking AWS Instance Status
```bash
# SSH into your AWS instance
ssh ubuntu@YOUR_AWS_IP

# Check if services are running
sudo docker-compose ps

# Check logs
sudo docker-compose logs -f

# Restart if needed
sudo docker-compose restart
```

## 📝 Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AWS_LIGHTSAIL_URL` | Yes | - | Full URL to your AWS Lightsail instance |
| `PROXY_TOKEN` | Yes | - | API token for authentication |
| `TIMEOUT_SECONDS` | No | `120` | Request timeout in seconds |
| `PORT` | No | `8080` | Server port (auto-set by Render) |

## 📚 Related Documentation

- [Original PAANY RAG System](../paany_instance/README.md)
- [AWS Deployment Guide](../paany_instance/AWS_DEPLOYMENT.md)
- [Render.com Documentation](https://render.com/docs)

## 🎯 Benefits of This Approach

1. **Free Hosting**: Render offers generous free tier
2. **HTTPS**: Automatic SSL certificates
3. **High Availability**: Render's infrastructure is more reliable than keeping AWS instance always on
4. **Cost Optimization**: Turn off AWS instance when not needed
5. **Global CDN**: Faster response times worldwide
6. **Easy Scaling**: Render handles auto-scaling

## 📞 Support

If you encounter issues:
1. Check the Render deployment logs
2. Verify AWS instance is accessible
3. Test direct connection to AWS instance
4. Review environment variables configuration
