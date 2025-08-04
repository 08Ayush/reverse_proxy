#!/bin/bash
"""
PAANY RAG Reverse Proxy - Local Development Setup
"""

echo "🚀 PAANY RAG Reverse Proxy Setup"
echo "================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✅ pip3 found"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and set your AWS_LIGHTSAIL_URL"
    echo "   Example: AWS_LIGHTSAIL_URL=http://your-aws-ip:8000"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎯 Setup Complete!"
echo "=================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your AWS Lightsail IP address"
echo "2. Run the proxy: python3 main.py"
echo "3. Test the proxy: python3 test_proxy.py"
echo ""
echo "For Render deployment:"
echo "1. Upload this folder to GitHub"
echo "2. Deploy on Render.com"
echo "3. Set environment variables in Render dashboard"
echo ""
echo "📚 See README.md for detailed instructions"
