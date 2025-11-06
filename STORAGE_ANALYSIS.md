# Storage Requirements Analysis

## Current Application Storage Needs

### Docker Images (Estimated)
- **Backend Image**: ~3-4GB
  - Python 3.11-slim base: ~1GB
  - PyTorch + transformers: ~2-3GB
  - Slither + Mythril: ~500MB
  - Application code: ~100MB

- **Frontend Image**: ~200-300MB
  - Nginx Alpine: ~50MB
  - React build: ~150-250MB

### System Requirements
- **Ubuntu 22.04**: ~3-4GB
- **Docker Engine**: ~500MB
- **Docker Compose**: ~50MB
- **System logs**: ~1-2GB (grows over time)

### Application Data
- **Analysis logs**: ~100MB-1GB (grows with usage)
- **Docker volumes**: ~500MB-1GB
- **Temporary files**: ~1-2GB

## Storage Recommendations

### Development/Testing: 30GB
```
Base OS:           4GB
Docker Images:     5GB
Dependencies:      15GB
Application:       3GB
Buffer:            3GB
Total:             30GB
```

### Production (Recommended): 50GB
```
Base OS:           4GB
Docker Images:     5GB
Dependencies:      20GB
Application:       8GB
Logs & Data:       5GB
Buffer:            8GB
Total:             50GB
```

### High-Traffic Production: 80GB
```
Base OS:           4GB
Docker Images:     6GB
Dependencies:      25GB
Application:       15GB
Logs & Data:       15GB
Buffer:            15GB
Total:             80GB
```

## Storage Optimization Tips

### 1. Use EBS gp3 (Recommended)
- Better price/performance than gp2
- Configurable IOPS and throughput
- Cost-effective for most workloads

### 2. Docker Image Optimization
```bash
# Clean up unused images
docker system prune -a

# Remove unused volumes
docker volume prune

# Clean up build cache
docker builder prune
```

### 3. Log Management
```bash
# Configure log rotation
sudo nano /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

### 4. Regular Cleanup Script
```bash
#!/bin/bash
# Add to crontab for weekly cleanup
docker system prune -f
docker volume prune -f
find /var/log -name "*.log" -mtime +7 -delete
```

## Cost Analysis (AWS EBS)

### EBS Storage Costs (us-east-1)
- **gp3 (30GB)**: ~$3.00/month
- **gp3 (50GB)**: ~$5.00/month
- **gp3 (80GB)**: ~$8.00/month

### Instance Type Recommendations
- **t3.medium**: 4GB RAM, 2 vCPU (good for development)
- **t3.large**: 8GB RAM, 2 vCPU (recommended for production)
- **c5.large**: 4GB RAM, 2 vCPU (better for CPU-intensive analysis)

## Monitoring Storage Usage

### Check Current Usage
```bash
# Overall disk usage
df -h

# Docker usage
docker system df

# Largest directories
du -sh /* | sort -hr | head -10
```

### Set Up Alerts
```bash
# Create storage monitoring script
#!/bin/bash
USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $USAGE -gt 80 ]; then
    echo "Warning: Disk usage is ${USAGE}%"
    # Send notification or cleanup
fi
```

## Backup Strategy

### Automated Backups
```bash
# Backup important data
tar -czf backup-$(date +%Y%m%d).tar.gz \
    /home/ubuntu/smart-contract-analyzer \
    /var/lib/docker/volumes
```

### EBS Snapshots
- Create snapshots before major updates
- Schedule regular snapshots (daily/weekly)
- Keep snapshots for 30 days

## Troubleshooting Storage Issues

### If Running Out of Space
1. **Check what's using space**:
   ```bash
   du -sh /* | sort -hr
   ```

2. **Clean Docker**:
   ```bash
   docker system prune -a -f
   ```

3. **Clean logs**:
   ```bash
   sudo journalctl --vacuum-time=7d
   ```

4. **Resize EBS volume** (if needed):
   - Stop instance
   - Modify volume size in AWS Console
   - Resize filesystem: `sudo resize2fs /dev/xvda1`




