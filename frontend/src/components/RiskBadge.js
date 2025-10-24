import React from 'react';
import { AlertTriangle, CheckCircle, AlertCircle, Shield } from 'lucide-react';

const RiskBadge = ({ riskLevel }) => {
  const getRiskConfig = (level) => {
    switch (level) {
      case 'High Risk':
        return {
          icon: <AlertTriangle className="h-4 w-4" />,
          bgColor: 'bg-red-100',
          textColor: 'text-red-800',
          borderColor: 'border-red-200',
          iconColor: 'text-red-600'
        };
      case 'Moderate Risk':
        return {
          icon: <AlertCircle className="h-4 w-4" />,
          bgColor: 'bg-orange-100',
          textColor: 'text-orange-800',
          borderColor: 'border-orange-200',
          iconColor: 'text-orange-600'
        };
      case 'Low Risk':
        return {
          icon: <Shield className="h-4 w-4" />,
          bgColor: 'bg-yellow-100',
          textColor: 'text-yellow-800',
          borderColor: 'border-yellow-200',
          iconColor: 'text-yellow-600'
        };
      case 'Safe':
        return {
          icon: <CheckCircle className="h-4 w-4" />,
          bgColor: 'bg-green-100',
          textColor: 'text-green-800',
          borderColor: 'border-green-200',
          iconColor: 'text-green-600'
        };
      default:
        return {
          icon: <Shield className="h-4 w-4" />,
          bgColor: 'bg-gray-100',
          textColor: 'text-gray-800',
          borderColor: 'border-gray-200',
          iconColor: 'text-gray-600'
        };
    }
  };

  const config = getRiskConfig(riskLevel);

  return (
    <div className={`inline-flex items-center space-x-2 px-3 py-1 rounded-full border ${config.bgColor} ${config.borderColor}`}>
      <span className={config.iconColor}>
        {config.icon}
      </span>
      <span className={`text-sm font-medium ${config.textColor}`}>
        {riskLevel}
      </span>
    </div>
  );
};

export default RiskBadge;
