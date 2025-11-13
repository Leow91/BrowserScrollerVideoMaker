# Deployment Guide

Complete guide for deploying the Scroll Video Generator in various environments.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Development Setup](#development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Cloud Deployment](#cloud-deployment)
6. [Configuration](#configuration)
7. [Monitoring](#monitoring)
8. [Troubleshooting](#troubleshooting)

## Quick Start

### Option 1: Local Python (Development)

```bash
# 1. Clone repository
git clone <repository-url>
cd BrowserScrollerVideoMaker

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 4. Install FFmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg
# Windows: choco install ffmpeg

# 5. Start Web GUI
python web_gui.py
```

Access at: http://localhost:7860

### Option 2: Docker (Recommended)

```bash
# 1. Build and start
docker-compose up -d

# 2. Access
# Open http://localhost:7860

# 3. View logs
docker-compose logs -f

# 4. Stop
docker-compose down
```

## Development Setup

### Prerequisites

- Python 3.11+
- FFmpeg
- Git

### Step-by-Step

```bash
# Clone repository
git clone <repository-url>
cd BrowserScrollerVideoMaker

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Generate example .env file
python config.py

# Edit .env file
cp .env.example .env
nano .env

# Run tests (if available)
pytest

# Start development server
python web_gui.py
```

### Development Tools

```bash
# Code formatting
pip install black isort
black .
isort .

# Linting
pip install flake8 pylint
flake8 .
pylint *.py

# Type checking
pip install mypy
mypy .
```

## Docker Deployment

### Build Image

```bash
# Build image
docker build -t scroll-video-gen:latest .

# Test image
docker run -p 7860:7860 scroll-video-gen:latest
```

### Docker Compose

```bash
# Start services
docker-compose up -d

# Scale workers (if you add worker service)
docker-compose up -d --scale worker=3

# View logs
docker-compose logs -f scroll-video-gen

# Stop services
docker-compose down

# Remove volumes (WARNING: deletes data)
docker-compose down -v
```

### Custom Configuration

Create `.env` file:

```bash
# GUI Settings
GUI_HOST=0.0.0.0
GUI_PORT=7860
GUI_SHARE=false

# Performance
MAX_CONCURRENT_JOBS=5

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/app.log

# Video Settings
DEFAULT_DURATION=15
DEFAULT_WIDTH=1920
DEFAULT_HEIGHT=1080
FFMPEG_CRF=23
FFMPEG_PRESET=medium
```

Then:

```bash
docker-compose --env-file .env up -d
```

### Volume Management

```bash
# Backup workflows
docker cp scroll-video-generator:/app/workflows ./backup/workflows

# Backup output videos
docker cp scroll-video-generator:/app/output ./backup/output

# Restore workflows
docker cp ./backup/workflows scroll-video-generator:/app/workflows
```

## Production Deployment

### System Requirements

**Minimum:**
- 2 CPU cores
- 4 GB RAM
- 20 GB disk
- Ubuntu 20.04+

**Recommended:**
- 4+ CPU cores
- 8+ GB RAM
- 100+ GB SSD
- Ubuntu 22.04 LTS

### Production Setup (Ubuntu)

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install dependencies
sudo apt install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    ffmpeg \
    nginx \
    certbot \
    python3-certbot-nginx

# 3. Create app user
sudo useradd -m -s /bin/bash scrollvideo
sudo su - scrollvideo

# 4. Clone and setup
git clone <repository-url> /home/scrollvideo/app
cd /home/scrollvideo/app
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# 5. Configure environment
cp .env.example .env
nano .env

# 6. Create systemd service
exit  # Exit to root user
```

Create `/etc/systemd/system/scroll-video-gen.service`:

```ini
[Unit]
Description=Scroll Video Generator Web GUI
After=network.target

[Service]
Type=simple
User=scrollvideo
Group=scrollvideo
WorkingDirectory=/home/scrollvideo/app
Environment="PATH=/home/scrollvideo/app/venv/bin"
ExecStart=/home/scrollvideo/app/venv/bin/python web_gui.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable scroll-video-gen
sudo systemctl start scroll-video-gen
sudo systemctl status scroll-video-gen
```

### Nginx Reverse Proxy

Create `/etc/nginx/sites-available/scroll-video-gen`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:7860;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support for Gradio
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Timeouts for long-running operations
        proxy_connect_timeout 3600;
        proxy_send_timeout 3600;
        proxy_read_timeout 3600;
    }

    # Increase max body size for video uploads
    client_max_body_size 500M;
}
```

Enable and configure SSL:

```bash
sudo ln -s /etc/nginx/sites-available/scroll-video-gen /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

### Firewall Configuration

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Cloud Deployment

### AWS EC2

**1. Launch EC2 Instance:**
- AMI: Ubuntu 22.04 LTS
- Instance Type: t3.medium (minimum) or c5.xlarge (recommended)
- Storage: 50 GB gp3

**2. Security Group:**
- SSH (22): Your IP
- HTTP (80): 0.0.0.0/0
- HTTPS (443): 0.0.0.0/0

**3. Setup:**

```bash
# SSH into instance
ssh -i key.pem ubuntu@<instance-ip>

# Run production setup (see above)
```

**4. Optional: Use EFS for shared storage**

```bash
sudo apt install -y nfs-common
sudo mkdir /mnt/efs
sudo mount -t nfs4 <efs-dns-name>:/ /mnt/efs

# Update .env
OUTPUT_DIR=/mnt/efs/output
WORKFLOW_DIR=/mnt/efs/workflows
```

### Google Cloud Platform (GCP)

**1. Create VM:**

```bash
gcloud compute instances create scroll-video-gen \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --machine-type=n2-standard-4 \
    --boot-disk-size=50GB \
    --tags=http-server,https-server
```

**2. Setup firewall:**

```bash
gcloud compute firewall-rules create allow-http \
    --allow tcp:80 \
    --target-tags http-server

gcloud compute firewall-rules create allow-https \
    --allow tcp:443 \
    --target-tags https-server
```

**3. SSH and setup:**

```bash
gcloud compute ssh scroll-video-gen

# Run production setup
```

### Digital Ocean

**1. Create Droplet:**
- Choose Ubuntu 22.04
- Select plan: 4 GB / 2 vCPUs ($24/mo) or higher
- Add block storage (optional)

**2. Setup:**

```bash
# SSH into droplet
ssh root@<droplet-ip>

# Run production setup
```

### Kubernetes (Advanced)

Create `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: scroll-video-gen
spec:
  replicas: 3
  selector:
    matchLabels:
      app: scroll-video-gen
  template:
    metadata:
      labels:
        app: scroll-video-gen
    spec:
      containers:
      - name: app
        image: scroll-video-gen:latest
        ports:
        - containerPort: 7860
        env:
        - name: GUI_HOST
          value: "0.0.0.0"
        volumeMounts:
        - name: workflows
          mountPath: /app/workflows
        - name: output
          mountPath: /app/output
        resources:
          requests:
            cpu: "1"
            memory: "2Gi"
          limits:
            cpu: "2"
            memory: "4Gi"
      volumes:
      - name: workflows
        persistentVolumeClaim:
          claimName: workflows-pvc
      - name: output
        persistentVolumeClaim:
          claimName: output-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: scroll-video-gen-service
spec:
  selector:
    app: scroll-video-gen
  ports:
  - port: 80
    targetPort: 7860
  type: LoadBalancer
```

Deploy:

```bash
kubectl apply -f k8s-deployment.yaml
```

## Configuration

### Environment Variables

Create `.env` file:

```bash
# Application
APP_NAME=Scroll Video Generator
DEBUG=false

# Video Settings
DEFAULT_DURATION=15
DEFAULT_WIDTH=1920
DEFAULT_HEIGHT=1080
DEFAULT_FPS=30

# FFmpeg
FFMPEG_CRF=23
FFMPEG_PRESET=medium

# Browser
BROWSER_HEADLESS=true
BROWSER_TIMEOUT=60000

# Paths
WORKFLOW_DIR=workflows
OUTPUT_DIR=output
TEMP_DIR=temp

# Performance
MAX_CONCURRENT_JOBS=3

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# GUI
GUI_HOST=127.0.0.1
GUI_PORT=7860
GUI_SHARE=false

# Security
# ALLOWED_DOMAINS=example.com,mysite.com
BLOCKED_DOMAINS=localhost,127.0.0.1,0.0.0.0
```

### Advanced Configuration

For complex setups, edit `config.py` directly or use a custom config file:

```python
from config import AppConfig

custom_config = AppConfig(
    _env_file="custom.env",
    max_concurrent_jobs=10,
    ffmpeg_crf=18,  # Higher quality
)
```

## Monitoring

### Logs

```bash
# View logs
tail -f logs/app.log

# View last 100 lines
tail -n 100 logs/app.log

# View errors only
grep ERROR logs/app.log
```

### System Resources

```bash
# Monitor CPU/Memory
htop

# Monitor disk usage
df -h

# Monitor specific process
ps aux | grep python
```

### Prometheus + Grafana (Advanced)

```yaml
# docker-compose-monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

## Troubleshooting

### Common Issues

**1. FFmpeg not found**

```bash
# Install FFmpeg
sudo apt install ffmpeg  # Linux
brew install ffmpeg      # macOS
choco install ffmpeg     # Windows
```

**2. Playwright browser not found**

```bash
playwright install chromium
playwright install-deps chromium
```

**3. Permission denied**

```bash
chmod +x *.py
chown -R appuser:appuser /app
```

**4. Out of memory**

```bash
# Increase swap
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**5. Port already in use**

```bash
# Find process using port
sudo lsof -i :7860

# Kill process
kill -9 <PID>

# Or change port in .env
GUI_PORT=7861
```

### Debug Mode

```bash
# Enable debug logging
export DEBUG=true
export LOG_LEVEL=DEBUG

# Run with debug
python web_gui.py
```

### Health Checks

```bash
# Check service status
systemctl status scroll-video-gen

# Check if port is listening
netstat -tulpn | grep 7860

# Test endpoint
curl http://localhost:7860

# Check disk space
df -h

# Check memory
free -h
```

## Backup & Restore

### Backup

```bash
# Create backup directory
mkdir -p backups/$(date +%Y%m%d)

# Backup workflows
cp -r workflows backups/$(date +%Y%m%d)/

# Backup output
cp -r output backups/$(date +%Y%m%d)/

# Backup config
cp .env backups/$(date +%Y%m%d)/

# Create archive
tar -czf backup-$(date +%Y%m%d).tar.gz backups/$(date +%Y%m%d)/
```

### Restore

```bash
# Extract backup
tar -xzf backup-20250113.tar.gz

# Restore workflows
cp -r backups/20250113/workflows .

# Restore output
cp -r backups/20250113/output .

# Restore config
cp backups/20250113/.env .
```

### Automated Backups

Create `/etc/cron.daily/backup-scroll-video-gen`:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_DIR="/backups/scroll-video-gen"
APP_DIR="/home/scrollvideo/app"

mkdir -p $BACKUP_DIR

# Backup workflows and output
tar -czf $BACKUP_DIR/backup-$DATE.tar.gz \
    $APP_DIR/workflows \
    $APP_DIR/output \
    $APP_DIR/.env

# Keep only last 7 days
find $BACKUP_DIR -name "backup-*.tar.gz" -mtime +7 -delete
```

Make executable:

```bash
sudo chmod +x /etc/cron.daily/backup-scroll-video-gen
```

## Performance Tuning

### For High Load

```bash
# Increase file descriptors
ulimit -n 65536

# Increase max concurrent jobs
MAX_CONCURRENT_JOBS=10

# Use faster FFmpeg preset
FFMPEG_PRESET=fast

# Reduce CRF for smaller files (lower quality)
FFMPEG_CRF=28
```

### For Quality

```bash
# Reduce concurrent jobs
MAX_CONCURRENT_JOBS=2

# Use slower FFmpeg preset
FFMPEG_PRESET=slow

# Increase CRF for better quality
FFMPEG_CRF=18
```

## Security

### Best Practices

1. **Use HTTPS** (Let's Encrypt)
2. **Firewall** (UFW/iptables)
3. **Rate Limiting** (Nginx)
4. **Regular Updates**
5. **Monitoring**
6. **Backups**

### Rate Limiting (Nginx)

```nginx
limit_req_zone $binary_remote_addr zone=videogen:10m rate=10r/m;

location / {
    limit_req zone=videogen burst=5 nodelay;
    proxy_pass http://127.0.0.1:7860;
}
```

## Support

For issues and questions:
- GitHub Issues: <repository-url>/issues
- Documentation: README.md, WORKFLOW_GUIDE.md
- Logs: Check logs/app.log

---

**Last Updated:** 2025-11-13
