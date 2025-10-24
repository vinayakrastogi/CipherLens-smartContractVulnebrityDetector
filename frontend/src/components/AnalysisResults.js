import React from 'react';
import { 
  AlertTriangle, 
  CheckCircle, 
  Clock, 
  Shield, 
  Brain,
  Activity,
  TrendingUp,
  FileText
} from 'lucide-react';
import RiskBadge from './RiskBadge';
import ToolResults from './ToolResults';

const AnalysisResults = ({ results, isAnalyzing }) => {
  if (isAnalyzing) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-center space-x-3">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
          <span className="text-lg font-medium text-gray-700">Analyzing contract...</span>
        </div>
        <div className="mt-4 text-sm text-gray-500 text-center">
          Running Slither, Mythril, and ML analysis
        </div>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="text-center text-gray-500">
          <Shield className="h-12 w-12 mx-auto mb-4 text-gray-300" />
          <h3 className="text-lg font-medium mb-2">No Analysis Results</h3>
          <p className="text-sm">Analyze a contract to see results here</p>
        </div>
      </div>
    );
  }

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'High Risk':
        return 'text-red-600 bg-red-50 border-red-200';
      case 'Moderate Risk':
        return 'text-orange-600 bg-orange-50 border-orange-200';
      case 'Low Risk':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'Safe':
        return 'text-green-600 bg-green-50 border-green-200';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  return (
    <div className="space-y-6">
      {/* Overall Risk Assessment */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-800">Risk Assessment</h3>
          <RiskBadge riskLevel={results.final_risk_level} />
        </div>
        
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <TrendingUp className="h-4 w-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">Risk Score</span>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              {(results.risk_score * 100).toFixed(1)}%
            </div>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <Clock className="h-4 w-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">Analysis Time</span>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              {results.total_execution_time.toFixed(2)}s
            </div>
          </div>
        </div>
        
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Summary</h4>
          <p className="text-sm text-gray-600">{results.summary}</p>
        </div>
        
        {results.recommendations && results.recommendations.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-2">Recommendations</h4>
            <ul className="space-y-1">
              {results.recommendations.map((rec, index) => (
                <li key={index} className="text-sm text-gray-600 flex items-start space-x-2">
                  <span className="text-blue-500 mt-1">•</span>
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Tool Results */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-gray-800">Analysis Results</h3>
        
        {results.slither_result && (
          <ToolResults 
            tool="Slither" 
            result={results.slither_result}
            icon={<Activity className="h-5 w-5" />}
            color="blue"
          />
        )}
        
        {results.mythril_result && (
          <ToolResults 
            tool="Mythril" 
            result={results.mythril_result}
            icon={<Brain className="h-5 w-5" />}
            color="purple"
          />
        )}
        
        {results.ml_result && (
          <ToolResults 
            tool="ML Model" 
            result={results.ml_result}
            icon={<Brain className="h-5 w-5" />}
            color="green"
          />
        )}
      </div>
    </div>
  );
};

export default AnalysisResults;
