#!/bin/bash

# Simple deployment script for Smart Contract Analyzer
set -e

echo "🚀 Starting Smart Contract Analyzer Deployment..."

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check Docker Compose
if ! docker compose version &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    print_warning "Creating .env file..."
    cat > .env << EOF
# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
BACKEND_WORKERS=1

# Frontend Configuration
FRONTEND_PORT=80

# Security
ALLOWED_ORIGINS=http://localhost,http://127.0.0.1

# Logging
LOG_LEVEL=INFO
EOF
    print_warning "Please update .env file if needed."
fi

# Stop existing containers
print_status "Stopping existing containers..."
docker compose -f docker-compose.prod.yml down --remove-orphans 2>/dev/null || true

# Clean up old images (optional)
read -p "Do you want to clean up old Docker images? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Cleaning up old images..."
    docker system prune -f 2>/dev/null || true
fi

# Build and start services
print_status "Building and starting services..."
print_status "This may take 5-10 minutes for first-time setup..."

# Build with verbose output to see any errors
docker compose -f docker-compose.prod.yml up --build -d

# Wait for services
print_status "Waiting for services to start..."
sleep 30

# Check if services are running
print_status "Checking service status..."

# Check backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_status "✅ Backend is healthy"
else
    print_warning "⚠️ Backend may still be starting up..."
    print_status "Backend logs:"
    docker compose -f docker-compose.prod.yml logs backend --tail=20
fi

# Check frontend
if curl -f http://localhost/health > /dev/null 2>&1; then
    print_status "✅ Frontend is healthy"
else
    print_warning "⚠️ Frontend may still be starting up..."
    print_status "Frontend logs:"
    docker compose -f docker-compose.prod.yml logs frontend --tail=20
fi

# Show final status
print_status "🎉 Deployment completed!"
echo
echo "📋 Service Information:"
echo "  Frontend: http://localhost (or your EC2 public IP)"
echo "  Backend API: http://localhost:8000"
echo "  API Documentation: http://localhost:8000/docs"
echo
echo "🔧 Management Commands:"
echo "  View logs: docker compose -f docker-compose.prod.yml logs -f"
echo "  Stop services: docker compose -f docker-compose.prod.yml down"
echo "  Restart services: docker compose -f docker-compose.prod.yml restart"
echo

# Show container status
print_status "Container Status:"
docker compose -f docker-compose.prod.yml ps
