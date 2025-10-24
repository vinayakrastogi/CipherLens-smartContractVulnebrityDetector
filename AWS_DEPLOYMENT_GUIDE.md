# AWS EC2 Deployment Guide

## Prerequisites

1. **AWS EC2 Instance** (Recommended: t3.medium or larger)
2. **Security Group Configuration**
3. **Domain Name** (optional, for custom domain)

## Step 1: Launch EC2 Instance

### Instance Configuration
- **Instance Type**: t3.medium (2 vCPU, 4 GB RAM) or larger
- **Operating System**: Ubuntu 22.04 LTS
- **Storage**: 20 GB minimum
- **Security Group**: Create with the following rules:
  - SSH (22) - Your IP only
  - HTTP (80) - 0.0.0.0/0
  - HTTPS (443) - 0.0.0.0/0 (if using SSL)
  - Custom TCP (8000) - 0.0.0.0/0 (for backend API)

## Step 2: Connect to EC2 Instance

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

## Step 3: Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again to apply docker group changes
exit
```

## Step 4: Deploy Application

### Option A: Using Git (Recommended)

```bash
# Clone your repository
git clone https://github.com/yourusername/your-repo.git
cd your-repo

# Copy environment file
cp env.production .env

# Edit environment variables
nano .env
# Update HUGGINGFACE_API_TOKEN and other values

# Run deployment script
chmod +x deploy.sh
./deploy.sh
```

### Option B: Upload Files

```bash
# Create project directory
mkdir smart-contract-analyzer
cd smart-contract-analyzer

# Upload your project files using SCP
# scp -i your-key.pem -r /path/to/your/project/* ubuntu@your-ec2-ip:~/smart-contract-analyzer/

# Copy environment file
cp env.production .env

# Edit environment variables
nano .env

# Run deployment
chmod +x deploy.sh
./deploy.sh
```

## Step 5: Configure Environment Variables

Edit the `.env` file with your actual values:

```bash
nano .env
```

Required variables:
- `HUGGINGFACE_API_TOKEN`: Your Hugging Face API token
- `ALLOWED_ORIGINS`: Your domain or EC2 public IP

Example:
```env
HUGGINGFACE_API_TOKEN=hf_your_actual_token_here
ALLOWED_ORIGINS=http://your-ec2-public-ip,https://yourdomain.com
```

## Step 6: Access Your Application

- **Frontend**: `http://your-ec2-public-ip`
- **Backend API**: `http://your-ec2-public-ip:8000`
- **API Documentation**: `http://your-ec2-public-ip:8000/docs`

## Step 7: SSL/HTTPS Setup (Optional)

### Using Let's Encrypt with Nginx

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Step 8: Monitoring and Maintenance

### View Logs
```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
```

### Update Application
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up --build -d
```

### Backup
```bash
# Backup volumes
docker run --rm -v smart-contract-analyzer_backend_logs:/data -v $(pwd):/backup ubuntu tar czf /backup/backend_logs.tar.gz -C /data .
```

## Step 9: Performance Optimization

### For High Traffic
1. **Increase Instance Size**: Use t3.large or c5.large
2. **Add Load Balancer**: Use AWS Application Load Balancer
3. **Database**: Consider using RDS for persistent data
4. **CDN**: Use CloudFront for static assets

### Resource Limits
The current configuration includes:
- Backend: 2GB RAM, 1 CPU
- Frontend: 512MB RAM, 0.5 CPU

Adjust in `docker-compose.prod.yml` as needed.

## Troubleshooting

### Common Issues

1. **Port 8000 not accessible**
   - Check security group rules
   - Verify firewall settings

2. **Services not starting**
   - Check logs: `docker-compose -f docker-compose.prod.yml logs`
   - Verify environment variables

3. **Out of memory**
   - Increase instance size
   - Check resource limits in docker-compose.prod.yml

4. **SSL certificate issues**
   - Verify domain DNS settings
   - Check nginx configuration

### Health Checks
```bash
# Check backend
curl http://localhost:8000/health

# Check frontend
curl http://localhost/health

# Check container status
docker-compose -f docker-compose.prod.yml ps
```

## Security Considerations

1. **Firewall**: Only open necessary ports
2. **SSH**: Use key-based authentication only
3. **Updates**: Regularly update system and Docker images
4. **Monitoring**: Set up CloudWatch or similar monitoring
5. **Backups**: Regular backups of important data

## Cost Optimization

1. **Instance Type**: Start with t3.medium, scale as needed
2. **Storage**: Use EBS gp3 for better price/performance
3. **Reserved Instances**: For long-term usage
4. **Spot Instances**: For development/testing

## Support

For issues:
1. Check application logs
2. Verify environment variables
3. Test individual services
4. Review AWS CloudWatch logs
