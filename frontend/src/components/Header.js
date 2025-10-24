import React from 'react';
import { Shield, Zap } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              <Shield className="h-8 w-8 text-blue-600" />
              <Zap className="h-6 w-6 text-yellow-500" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Smart Contract Analyzer
              </h1>
              <p className="text-sm text-gray-600">
                Unified vulnerability detection with Slither, Mythril & AI
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="text-sm text-gray-500">
              <span className="inline-block w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              API Connected
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
