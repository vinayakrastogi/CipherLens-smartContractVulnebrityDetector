import asyncio
import json
import tempfile
import os
from typing import List, Optional
from app.models.schemas import AnalysisResult, Vulnerability, VulnerabilityType

class MythrilService:
    """Service for running Mythril symbolic execution analysis on Solidity code"""
    
    def __init__(self):
        self.tool_name = "Mythril"
        self.mock_mode = True  # Set to True for now due to installation issues
    
    async def analyze_contract(self, code: str, contract_name: str = "Contract") -> AnalysisResult:
        """
        Run Mythril analysis on the provided Solidity code
        """
        start_time = asyncio.get_event_loop().time()
        
        if self.mock_mode:
            # Return mock results for now
            await asyncio.sleep(1)  # Simulate analysis time
            
            # Generate some mock vulnerabilities based on code patterns
            vulnerabilities = self._generate_mock_vulnerabilities(code)
            
            return AnalysisResult(
                tool=self.tool_name,
                vulnerabilities=vulnerabilities,
                summary=f"Mock analysis found {len(vulnerabilities)} potential issues",
                execution_time=asyncio.get_event_loop().time() - start_time,
                success=True
            )
        
        try:
            # Create temporary file for the contract
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sol', delete=False) as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name
            
            # Run Mythril analysis
            process = await asyncio.create_subprocess_exec(
                'myth',
                'analyze',
                temp_file_path,
                '--execution-timeout', '60',
                '--max-depth', '10',
                '--output', 'json',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
            if process.returncode != 0:
                return AnalysisResult(
                    tool=self.tool_name,
                    vulnerabilities=[],
                    summary="Mythril analysis failed",
                    execution_time=asyncio.get_event_loop().time() - start_time,
                    success=False,
                    error_message=stderr.decode() if stderr else "Unknown error"
                )
            
            # Parse Mythril JSON output
            vulnerabilities = self._parse_mythril_output(stdout.decode())
            
            return AnalysisResult(
                tool=self.tool_name,
                vulnerabilities=vulnerabilities,
                summary=f"Found {len(vulnerabilities)} potential issues",
                execution_time=asyncio.get_event_loop().time() - start_time,
                success=True
            )
            
        except Exception as e:
            return AnalysisResult(
                tool=self.tool_name,
                vulnerabilities=[],
                summary="Mythril analysis failed due to exception",
                execution_time=asyncio.get_event_loop().time() - start_time,
                success=False,
                error_message=str(e)
            )
    
    def _parse_mythril_output(self, output: str) -> List[Vulnerability]:
        """Parse Mythril JSON output and convert to our vulnerability format"""
        vulnerabilities = []
        
        try:
            data = json.loads(output)
            
            for issue in data.get('issues', []):
                vuln_type = self._map_mythril_swc(issue.get('swc-id', ''))
                
                vulnerability = Vulnerability(
                    type=vuln_type,
                    severity=self._map_mythril_severity(issue.get('severity', 'Medium')),
                    description=issue.get('description', 'No description available'),
                    line_number=issue.get('lineno'),
                    confidence=float(issue.get('confidence', 0.8))
                )
                vulnerabilities.append(vulnerability)
        
        except (json.JSONDecodeError, KeyError) as e:
            # If parsing fails, return empty list
            pass
        
        return vulnerabilities
    
    def _map_mythril_swc(self, swc_id: str) -> VulnerabilityType:
        """Map Mythril SWC IDs to our vulnerability types"""
        swc_mapping = {
            'SWC-107': VulnerabilityType.REENTRANCY,
            'SWC-101': VulnerabilityType.INTEGER_OVERFLOW,
            'SWC-104': VulnerabilityType.UNCHECKED_CALL,
            'SWC-105': VulnerabilityType.ACCESS_CONTROL,
            'SWC-106': VulnerabilityType.ACCESS_CONTROL,
            'SWC-114': VulnerabilityType.ACCESS_CONTROL,
            'SWC-115': VulnerabilityType.ACCESS_CONTROL,
        }
        
        return swc_mapping.get(swc_id, VulnerabilityType.UNKNOWN)
    
    def _map_mythril_severity(self, severity: str) -> str:
        """Map Mythril severity levels to our severity levels"""
        severity_mapping = {
            'High': 'high',
            'Medium': 'medium',
            'Low': 'low'
        }
        
        return severity_mapping.get(severity, 'medium')
    
    def _generate_mock_vulnerabilities(self, code: str) -> List[Vulnerability]:
        """Generate mock vulnerabilities based on code patterns"""
        vulnerabilities = []
        code_lower = code.lower()
        
        # Check for common vulnerability patterns
        if 'call.value' in code_lower or 'call{value:' in code_lower:
            vulnerabilities.append(Vulnerability(
                type=VulnerabilityType.REENTRANCY,
                severity="high",
                description="Potential reentrancy vulnerability detected in external call",
                line_number=None,
                confidence=0.8
            ))
        
        if 'msg.sender.call' in code_lower:
            vulnerabilities.append(Vulnerability(
                type=VulnerabilityType.UNCHECKED_CALL,
                severity="medium",
                description="Unchecked external call detected",
                line_number=None,
                confidence=0.7
            ))
        
        if 'tx.origin' in code_lower:
            vulnerabilities.append(Vulnerability(
                type=VulnerabilityType.ACCESS_CONTROL,
                severity="medium",
                description="Use of tx.origin for authorization is vulnerable",
                line_number=None,
                confidence=0.9
            ))
        
        if 'selfdestruct' in code_lower:
            vulnerabilities.append(Vulnerability(
                type=VulnerabilityType.ACCESS_CONTROL,
                severity="high",
                description="Self-destruct function detected",
                line_number=None,
                confidence=0.6
            ))
        
        # If no specific patterns found, return a generic warning
        if not vulnerabilities:
            vulnerabilities.append(Vulnerability(
                type=VulnerabilityType.UNKNOWN,
                severity="low",
                description="No obvious vulnerabilities detected in mock analysis",
                line_number=None,
                confidence=0.5
            ))
        
        return vulnerabilities
