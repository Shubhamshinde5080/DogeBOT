#!/bin/bash
# DogeBot Cloud Deployment Script
echo "🚀 DogeBot Cloud Deployment Setup"
echo "=================================="

# Check if we're on a cloud server
if [ -f /.dockerenv ] || [ -n "${container}" ]; then
    echo "🐳 Running in container environment"
else
    echo "💻 Setting up cloud server..."
fi

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "✅ Docker installed"
fi

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    echo "📦 Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose installed"
fi

# Create production environment file
echo "🔧 Setting up production environment..."
cat > .env.production << EOF
# Production DogeBot Configuration
API_KEY=your_binance_api_key_here
API_SECRET=your_binance_api_secret_here
BASE_URL=https://testnet.binance.vision

# Trading Configuration
DAILY_TARGET=6.0
SYMBOL=DOGEFDUSD
GRID_SIZE=300

# Monitoring
LOG_LEVEL=INFO
ENABLE_METRICS=true
EOF

# Create production docker-compose
echo "🐋 Creating production docker-compose..."
cat > docker-compose.prod.yml << EOF
version: '3.8'

services:
  dogebot:
    build: .
    container_name: dogebot-prod
    restart: unless-stopped
    ports:
      - "8000:8000"
    env_file:
      - .env.production
    volumes:
      - ./logs:/app/logs
    networks:
      - dogebot-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    container_name: dogebot-redis-prod
    restart: unless-stopped
    volumes:
      - redis_data:/data
    networks:
      - dogebot-network

volumes:
  redis_data:

networks:
  dogebot-network:
    driver: bridge
EOF

# Create logs directory
mkdir -p logs

# Create startup script
cat > start_bot.sh << 'EOF'
#!/bin/bash
echo "🤖 Starting DogeBot in production mode..."
docker-compose -f docker-compose.prod.yml up -d
echo "✅ DogeBot started!"
echo "📊 Monitor with: docker logs dogebot-prod -f"
echo "🔍 Check status: docker ps | grep dogebot"
EOF

# Create monitoring script
cat > monitor_prod.sh << 'EOF'
#!/bin/bash
echo "🤖 DogeBot Production Monitoring"
echo "==============================="
echo "⏰ $(date)"
echo ""

echo "🐳 Container Status:"
docker ps | grep dogebot
echo ""

echo "📊 Resource Usage:"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" | grep dogebot
echo ""

echo "📝 Recent Logs:"
docker logs dogebot-prod --tail 5
echo ""

echo "💰 Quick Status Check:"
curl -s http://localhost:8000/health 2>/dev/null && echo "✅ Bot API: Healthy" || echo "❌ Bot API: Down"
echo ""
EOF

# Make scripts executable
chmod +x start_bot.sh monitor_prod.sh

echo ""
echo "🎉 Production setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Edit .env.production with your real API keys"
echo "2. Run: ./start_bot.sh"
echo "3. Monitor: ./monitor_prod.sh"
echo "4. View logs: docker logs dogebot-prod -f"
echo ""
echo "🚀 Ready for 24/7 cloud deployment!"
