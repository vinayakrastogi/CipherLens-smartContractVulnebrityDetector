import asyncio
import json
import tempfile
import os
from typing import List, Optional
from app.models.schemas import AnalysisResult, Vulnerability, VulnerabilityType

class SlitherService:
    """Service for running Slither static analysis on Solidity code"""
    
    def __init__(self):
        self.tool_name = "Slither"
    
    async def analyze_contract(self, code: str, contract_name: str = "Contract") -> AnalysisResult:
        """
        Run Slither analysis on the provided Solidity code
        """
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Create temporary file for the contract
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sol', delete=False) as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name
            
            # Create output file for JSON results
            output_file = temp_file_path.replace('.sol', '_output.json')
            
            # Detect Solidity version and set appropriate compiler
            solidity_version = self._detect_solidity_version(code)
            slither_args = ['slither', temp_file_path, '--json', output_file, '--disable-color']
            
            # Add compiler version if needed
            if solidity_version:
                solc_path = self._get_solc_path(solidity_version)
                if solc_path:
                    slither_args.extend(['--solc', solc_path])
            
            # Run Slither analysis
            process = await asyncio.create_subprocess_exec(
                *slither_args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
            # Parse Slither output from stderr (where Slither outputs results)
            vulnerabilities = []
            stderr_output = stderr.decode() if stderr else ""
            
            if stderr_output:
                vulnerabilities = self._parse_slither_output(stderr_output)
            
            # Also try to read from JSON file if it exists
            if os.path.exists(output_file):
                try:
                    with open(output_file, 'r') as f:
                        json_output = f.read()
                    json_vulnerabilities = self._parse_slither_output(json_output)
                    vulnerabilities.extend(json_vulnerabilities)
                    os.unlink(output_file)  # Clean up output file
                except Exception:
                    pass  # Ignore JSON parsing errors
            
            # Slither returns non-zero exit code even when it finds vulnerabilities
            # This is normal behavior, so we consider it successful if we found vulnerabilities
            success = len(vulnerabilities) > 0 or process.returncode == 0
            
            if not success:
                # Clean up output file if it exists
                if os.path.exists(output_file):
                    os.unlink(output_file)
                return AnalysisResult(
                    tool=self.tool_name,
                    vulnerabilities=[],
                    summary="Slither analysis failed",
                    execution_time=asyncio.get_event_loop().time() - start_time,
                    success=False,
                    error_message=stderr_output if stderr_output else "Unknown error"
                )
            
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
                summary="Slither analysis failed due to exception",
                execution_time=asyncio.get_event_loop().time() - start_time,
                success=False,
                error_message=str(e)
            )
    
    def _parse_slither_output(self, output: str) -> List[Vulnerability]:
        """Parse Slither output and convert to our vulnerability format"""
        vulnerabilities = []
        
        # Try to parse as JSON first
        try:
            data = json.loads(output)
            
            for detector in data.get('results', {}).get('detectors', []):
                for element in detector.get('elements', []):
                    vuln_type = self._map_slither_detector(detector.get('check', ''))
                    
                    vulnerability = Vulnerability(
                        type=vuln_type,
                        severity=self._map_slither_impact(detector.get('impact', 'Medium')),
                        description=detector.get('description', 'No description available'),
                        line_number=element.get('source_mapping', {}).get('lines', [None])[0] if element.get('source_mapping', {}).get('lines') else None,
                        confidence=0.8  # Default confidence for Slither
                    )
                    vulnerabilities.append(vulnerability)
        
        except (json.JSONDecodeError, KeyError):
            # If JSON parsing fails, parse text output
            vulnerabilities = self._parse_slither_text_output(output)
        
        return vulnerabilities
    
    def _parse_slither_text_output(self, output: str) -> List[Vulnerability]:
        """Parse Slither text output and convert to our vulnerability format"""
        vulnerabilities = []
        lines = output.split('\n')
        
        current_vuln = None
        
        for line in lines:
            line = line.strip()
            
            # Detect vulnerability types
            if 'Reentrancy in' in line:
                current_vuln = Vulnerability(
                    type=VulnerabilityType.REENTRANCY,
                    severity="high",
                    description=line,
                    line_number=None,
                    confidence=0.9
                )
                vulnerabilities.append(current_vuln)
            
            elif 'Low level call in' in line:
                current_vuln = Vulnerability(
                    type=VulnerabilityType.UNCHECKED_CALL,
                    severity="medium",
                    description=line,
                    line_number=None,
                    confidence=0.8
                )
                vulnerabilities.append(current_vuln)
            
            elif 'Version constraint' in line and 'contains known severe issues' in line:
                current_vuln = Vulnerability(
                    type=VulnerabilityType.UNKNOWN,
                    severity="medium",
                    description=line,
                    line_number=None,
                    confidence=0.7
                )
                vulnerabilities.append(current_vuln)
        
        return vulnerabilities
    
    def _map_slither_detector(self, detector_name: str) -> VulnerabilityType:
        """Map Slither detector names to our vulnerability types"""
        detector_mapping = {
            'reentrancy': VulnerabilityType.REENTRANCY,
            'unchecked-transfer': VulnerabilityType.UNCHECKED_CALL,
            'unchecked-send': VulnerabilityType.UNCHECKED_CALL,
            'tx-origin': VulnerabilityType.ACCESS_CONTROL,
            'suicidal': VulnerabilityType.ACCESS_CONTROL,
            'arbitrary-send-eth': VulnerabilityType.ACCESS_CONTROL,
            'controlled-array-length': VulnerabilityType.INTEGER_OVERFLOW,
            'controlled-delegatecall': VulnerabilityType.ACCESS_CONTROL,
        }
        
        return detector_mapping.get(detector_name.lower(), VulnerabilityType.UNKNOWN)
    
    def _map_slither_impact(self, impact: str) -> str:
        """Map Slither impact levels to our severity levels"""
        impact_mapping = {
            'High': 'high',
            'Medium': 'medium',
            'Low': 'low',
            'Informational': 'low'
        }
        
        return impact_mapping.get(impact, 'medium')
    
    def _detect_solidity_version(self, code: str) -> Optional[str]:
        """Detect Solidity version from pragma statement"""
        lines = code.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('pragma solidity'):
                # Extract version from pragma solidity ^0.4.4;
                import re
                match = re.search(r'pragma solidity\s+([^;]+)', line)
                if match:
                    version = match.group(1).strip()
                    # Extract full version (e.g., 0.4.24)
                    version_match = re.search(r'(\d+\.\d+\.\d+)', version)
                    if version_match:
                        return version_match.group(1)
                    # Fallback to major.minor if patch version not found
                    version_match = re.search(r'(\d+\.\d+)', version)
                    if version_match:
                        return version_match.group(1)
        return None
    
    def _get_solc_path(self, version: str) -> Optional[str]:
        """Get the path to the appropriate solc compiler for the given version"""
        base_path = '/home/vinayakr/Workspace/SmartContractVulnebrityDetection/version4/backend/venv/.solc-select/artifacts'
        
        # Map version to available solc versions
        version_mapping = {
            '0.4.24': 'solc-0.4.24',
            '0.4.26': 'solc-0.4.26', 
            '0.8.30': 'solc-0.8.30'
        }
        
        # Find the best matching version
        target_version = version_mapping.get(version)
        if not target_version:
            # Try to find a compatible version
            if version.startswith('0.4'):
                target_version = 'solc-0.4.26'  # Use 0.4.26 as fallback for 0.4.x
            elif version.startswith('0.8'):
                target_version = 'solc-0.8.30'  # Use 0.8.30 as fallback for 0.8.x
            else:
                return None
        
        solc_path = os.path.join(base_path, target_version, target_version)
        
        # Check if the solc binary exists
        if os.path.exists(solc_path):
            return solc_path
        
        return None
