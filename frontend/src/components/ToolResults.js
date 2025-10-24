import React, { useState } from 'react';
import { ChevronDown, ChevronRight, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';

const ToolResults = ({ tool, result, icon, color }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const getColorClasses = (color) => {
    const colorMap = {
      blue: {
        bg: 'bg-blue-50',
        border: 'border-blue-200',
        text: 'text-blue-800',
        icon: 'text-blue-600'
      },
      purple: {
        bg: 'bg-purple-50',
        border: 'border-purple-200',
        text: 'text-purple-800',
        icon: 'text-purple-600'
      },
      green: {
        bg: 'bg-green-50',
        border: 'border-green-200',
        text: 'text-green-800',
        icon: 'text-green-600'
      }
    };
    return colorMap[color] || colorMap.blue;
  };

  const colors = getColorClasses(color);

  const getStatusIcon = (success) => {
    if (success) {
      return <CheckCircle className="h-4 w-4 text-green-600" />;
    } else {
      return <XCircle className="h-4 w-4 text-red-600" />;
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high':
        return 'text-red-600 bg-red-50 border-red-200';
      case 'medium':
        return 'text-orange-600 bg-orange-50 border-orange-200';
      case 'low':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  return (
    <div className={`rounded-lg border ${colors.bg} ${colors.border}`}>
      <div 
        className="p-4 cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <span className={colors.icon}>
              {icon}
            </span>
            <div>
              <h4 className={`font-medium ${colors.text}`}>{tool}</h4>
              <p className="text-sm text-gray-600">{result.summary}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            {getStatusIcon(result.success)}
            <span className="text-sm text-gray-500">
              {result.execution_time.toFixed(2)}s
            </span>
            {isExpanded ? (
              <ChevronDown className="h-4 w-4 text-gray-400" />
            ) : (
              <ChevronRight className="h-4 w-4 text-gray-400" />
            )}
          </div>
        </div>
      </div>
      
      {isExpanded && (
        <div className="border-t border-gray-200 p-4">
          {result.success ? (
            <div className="space-y-3">
              {result.vulnerabilities && result.vulnerabilities.length > 0 ? (
                <div>
                  <h5 className="text-sm font-medium text-gray-700 mb-2">
                    Vulnerabilities Found ({result.vulnerabilities.length})
                  </h5>
                  <div className="space-y-2">
                    {result.vulnerabilities.map((vuln, index) => (
                      <div key={index} className="bg-white rounded-lg p-3 border">
                        <div className="flex items-center justify-between mb-2">
                          <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border ${getSeverityColor(vuln.severity)}`}>
                            {vuln.severity.toUpperCase()}
                          </span>
                          {vuln.line_number && (
                            <span className="text-xs text-gray-500">
                              Line {vuln.line_number}
                            </span>
                          )}
                        </div>
                        <p className="text-sm text-gray-700 mb-1">
                          <strong>{vuln.type.replace('_', ' ').toUpperCase()}</strong>
                        </p>
                        <p className="text-sm text-gray-600">
                          {vuln.description}
                        </p>
                        {vuln.confidence && (
                          <div className="mt-2">
                            <div className="flex items-center space-x-2">
                              <span className="text-xs text-gray-500">Confidence:</span>
                              <div className="flex-1 bg-gray-200 rounded-full h-2">
                                <div 
                                  className="bg-blue-600 h-2 rounded-full"
                                  style={{ width: `${vuln.confidence * 100}%` }}
                                ></div>
                              </div>
                              <span className="text-xs text-gray-500">
                                {(vuln.confidence * 100).toFixed(0)}%
                              </span>
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="text-center py-4">
                  <CheckCircle className="h-8 w-8 text-green-500 mx-auto mb-2" />
                  <p className="text-sm text-gray-600">No vulnerabilities found</p>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-4">
              <XCircle className="h-8 w-8 text-red-500 mx-auto mb-2" />
              <p className="text-sm text-red-600 mb-1">Analysis failed</p>
              {result.error_message && (
                <p className="text-xs text-gray-500">{result.error_message}</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ToolResults;
