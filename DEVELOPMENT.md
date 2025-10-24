# Development Guide

## Project Overview

This is a unified smart contract vulnerability detection system that combines:
- **Slither**: Static analysis for common vulnerabilities
- **Mythril**: Symbolic execution for deeper analysis
- **ML Model**: AI-based classification (rastogivinayak/cipher-lens)

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │ Analysis Tools  │
│                 │    │                 │    │                 │
│ • Code Editor   │◄──►│ • API Endpoints │◄──►│ • Slither      │
│ • Results UI    │    │ • Risk Classifier│    │ • Mythril      │
│ • File Upload   │    │ • ML Integration │    │ • ML Model     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- Git

### Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository>
   cd SmartContractVulnebrityDetection/version4
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Manual Development Setup

#### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install analysis tools
pip install slither-analyzer mythril

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## API Endpoints

### Core Endpoints

- `POST /analyze` - Analyze smart contract code
- `GET /health` - Health check
- `GET /tools/status` - Check analysis tools status

### Request Format

```json
{
  "code": "pragma solidity ^0.8.0; contract Example { ... }",
  "contract_name": "Example",
  "include_slither": true,
  "include_mythril": true,
  "include_ml": true
}
```

### Response Format

```json
{
  "contract_name": "Example",
  "analysis_id": "analysis_abc123",
  "timestamp": "2024-01-01T00:00:00Z",
  "slither_result": { ... },
  "mythril_result": { ... },
  "ml_result": { ... },
  "final_risk_level": "High Risk",
  "risk_score": 0.85,
  "summary": "Found 3 critical vulnerabilities",
  "recommendations": [ ... ],
  "total_execution_time": 12.5
}
```

## Risk Classification

The system uses a weighted scoring algorithm:

- **Slither Weight**: 40%
- **Mythril Weight**: 40%  
- **ML Model Weight**: 20%

### Risk Levels

- **High Risk** (≥80%): Critical vulnerabilities detected
- **Moderate Risk** (50-79%): Some security concerns
- **Low Risk** (20-49%): Minor issues or warnings
- **Safe** (<20%): No significant vulnerabilities

## Adding New Analysis Tools

1. Create a new service in `backend/app/services/`
2. Implement the analysis logic
3. Add the service to the main analysis endpoint
4. Update the risk classifier weights

## Frontend Customization

The frontend uses:
- **React 18** with functional components
- **TailwindCSS** for styling
- **Lucide React** for icons
- **Axios** for API calls

### Adding New Components

1. Create component in `frontend/src/components/`
2. Import and use in `App.js`
3. Style with TailwindCSS classes

## Testing

### Backend Testing

```bash
cd backend
python -m pytest tests/
```

### Frontend Testing

```bash
cd frontend
npm test
```

### Integration Testing

```bash
# Test the full stack
docker-compose up -d
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "pragma solidity ^0.8.0; contract Test {}"}'
```

## Deployment

### Production Deployment

1. **Set environment variables**:
   ```bash
   cp env.example .env
   # Edit .env with production values
   ```

2. **Build and deploy**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Environment Variables

- `HUGGINGFACE_API_TOKEN`: Required for ML model access
- `REACT_APP_API_URL`: Frontend API endpoint
- `BACKEND_HOST/PORT`: Backend configuration

## Troubleshooting

### Common Issues

1. **Slither/Mythril not found**:
   - Ensure tools are installed in the Docker container
   - Check the Dockerfile includes the installations

2. **ML model API errors**:
   - Verify Hugging Face API token is set
   - Check model name is correct

3. **Frontend can't connect to backend**:
   - Check CORS settings in backend
   - Verify API URL in frontend

### Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
