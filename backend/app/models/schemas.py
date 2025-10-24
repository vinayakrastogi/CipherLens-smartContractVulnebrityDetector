from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class RiskLevel(str, Enum):
    HIGH = "High Risk"
    MODERATE = "Moderate Risk"
    LOW = "Low Risk"
    SAFE = "Safe"

class VulnerabilityType(str, Enum):
    REENTRANCY = "reentrancy"
    INTEGER_OVERFLOW = "integer_overflow"
    UNCHECKED_CALL = "unchecked_call"
    ACCESS_CONTROL = "access_control"
    FRONT_RUNNING = "front_running"
    DENIAL_OF_SERVICE = "denial_of_service"
    UNKNOWN = "unknown"

class Vulnerability(BaseModel):
    type: VulnerabilityType
    severity: str  # "high", "medium", "low"
    description: str
    line_number: Optional[int] = None
    confidence: float  # 0.0 to 1.0

class AnalysisResult(BaseModel):
    tool: str
    vulnerabilities: List[Vulnerability]
    summary: str
    execution_time: float
    success: bool
    error_message: Optional[str] = None

class MLPrediction(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    model_name: str
    prediction: str  # "vulnerable" or "safe"
    confidence: float
    features_used: List[str]
    execution_time: float

class ContractAnalysisRequest(BaseModel):
    code: str
    contract_name: Optional[str] = "Contract"
    include_slither: bool = True
    include_mythril: bool = True
    include_ml: bool = True

class ContractAnalysisResponse(BaseModel):
    contract_name: str
    analysis_id: str
    timestamp: str
    slither_result: Optional[AnalysisResult] = None
    mythril_result: Optional[AnalysisResult] = None
    ml_result: Optional[AnalysisResult] = None
    final_risk_level: RiskLevel
    risk_score: float  # 0.0 to 1.0
    summary: str
    recommendations: List[str]
    total_execution_time: float

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    services: Dict[str, str]
