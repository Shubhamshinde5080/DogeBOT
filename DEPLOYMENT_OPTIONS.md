# DogeBot Cloud Deployment Guide
# =====================================

## 🌩️ **Option 1: DigitalOcean Droplet ($4/month)**
```bash
# 1. Create a $4/month droplet (512MB RAM, enough for DogeBot)
# 2. SSH into droplet and run:
git clone https://github.com/yourusername/DogeBot.git
cd DogeBot
docker build -t dogebot .
docker run -d --restart=unless-stopped -p 8000:8000 --env-file .env --name dogebot dogebot
```

## ☁️ **Option 2: AWS EC2 Free Tier (Free for 1 year)**
```bash
# 1. Launch t2.micro instance (free tier)
# 2. Install Docker and run:
sudo yum update -y
sudo yum install -y docker git
sudo service docker start
sudo usermod -a -G docker ec2-user
# Upload your code and run container
```

## 🐋 **Option 3: Railway.app (Starts Free)**
```bash
# 1. Connect GitHub repo to Railway
# 2. Railway auto-deploys from Dockerfile
# 3. Add environment variables in Railway dashboard
# 4. Bot runs 24/7 automatically
```

## 🔗 **Option 4: Render.com (Free tier available)**
```bash
# 1. Connect GitHub repo
# 2. Select "Web Service" 
# 3. Use Dockerfile for deployment
# 4. Add environment variables
```

## 💻 **Option 5: Raspberry Pi (One-time cost ~$100)**
```bash
# Run at home 24/7 with minimal power consumption
# Perfect for crypto bots
sudo docker run -d --restart=always --name dogebot dogebot
```

## 🏠 **Option 6: VPS Providers (Cheap options)**
- **Vultr**: $2.50/month
- **Linode**: $5/month  
- **Contabo**: $4/month
- **Hetzner**: €3/month

## ⚡ **Quick Deploy Commands**
```bash
# For any Linux server:
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
git clone [your-repo]
cd DogeBot
docker build -t dogebot .
docker run -d --restart=unless-stopped -p 8000:8000 --env-file .env dogebot
```
