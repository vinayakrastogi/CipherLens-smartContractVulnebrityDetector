import React, { useState } from 'react';
import Header from './components/Header';
import CodeEditor from './components/CodeEditor';
import AnalysisResults from './components/AnalysisResults';
import { analyzeContract } from './utils/api';

function App() {
  const [showLanding, setShowLanding] = useState(true);
  const [code, setCode] = useState('');
  const [contractName, setContractName] = useState('MyContract');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!code.trim()) {
      setError('Please enter some Solidity code to analyze');
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setResults(null);

    try {
      const analysisResults = await analyzeContract({
        code,
        contract_name: contractName,
        include_slither: true,
        include_mythril: true,
        include_ml: true
      });
      setResults(analysisResults);
    } catch (err) {
      setError(err.message || 'Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.name.endsWith('.sol')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setCode(e.target.result);
        setContractName(file.name.replace('.sol', ''));
      };
      reader.readAsText(file);
    } else {
      setError('Please select a valid .sol file');
    }
  };

  if (showLanding) {
    return (
      <div className="min-h-screen text-white bg-gradient-animate">
        <Header dark />
        <main className="relative">
          <section className="container mx-auto px-4 pt-16 pb-10 lg:pt-24 lg:pb-16">
            <div className="max-w-4xl mx-auto text-center">
              <div className="inline-flex items-center justify-center space-x-3 mb-6">
                <span className="text-4xl font-extrabold tracking-tight">CipherLens</span>
                <span className="inline-block h-2 w-2 rounded-full bg-fuchsia-400 shadow-[0_0_15px_2px_rgba(217,70,239,0.6)]" />
              </div>
              <h2 className="text-2xl md:text-3xl text-fuchsia-200/90 font-medium mb-6">
                AI-Powered Smart Contract Vulnerability Detection System
              </h2>
              <button
                onClick={() => setShowLanding(false)}
                className="mt-2 inline-flex items-center px-6 py-3 rounded-lg bg-gradient-to-r from-fuchsia-500 via-purple-500 to-indigo-500 hover:from-fuchsia-400 hover:via-purple-400 hover:to-indigo-400 transition-colors shadow-lg shadow-fuchsia-500/30"
              >
                Start Analyzing
              </button>
            </div>
          </section>

          <section className="container mx-auto px-4 pb-16">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {[
                {
                  title: 'Why CipherLens',
                  desc: 'Unified static + symbolic + ML analysis for comprehensive coverage.'
                },
                {
                  title: 'How It’s Better',
                  desc: 'Parallel tool execution with a calibrated risk classifier.'
                },
                {
                  title: 'ML Model',
                  desc: 'Locally hosted transformer pipeline tuned for Solidity semantics.'
                },
                {
                  title: 'Slither & Mythril',
                  desc: 'Industry-standard analyzers for best-in-class findings.'
                }
              ].map((c, i) => (
                <div key={i} className="rounded-xl p-5 bg-white/5 backdrop-blur-sm border border-white/10 hover:border-fuchsia-400/40 transition-colors">
                  <h3 className="text-lg font-semibold text-white mb-2">{c.title}</h3>
                  <p className="text-sm text-fuchsia-100/80 leading-relaxed">{c.desc}</p>
                </div>
              ))}
            </div>
          </section>

          {/* How It Works */}
          <section className="container mx-auto px-4 pb-16">
            <h3 className="text-center text-xl font-semibold text-white mb-8">How It Works</h3>
            <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-5 gap-4">
              {[
                'User Uploads Contract',
                'Slither Scan',
                'Mythril Symbolic Execution',
                'ML Risk Classifier',
                'Final Score & Report'
              ].map((step, idx) => (
                <div key={idx} className="text-center">
                  <div className="rounded-xl p-4 bg-white/5 border border-white/10 text-white">
                    <div className="text-2xl font-bold mb-1">{idx + 1}</div>
                    <div className="text-sm text-fuchsia-100/80">{step}</div>
                  </div>
                  {idx < 4 && (
                    <div className="hidden md:block h-0.5 bg-gradient-to-r from-fuchsia-500 to-indigo-500 mt-2"></div>
                  )}
                </div>
              ))}
            </div>
          </section>

          {/* Supported Vulnerabilities */}
          <section className="container mx-auto px-4 pb-16">
            <h3 className="text-center text-xl font-semibold text-white mb-8">Supported Vulnerabilities</h3>
            <div className="max-w-5xl mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {[
                'Reentrancy',
                'Integer Overflow / Underflow',
                'Access Control Misconfigurations',
                'Missing Input Validation',
                'Front-running / MEV Risks',
                'Denial of Service',
                'Unused Return Values',
                'Unprotected Self-Destruct',
                'Insecure Delegatecall'
              ].map((v, i) => (
                <div key={i} className="rounded-xl p-4 bg-white/5 border border-white/10 text-white flex items-center space-x-3">
                  <span className="inline-block h-2 w-2 rounded-full bg-green-400 shadow-[0_0_10px_2px_rgba(74,222,128,0.5)]"></span>
                  <span className="text-sm">{v}</span>
                </div>
              ))}
            </div>
          </section>

          {/* Comparison Table */}
          <section className="container mx-auto px-4 pb-16">
            <h3 className="text-center text-xl font-semibold text-white mb-8">Comparison</h3>
            <div className="max-w-5xl mx-auto overflow-x-auto">
              <table className="w-full text-left text-sm text-white/90 bg-white/5 border border-white/10 rounded-lg overflow-hidden">
                <thead className="bg-white/10">
                  <tr>
                    <th className="px-4 py-3">Feature</th>
                    <th className="px-4 py-3">Slither</th>
                    <th className="px-4 py-3">Mythril</th>
                    <th className="px-4 py-3">CipherLens</th>
                  </tr>
                </thead>
                <tbody>
                  {[
                    ['Static Analysis', '✅', '⚠️', '✅'],
                    ['Symbolic Execution', '❌', '✅', '✅'],
                    ['ML-Based Risk Scoring', '❌', '❌', '✅'],
                    ['Unified Report', '❌', '❌', '✅'],
                    ['Web UI', '❌', '❌', '✅']
                  ].map((row, i) => (
                    <tr key={i} className="border-t border-white/10">
                      <td className="px-4 py-3 text-fuchsia-100/90">{row[0]}</td>
                      <td className="px-4 py-3">{row[1]}</td>
                      <td className="px-4 py-3">{row[2]}</td>
                      <td className="px-4 py-3">{row[3]}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          {/* Why Choose */}
          <section className="container mx-auto px-4 pb-16">
            <h3 className="text-center text-xl font-semibold text-white mb-8">Why Choose CipherLens?</h3>
            <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {[
                ['Fast', 'Parallel execution of all tools'],
                ['Accurate', 'ML + static + symbolic combo'],
                ['Local', 'Zero data leaves your system'],
                ['Developer-centric', 'Clean reports, easy fixes']
              ].map((item, i) => (
                <div key={i} className="rounded-xl p-5 bg-white/5 border border-white/10 text-white">
                  <div className="text-lg font-semibold mb-1">{item[0]}</div>
                  <div className="text-sm text-fuchsia-100/80">{item[1]}</div>
                </div>
              ))}
            </div>
          </section>

          {/* Testimonials */}
          <section className="container mx-auto px-4 pb-20">
            <h3 className="text-center text-xl font-semibold text-white mb-8">Testimonials & Use Cases</h3>
            <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="rounded-xl p-5 bg-white/5 border border-white/10 text-white">
                <p className="text-sm text-white/90">“CipherLens immediately caught a reentrancy issue in our staking contract before deployment.”</p>
                <p className="text-xs text-fuchsia-200/80 mt-3">— Web3 Startup</p>
              </div>
              <div className="rounded-xl p-5 bg-white/5 border border-white/10 text-white">
                <p className="text-sm text-white/90">“Unified analysis saved us hours of manual Mythril review.”</p>
                <p className="text-xs text-fuchsia-200/80 mt-3">— Smart Contract Auditor</p>
              </div>
            </div>
          </section>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0b0b10] text-white">
      <Header dark />
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Left Column - Code Input */}
            <div className="space-y-6">
              <div className="bg-white/5 border border-white/10 rounded-lg shadow-md p-6">
                <h2 className="text-xl font-semibold text-white mb-4">
                  Smart Contract Code
                </h2>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-fuchsia-200 mb-2">
                      Contract Name
                    </label>
                    <input
                      type="text"
                      value={contractName}
                      onChange={(e) => setContractName(e.target.value)}
                      className="w-full px-3 py-2 bg-black/30 border border-white/15 rounded-md focus:outline-none focus:ring-2 focus:ring-fuchsia-500 placeholder-gray-400"
                      placeholder="Enter contract name"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-fuchsia-200 mb-2">
                      Upload .sol File
                    </label>
                    <input
                      type="file"
                      accept=".sol"
                      onChange={handleFileUpload}
                      className="w-full px-3 py-2 bg-black/30 border border-white/15 rounded-md focus:outline-none focus:ring-2 focus:ring-fuchsia-500 text-white"
                    />
                  </div>
                </div>
              </div>

              <CodeEditor 
                code={code}
                setCode={setCode}
              />

              <div className="flex space-x-4">
                <button
                  onClick={handleAnalyze}
                  disabled={isAnalyzing || !code.trim()}
                  className={`flex-1 py-3 px-6 rounded-lg font-medium transition-colors ${
                    isAnalyzing || !code.trim()
                      ? 'bg-white/10 text-gray-400 cursor-not-allowed'
                      : 'bg-gradient-to-r from-fuchsia-600 via-purple-600 to-indigo-600 text-white hover:from-fuchsia-500 hover:via-purple-500 hover:to-indigo-500'
                  }`}
                >
                  {isAnalyzing ? 'Analyzing...' : 'Analyze Contract'}
                </button>
              </div>

              {error && (
                <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4">
                  <p className="text-red-200">{error}</p>
                </div>
              )}
            </div>

            {/* Right Column - Results */}
            <div>
              <AnalysisResults 
                results={results}
                isAnalyzing={isAnalyzing}
              />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
