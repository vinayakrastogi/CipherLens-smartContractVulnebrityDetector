# Smart Contract Vulnerability Detection System

A unified risk classification system that combines Slither, Mythril, and ML-based analysis to detect vulnerabilities in smart contracts.

## Features

- **Multi-tool Analysis**: Integrates Slither, Mythril, and custom ML model
- **Risk Classification**: Categorizes contracts as High Risk, Moderate Risk, Low Risk, or Safe
- **Web Interface**: React-based frontend for easy contract analysis
- **REST API**: FastAPI backend for scalable analysis processing
- **Docker Support**: Containerized deployment for easy setup

## Project Structure

```
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI application
│   │   ├── models/         # Pydantic models
│   │   ├── services/       # Analysis services
│   │   └── utils/          # Utility functions
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── utils/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml      # Multi-service orchestration
└── README.md
```

## Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository>
   cd SmartContractVulnebrityDetection/version4
   ```

2. **Run with Docker**:
   ```bash
   docker compose up --build
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Development Setup

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (React)
```bash
cd frontend
npm install
npm start
```

## API Endpoints

- `POST /analyze` - Analyze smart contract code
- `GET /health` - Health check
- `GET /docs` - API documentation

## Risk Classification

The system combines results from:
- **Slither**: Static analysis for common vulnerabilities
- **Mythril**: Symbolic execution for deeper analysis  
- **ML Model**: AI-based classification (rastogivinayak/cipher-lens)

Final risk levels:
- **High Risk**: Critical vulnerabilities detected
- **Moderate Risk**: Some security concerns
- **Low Risk**: Minor issues or warnings
- **Safe**: No significant vulnerabilities found



under developement --> other models being tested
