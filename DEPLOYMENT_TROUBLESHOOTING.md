# Deployment Troubleshooting Guide

## 🚀 Quick Deployment Steps

### 1. Use the Simple Deployment Script
```bash
# Use the simplified deployment script
./deploy-simple.sh
```

### 2. If That Fails, Manual Steps
```bash
# Stop any existing containers
docker compose -f docker-compose.prod.yml down --remove-orphans

# Clean up Docker
docker system prune -f

# Build and start
docker compose -f docker-compose.prod.yml up --build -d

# Check logs if issues
docker compose -f docker-compose.prod.yml logs -f
```

## 🔧 Common Issues & Solutions

### Issue 1: npm ci fails
**Problem**: `npm ci` requires package-lock.json
**Solution**: Use `npm install` instead (already fixed in Dockerfile)

### Issue 2: Docker Compose not found
**Problem**: Using `docker-compose` instead of `docker compose`
**Solution**: All scripts updated to use `docker compose`

### Issue 3: Frontend build fails
**Problem**: Missing devDependencies for build
**Solution**: Install all dependencies, then build

### Issue 4: Backend dependencies fail
**Problem**: PyTorch/transformers installation issues
**Solution**: Added fallback installation methods

## 📋 Complete Deployment Checklist

### Before Deployment:
- [ ] EC2 instance with 50GB storage
- [ ] Docker installed: `sudo apt install docker.io docker-compose-plugin`
- [ ] User in docker group: `sudo usermod -aG docker $USER`
- [ ] Logout and login again

### Deployment Steps:
1. **Clone repository**:
   ```bash
   git clone <your-repo>
   cd <repo-name>
   ```

2. **Create environment file**:
   ```bash
   cp env.production .env
   # Edit .env if needed (remove HUGGINGFACE_API_TOKEN line)
   ```

3. **Run deployment**:
   ```bash
   chmod +x deploy-simple.sh
   ./deploy-simple.sh
   ```

### After Deployment:
- [ ] Check services: `docker compose -f docker-compose.prod.yml ps`
- [ ] Test frontend: `curl http://localhost/health`
- [ ] Test backend: `curl http://localhost:8000/health`

## 🐛 Debugging Commands

### Check Container Status:
```bash
docker compose -f docker-compose.prod.yml ps
```

### View Logs:
```bash
# All services
docker compose -f docker-compose.prod.yml logs -f

# Specific service
docker compose -f docker-compose.prod.yml logs -f backend
docker compose -f docker-compose.prod.yml logs -f frontend
```

### Restart Services:
```bash
docker compose -f docker-compose.prod.yml restart
```

### Clean Rebuild:
```bash
docker compose -f docker-compose.prod.yml down
docker system prune -f
docker compose -f docker-compose.prod.yml up --build -d
```

## 📊 Expected Build Times

- **First build**: 10-15 minutes (downloading dependencies)
- **Subsequent builds**: 3-5 minutes
- **Backend model download**: 2-3 minutes (one-time)

## 🔍 Health Checks

### Backend Health:
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy",...}
```

### Frontend Health:
```bash
curl http://localhost/health
# Should return: healthy
```

### API Documentation:
```bash
curl http://localhost:8000/docs
# Should return HTML page
```

## 🚨 Emergency Recovery

### If Everything Fails:
```bash
# Nuclear option - clean everything
docker system prune -a -f
docker volume prune -f
docker network prune -f

# Rebuild from scratch
docker compose -f docker-compose.prod.yml up --build -d
```

### If Storage is Full:
```bash
# Check usage
df -h
docker system df

# Clean up
docker system prune -a -f
docker volume prune -f
```

## 📞 Support Commands

### Get System Info:
```bash
# Docker version
docker --version
docker compose version

# System resources
free -h
df -h

# Container status
docker compose -f docker-compose.prod.yml ps
```

### Export Logs:
```bash
# Save logs to file
docker compose -f docker-compose.prod.yml logs > deployment.log 2>&1
```




