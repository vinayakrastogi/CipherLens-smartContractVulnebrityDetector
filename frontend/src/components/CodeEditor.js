import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';

const CodeEditor = ({ code, setCode }) => {
  return (
    <div className="bg-white/5 border border-white/10 rounded-lg shadow-md">
      <div className="px-6 py-4 border-b border-white/10">
        <h3 className="text-lg font-medium text-white">Solidity Code</h3>
        <p className="text-sm text-fuchsia-200/80">Paste your smart contract code below</p>
      </div>
      
      <div className="relative">
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="// Paste your Solidity contract code here...
pragma solidity ^0.8.0;

contract Example {
    function hello() public pure returns (string memory) {
        return 'Hello, World!';
    }
}"
          className="w-full h-96 p-4 font-mono text-sm border-0 resize-none focus:outline-none focus:ring-0 bg-black/30 text-white placeholder-gray-400"
          style={{ 
            fontFamily: 'Monaco, Menlo, "Ubuntu Mono", monospace',
            lineHeight: '1.5'
          }}
        />
        
        {code && (
          <div className="absolute top-4 right-4 bg-white/10 px-2 py-1 rounded text-xs text-fuchsia-200">
            {code.split('\n').length} lines
          </div>
        )}
      </div>
      
      {code && (
        <div className="border-t border-white/10 p-4 bg-black/20">
          <div className="text-sm text-fuchsia-200/80 mb-2">Preview:</div>
          <div className="max-h-32 overflow-y-auto">
            <SyntaxHighlighter
              language="solidity"
              style={tomorrow}
              customStyle={{
                margin: 0,
                padding: '0.5rem',
                fontSize: '0.875rem',
                background: 'transparent'
              }}
            >
              {code.slice(0, 500) + (code.length > 500 ? '...' : '')}
            </SyntaxHighlighter>
          </div>
        </div>
      )}
    </div>
  );
};

export default CodeEditor;
