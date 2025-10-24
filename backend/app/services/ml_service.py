import asyncio
import httpx
import os
import re
from typing import Optional, List
from app.models.schemas import MLPrediction, AnalysisResult, Vulnerability, VulnerabilityType

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

class MLService:
    """Service for running ML-based vulnerability detection using Hugging Face model locally"""

    def __init__(self, model_name: str = "rastogivinayak/cipher-lens"):
        self.model_name = model_name
        # Load tokenizer and model locally
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.nlp = pipeline("text-classification", model=self.model, tokenizer=self.tokenizer)
        # Threshold for binary classification (0.35 = 35% chance of being vulnerable)
        self.vulnerability_threshold = 0.35

    def improved_normalize_solidity(self, code: str) -> str:
        """
        More conservative normalization that preserves important vulnerability patterns
        """
        # Remove comments but keep structure
        code = re.sub(r'/\*.*?\*/', ' ', code, flags=re.DOTALL)
        code = re.sub(r'//.*', ' ', code)

        # Remove pragma and imports (less important for vulnerability detection)
        code = re.sub(r'pragma\s+solidity[^;]*;', ' ', code, flags=re.IGNORECASE)
        code = re.sub(r'import\s+["\'][^"\']+["\'];?', ' ', code, flags=re.IGNORECASE)

        # Only normalize very long addresses (keep shorter hex values as they might be important)
        code = re.sub(r'0x[a-fA-F0-9]{20,}', '<ADDR>', code)

        # Keep numbers that might indicate vulnerabilities (like version numbers, gas limits)
        # Only normalize very large numbers
        code = re.sub(r'\b\d{10,}\b', '<LARGE_NUM>', code)

        # Normalize very long strings but keep shorter ones
        code = re.sub(r'"[^"]{50,}"', '<LONG_STR>', code)
        code = re.sub(r"'[^']{50,}'", '<LONG_STR>', code)

        # Clean up whitespace
        code = re.sub(r'\s+', ' ', code)
        code = code.strip()

        return code
    
    async def analyze_contract(self, code: str, contract_name: str = "Contract") -> AnalysisResult:
        """
        Run ML analysis on the provided Solidity code using local Hugging Face model
        """
        import time
        start_time = time.time()

        try:
            preprocessed_code = self.improved_normalize_solidity(code)
            # Run local inference
            result = self.nlp(preprocessed_code[:512])  # Truncate to 512 tokens if needed

            # Parse the model output for binary classification
            prediction, confidence = self._parse_binary_classification_output(result)

            is_vulnerable = confidence >= self.vulnerability_threshold

            vulnerabilities = self._convert_ml_prediction_to_vulnerabilities(
                "vulnerable" if is_vulnerable else "safe",
                confidence,
                code
            )

            return AnalysisResult(
                tool="ML Model",
                vulnerabilities=vulnerabilities,
                summary=f"ML model prediction: {'vulnerable' if is_vulnerable else 'safe'} (confidence: {confidence:.2f}, threshold: {self.vulnerability_threshold})",
                execution_time=time.time() - start_time,
                success=True,
                error_message=None
            )
        except Exception as e:
            # Return enhanced mock prediction on error
            return self._generate_mock_ml_analysis_result(code, start_time, error_msg=str(e))

    def _parse_binary_classification_output(self, result: list) -> tuple[str, float]:
        """
        Parse binary classification output from Hugging Face model
        Returns (prediction, confidence) tuple
        """
        try:
            if isinstance(result, list) and len(result) > 0:
                # Format: [{"label": "LABEL_0", "score": 0.95}]
                if isinstance(result[0], dict) and "label" in result[0] and "score" in result[0]:
                    score = result[0]["score"]
                    prediction = "vulnerable" if result[0]["label"] == "LABEL_0" else "safe"
                    return prediction, score
            return "safe", 0.5
        except Exception:
            return "safe", 0.3
    
    def _convert_ml_prediction_to_vulnerabilities(self, prediction: str, confidence: float, code: str) -> List[Vulnerability]:
        """Convert ML prediction to vulnerability list"""
        vulnerabilities = []
        
        if prediction == "vulnerable":
            # Analyze code patterns to determine vulnerability type
            code_lower = code.lower()
            
            if 'call.value' in code_lower or 'msg.sender.call' in code_lower:
                vulnerabilities.append(Vulnerability(
                    type=VulnerabilityType.REENTRANCY,
                    severity="high",
                    description="Potential reentrancy vulnerability detected by ML model",
                    line_number=None,
                    confidence=confidence
                ))
            
            if 'tx.origin' in code_lower:
                vulnerabilities.append(Vulnerability(
                    type=VulnerabilityType.ACCESS_CONTROL,
                    severity="medium",
                    description="Use of tx.origin for authorization detected by ML model",
                    line_number=None,
                    confidence=confidence
                ))
            
            if 'selfdestruct' in code_lower:
                vulnerabilities.append(Vulnerability(
                    type=VulnerabilityType.UNKNOWN,
                    severity="high",
                    description="Selfdestruct function detected by ML model",
                    line_number=None,
                    confidence=confidence
                ))
            
            # If no specific patterns found, add a general vulnerability
            if not vulnerabilities:
                vulnerabilities.append(Vulnerability(
                    type=VulnerabilityType.UNKNOWN,
                    severity="medium",
                    description="ML model detected potential vulnerability",
                    line_number=None,
                    confidence=confidence
                ))
        
        return vulnerabilities
    
    def _generate_mock_ml_analysis_result(self, code: str, start_time: float, error_msg: str = None) -> AnalysisResult:
        """Generate a more realistic mock analysis result based on code patterns"""
        # Preprocess the code using the same normalization as training
        preprocessed_code = self.improved_normalize_solidity(code)
        code_lower = preprocessed_code.lower()
        
        # Simple pattern-based mock analysis on preprocessed code
        vulnerability_indicators = [
            'call.value', 'msg.sender.call', 'selfdestruct', 'tx.origin',
            'unchecked', 'assembly', 'delegatecall', 'call(', 'send('
        ]
        
        vulnerability_count = sum(1 for pattern in vulnerability_indicators if pattern in code_lower)
        
        # Generate confidence score based on vulnerability indicators
        # Make the confidence scores more realistic and above threshold for vulnerable contracts
        if vulnerability_count >= 3:
            confidence = 0.85  # High confidence for multiple indicators
        elif vulnerability_count >= 2:
            confidence = 0.75  # Good confidence for multiple indicators
        elif vulnerability_count >= 1:
            confidence = 0.65  # Moderate confidence for single indicator
        else:
            confidence = 0.25  # Low confidence for no indicators (below threshold)
        
        # Apply threshold: if confidence >= 0.35, mark as vulnerable
        is_vulnerable = confidence >= self.vulnerability_threshold
        prediction = "vulnerable" if is_vulnerable else "safe"
        
        # Convert to vulnerabilities
        vulnerabilities = self._convert_ml_prediction_to_vulnerabilities(prediction, confidence, code)
        
        summary = f"Mock ML analysis: {prediction} (confidence: {confidence:.2f}, threshold: {self.vulnerability_threshold})"
        if error_msg:
            summary += f" - {error_msg}"
        
        return AnalysisResult(
            tool="ML Model",
            vulnerabilities=vulnerabilities,
            summary=summary,
            execution_time=asyncio.get_event_loop().time() - start_time,
            success=True,
            error_message=error_msg
        )
