import React, { useState } from 'react';
import { ChevronDown, ChevronRight, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';

const ToolResults = ({ tool, result, icon, color }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const getColorClasses = (color) => {
    const colorMap = {
      blue: {
        bg: 'bg-white/5',
        border: 'border-white/10',
        text: 'text-white',
        icon: 'text-fuchsia-300'
      },
      purple: {
        bg: 'bg-white/5',
        border: 'border-white/10',
        text: 'text-white',
        icon: 'text-fuchsia-300'
      },
      green: {
        bg: 'bg-white/5',
        border: 'border-white/10',
        text: 'text-white',
        icon: 'text-fuchsia-300'
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
        return 'text-red-300 bg-red-500/10 border-red-500/30';
      case 'medium':
        return 'text-orange-300 bg-orange-500/10 border-orange-500/30';
      case 'low':
        return 'text-yellow-300 bg-yellow-500/10 border-yellow-500/30';
      default:
        return 'text-fuchsia-200 bg-white/5 border-white/10';
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
              <p className="text-sm text-white/80">{result.summary}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            {getStatusIcon(result.success)}
            <span className="text-sm text-fuchsia-200/80">
              {result.execution_time.toFixed(2)}s
            </span>
            {isExpanded ? (
              <ChevronDown className="h-4 w-4 text-fuchsia-300/60" />
            ) : (
              <ChevronRight className="h-4 w-4 text-fuchsia-300/60" />
            )}
          </div>
        </div>
      </div>
      
      {isExpanded && (
        <div className="border-t border-white/10 p-4 bg-black/20">
          {result.success ? (
            <div className="space-y-3">
              {result.vulnerabilities && result.vulnerabilities.length > 0 ? (
                <div>
                  <h5 className="text-sm font-medium text-fuchsia-200/80 mb-2">
                    Vulnerabilities Found ({result.vulnerabilities.length})
                  </h5>
                  <div className="space-y-2">
                    {result.vulnerabilities.map((vuln, index) => (
                      <div key={index} className="bg-white/5 border border-white/10 rounded-lg p-3">
                        <div className="flex items-center justify-between mb-2">
                          <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border ${getSeverityColor(vuln.severity)}`}>
                            {vuln.severity.toUpperCase()}
                          </span>
                          {vuln.line_number && (
                            <span className="text-xs text-fuchsia-200/80">
                              Line {vuln.line_number}
                            </span>
                          )}
                        </div>
                        <p className="text-sm text-white mb-1">
                          <strong>{vuln.type.replace('_', ' ').toUpperCase()}</strong>
                        </p>
                        <p className="text-sm text-white/80">
                          {vuln.description}
                        </p>
                        {vuln.confidence && (
                          <div className="mt-2">
                            <div className="flex items-center space-x-2">
                              <span className="text-xs text-fuchsia-200/80">Confidence:</span>
                              <div className="flex-1 bg-white/10 rounded-full h-2">
                                <div 
                                  className="bg-fuchsia-500 h-2 rounded-full"
                                  style={{ width: `${vuln.confidence * 100}%` }}
                                ></div>
                              </div>
                              <span className="text-xs text-fuchsia-200/80">
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
                  <CheckCircle className="h-8 w-8 text-green-400 mx-auto mb-2" />
                  <p className="text-sm text-fuchsia-200/80">No vulnerabilities found</p>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-4">
              <XCircle className="h-8 w-8 text-red-400 mx-auto mb-2" />
              <p className="text-sm text-red-300 mb-1">Analysis failed</p>
              {result.error_message && (
                <p className="text-xs text-fuchsia-200/80">{result.error_message}</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ToolResults;
