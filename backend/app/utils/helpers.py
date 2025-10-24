import uuid
from datetime import datetime
from typing import Dict, Any

def generate_analysis_id() -> str:
    """Generate a unique analysis ID"""
    return f"analysis_{uuid.uuid4().hex[:8]}"

def get_current_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.utcnow().isoformat()

def validate_solidity_code(code: str) -> tuple[bool, str]:
    """
    Basic validation of Solidity code
    Returns: (is_valid, error_message)
    """
    if not code or not code.strip():
        return False, "Code cannot be empty"
    
    if len(code) < 10:
        return False, "Code too short to be a valid contract"
    
    # Check for basic Solidity keywords
    solidity_keywords = ['contract', 'function', 'pragma', 'solidity']
    code_lower = code.lower()
    
    if not any(keyword in code_lower for keyword in solidity_keywords):
        return False, "Code doesn't appear to be Solidity"
    
    return True, ""

def format_execution_time(seconds: float) -> str:
    """Format execution time in a human-readable format"""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.1f}s"

def sanitize_contract_name(name: str) -> str:
    """Sanitize contract name for safe usage"""
    if not name:
        return "Contract"
    
    # Remove special characters and limit length
    sanitized = "".join(c for c in name if c.isalnum() or c in "_-")
    return sanitized[:50] or "Contract"
