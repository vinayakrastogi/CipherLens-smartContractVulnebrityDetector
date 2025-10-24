#!/bin/bash

# Smart Contract Vulnerability Detection System Setup Script

set -e

echo "🚀 Setting up Smart Contract Vulnerability Detection System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not available. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Check if required tools are available locally (for development)
check_tools() {
    print_status "Checking for analysis tools..."
    
    # Check Slither
    if command -v slither &> /dev/null; then
        print_success "Slither is available"
    else
        print_warning "Slither not found locally. Will use Docker version."
    fi
    
    # Check Mythril
    if command -v myth &> /dev/null; then
        print_success "Mythril is available"
    else
        print_warning "Mythril not found locally. Will use Docker version."
    fi
}

# Setup environment file
setup_env() {
    if [ ! -f .env ]; then
        print_status "Creating environment file..."
        cp env.example .env
        print_warning "Please edit .env file and add your Hugging Face API token"
    else
        print_success "Environment file already exists"
    fi
}

# Build and start services
start_services() {
    print_status "Building and starting services..."
    
    # Build images
    docker compose build
    
    # Start services
    docker compose up -d
    
    print_success "Services started successfully!"
}

# Wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    # Wait for backend
    timeout=60
    while [ $timeout -gt 0 ]; do
        if curl -f http://localhost:8000/health &> /dev/null; then
            print_success "Backend is ready"
            break
        fi
        sleep 2
        timeout=$((timeout-2))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "Backend failed to start within 60 seconds"
        exit 1
    fi
    
    # Wait for frontend
    timeout=30
    while [ $timeout -gt 0 ]; do
        if curl -f http://localhost:3000 &> /dev/null; then
            print_success "Frontend is ready"
            break
        fi
        sleep 2
        timeout=$((timeout-2))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "Frontend failed to start within 30 seconds"
        exit 1
    fi
}

# Show final information
show_info() {
    echo ""
    print_success "🎉 Setup completed successfully!"
    echo ""
    echo "📋 Access Information:"
    echo "  • Frontend: http://localhost:3000"
    echo "  • Backend API: http://localhost:8000"
    echo "  • API Documentation: http://localhost:8000/docs"
    echo ""
    echo "🔧 Management Commands:"
    echo "  • View logs: docker compose logs -f"
    echo "  • Stop services: docker compose down"
    echo "  • Restart services: docker compose restart"
    echo "  • Update services: docker compose pull && docker compose up -d"
    echo ""
    print_warning "Don't forget to add your Hugging Face API token to the .env file!"
}

# Main execution
main() {
    print_status "Starting setup process..."
    
    check_docker
    check_tools
    setup_env
    start_services
    wait_for_services
    show_info
}

# Run main function
main "$@"
