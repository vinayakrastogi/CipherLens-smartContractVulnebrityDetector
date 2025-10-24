from typing import List, Optional
from app.models.schemas import (
    AnalysisResult, MLPrediction, RiskLevel, 
    ContractAnalysisResponse, Vulnerability
)

class RiskClassifier:
    """Service for combining analysis results and determining final risk level"""
    
    def __init__(self):
        self.slither_weight = 0.4
        self.mythril_weight = 0.4
        self.ml_weight = 0.2
    
    def classify_risk(
        self,
        slither_result: Optional[AnalysisResult] = None,
        mythril_result: Optional[AnalysisResult] = None,
        ml_result: Optional[AnalysisResult] = None
    ) -> tuple[RiskLevel, float, str, List[str]]:
        """
        Combine results from all tools and determine final risk classification
        Returns: (risk_level, risk_score, summary, recommendations)
        """
        
        # Calculate individual risk scores
        slither_score = self._calculate_slither_score(slither_result) if slither_result else 0.0
        mythril_score = self._calculate_mythril_score(mythril_result) if mythril_result else 0.0
        ml_score = self._calculate_ml_score(ml_result) if ml_result else 0.0
        
        # Calculate weighted risk score
        total_weight = 0.0
        weighted_score = 0.0
        
        if slither_result and slither_result.success:
            weighted_score += slither_score * self.slither_weight
            total_weight += self.slither_weight
        
        if mythril_result and mythril_result.success:
            weighted_score += mythril_score * self.mythril_weight
            total_weight += self.mythril_weight
        
        if ml_result and ml_result.success:
            weighted_score += ml_score * self.ml_weight
            total_weight += self.ml_weight
        
        # Normalize score if weights don't sum to 1.0
        if total_weight > 0:
            final_score = weighted_score / total_weight
        else:
            final_score = 0.0
        
        # Determine risk level
        risk_level = self._determine_risk_level(final_score)
        
        # Generate summary and recommendations
        summary = self._generate_summary(slither_result, mythril_result, ml_result, final_score)
        recommendations = self._generate_recommendations(slither_result, mythril_result, ml_result, risk_level)
        
        return risk_level, final_score, summary, recommendations
    
    def _calculate_slither_score(self, result: AnalysisResult) -> float:
        """Calculate risk score from Slither results"""
        if not result.success or not result.vulnerabilities:
            return 0.0
        
        score = 0.0
        for vuln in result.vulnerabilities:
            if vuln.severity == "high":
                score += 0.8
            elif vuln.severity == "medium":
                score += 0.5
            elif vuln.severity == "low":
                score += 0.2
        
        # Normalize by number of vulnerabilities
        return min(score / len(result.vulnerabilities), 1.0)
    
    def _calculate_mythril_score(self, result: AnalysisResult) -> float:
        """Calculate risk score from Mythril results"""
        if not result.success or not result.vulnerabilities:
            return 0.0
        
        score = 0.0
        for vuln in result.vulnerabilities:
            if vuln.severity == "high":
                score += 0.9
            elif vuln.severity == "medium":
                score += 0.6
            elif vuln.severity == "low":
                score += 0.3
        
        # Normalize by number of vulnerabilities
        return min(score / len(result.vulnerabilities), 1.0)
    
    def _calculate_ml_score(self, result: AnalysisResult) -> float:
        """Calculate risk score from ML results"""
        if not result.success or not result.vulnerabilities:
            return 0.0
        
        # Calculate score based on vulnerabilities found
        score = 0.0
        for vuln in result.vulnerabilities:
            if vuln.severity == "high":
                score += 0.9
            elif vuln.severity == "medium":
                score += 0.6
            elif vuln.severity == "low":
                score += 0.3
        
        # Normalize by number of vulnerabilities
        return min(score / len(result.vulnerabilities), 1.0)
    
    def _determine_risk_level(self, score: float) -> RiskLevel:
        """Determine risk level based on final score"""
        if score >= 0.8:
            return RiskLevel.HIGH
        elif score >= 0.5:
            return RiskLevel.MODERATE
        elif score >= 0.2:
            return RiskLevel.LOW
        else:
            return RiskLevel.SAFE
    
    def _generate_summary(
        self,
        slither_result: Optional[AnalysisResult],
        mythril_result: Optional[AnalysisResult],
        ml_result: Optional[AnalysisResult],
        final_score: float
    ) -> str:
        """Generate a summary of the analysis results"""
        summary_parts = []
        
        if slither_result and slither_result.success:
            vuln_count = len(slither_result.vulnerabilities)
            summary_parts.append(f"Slither found {vuln_count} potential issues")
        
        if mythril_result and mythril_result.success:
            vuln_count = len(mythril_result.vulnerabilities)
            summary_parts.append(f"Mythril identified {vuln_count} vulnerabilities")
        
        if ml_result and ml_result.success:
            vuln_count = len(ml_result.vulnerabilities)
            if vuln_count > 0:
                summary_parts.append(f"ML model found {vuln_count} potential vulnerabilities")
            else:
                summary_parts.append("ML model classified as safe")
        
        if not summary_parts:
            return "No analysis results available"
        
        return " | ".join(summary_parts)
    
    def _generate_recommendations(
        self,
        slither_result: Optional[AnalysisResult],
        mythril_result: Optional[AnalysisResult],
        ml_result: Optional[AnalysisResult],
        risk_level: RiskLevel
    ) -> List[str]:
        """Generate security recommendations based on analysis results"""
        recommendations = []
        
        # General recommendations based on risk level
        if risk_level == RiskLevel.HIGH:
            recommendations.extend([
                "Immediate security review required",
                "Consider professional security audit",
                "Do not deploy to mainnet without fixes"
            ])
        elif risk_level == RiskLevel.MODERATE:
            recommendations.extend([
                "Address identified vulnerabilities before deployment",
                "Consider additional testing",
                "Review access control mechanisms"
            ])
        elif risk_level == RiskLevel.LOW:
            recommendations.extend([
                "Review and fix minor issues",
                "Consider best practices improvements",
                "Monitor for future vulnerabilities"
            ])
        else:  # SAFE
            recommendations.extend([
                "Contract appears secure",
                "Continue following security best practices",
                "Regular security reviews recommended"
            ])
        
        # Tool-specific recommendations
        if slither_result and slither_result.vulnerabilities:
            high_severity = [v for v in slither_result.vulnerabilities if v.severity == "high"]
            if high_severity:
                recommendations.append("Address high-severity Slither findings immediately")
        
        if mythril_result and mythril_result.vulnerabilities:
            high_severity = [v for v in mythril_result.vulnerabilities if v.severity == "high"]
            if high_severity:
                recommendations.append("Fix critical Mythril-detected vulnerabilities")
        
        return recommendations
