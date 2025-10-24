from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from app.models.schemas import (
    ContractAnalysisRequest, ContractAnalysisResponse, 
    HealthResponse, RiskLevel
)
from app.services.slither_service import SlitherService
from app.services.mythril_service import MythrilService
from app.services.ml_service import MLService
from app.services.risk_classifier import RiskClassifier
from app.utils.helpers import (
    generate_analysis_id, get_current_timestamp, 
    validate_solidity_code, sanitize_contract_name
)

# Initialize FastAPI app
app = FastAPI(
    title="Smart Contract Vulnerability Detection API",
    description="Unified risk classification system combining Slither, Mythril, and ML analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
# Get allowed origins from environment variable or use defaults
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
slither_service = SlitherService()
mythril_service = MythrilService()
ml_service = MLService()
risk_classifier = RiskClassifier()

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Smart Contract Vulnerability Detection API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    services_status = {}
    
    # Check if analysis tools are available
    try:
        # Test Slither availability
        process = await asyncio.create_subprocess_exec(
            'slither', '--version',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()
        services_status["slither"] = "available" if process.returncode == 0 else "unavailable"
    except:
        services_status["slither"] = "unavailable"
    
    try:
        # Test Mythril availability
        process = await asyncio.create_subprocess_exec(
            'myth', 'version',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()
        services_status["mythril"] = "available" if process.returncode == 0 else "unavailable"
    except:
        services_status["mythril"] = "unavailable"
    
    services_status["ml_model"] = "available"  # Assume available for now
    services_status["api"] = "healthy"
    
    return HealthResponse(
        status="healthy",
        timestamp=get_current_timestamp(),
        services=services_status
    )

@app.post("/analyze", response_model=ContractAnalysisResponse)
async def analyze_contract(request: ContractAnalysisRequest):
    """
    Analyze a smart contract for vulnerabilities using multiple tools
    """
    start_time = asyncio.get_event_loop().time()
    
    # Validate input
    is_valid, error_message = validate_solidity_code(request.code)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    # Sanitize contract name
    contract_name = sanitize_contract_name(request.contract_name)
    
    # Generate analysis ID
    analysis_id = generate_analysis_id()
    
    # Initialize results
    slither_result = None
    mythril_result = None
    ml_result = None
    
    # Run analyses in parallel
    tasks = []
    
    if request.include_slither:
        tasks.append(("slither", slither_service.analyze_contract(request.code, contract_name)))
    
    if request.include_mythril:
        tasks.append(("mythril", mythril_service.analyze_contract(request.code, contract_name)))
    
    if request.include_ml:
        tasks.append(("ml", ml_service.analyze_contract(request.code, contract_name)))
    
    # Execute all analyses
    if tasks:
        results = await asyncio.gather(*[task[1] for task in tasks], return_exceptions=True)
        
        for i, (tool_name, result) in enumerate(zip([task[0] for task in tasks], results)):
            if isinstance(result, Exception):
                continue  # Skip failed analyses
            
            if tool_name == "slither":
                slither_result = result
            elif tool_name == "mythril":
                mythril_result = result
            elif tool_name == "ml":
                ml_result = result
    
    # Classify risk
    risk_level, risk_score, summary, recommendations = risk_classifier.classify_risk(
        slither_result, mythril_result, ml_result
    )
    
    # Calculate total execution time
    total_execution_time = asyncio.get_event_loop().time() - start_time
    
    # Create response
    response = ContractAnalysisResponse(
        contract_name=contract_name,
        analysis_id=analysis_id,
        timestamp=get_current_timestamp(),
        slither_result=slither_result,
        mythril_result=mythril_result,
        ml_result=ml_result,
        final_risk_level=risk_level,
        risk_score=risk_score,
        summary=summary,
        recommendations=recommendations,
        total_execution_time=total_execution_time
    )
    
    return response

@app.get("/tools/status")
async def get_tools_status():
    """Get status of all analysis tools"""
    status = {}
    
    # Check Slither
    try:
        process = await asyncio.create_subprocess_exec(
            'slither', '--version',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        status["slither"] = {
            "available": process.returncode == 0,
            "version": stdout.decode().strip() if process.returncode == 0 else "Unknown"
        }
    except Exception as e:
        status["slither"] = {"available": False, "error": str(e)}
    
    # Check Mythril
    try:
        process = await asyncio.create_subprocess_exec(
            'myth', 'version',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        status["mythril"] = {
            "available": process.returncode == 0,
            "version": stdout.decode().strip() if process.returncode == 0 else "Unknown"
        }
    except Exception as e:
        status["mythril"] = {"available": False, "error": str(e)}
    
    # ML model status
    status["ml_model"] = {
        "available": True,
        "model": "rastogivinayak/cipher-lens",
        "note": "Hugging Face API integration"
    }
    
    return status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
