import React from 'react';
import { Shield } from 'lucide-react';

const Header = ({ dark = false }) => {
  return (
    <header className={`${dark ? 'bg-black/20 border-white/10' : 'bg-white border-gray-200'} backdrop-blur-sm border-b`}>
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              <Shield className={`h-8 w-8 ${dark ? 'text-fuchsia-400' : 'text-blue-600'}`} />
            </div>
            <div>
              <h1 className={`text-2xl font-bold ${dark ? 'text-white' : 'text-gray-900'}`}>
                CipherLens
              </h1>
              <p className={`text-sm ${dark ? 'text-fuchsia-200/80' : 'text-gray-600'}`}>
                Unified vulnerability detection with Slither, Mythril & AI
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className={`text-sm ${dark ? 'text-fuchsia-200/80' : 'text-gray-500'}`}>
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
