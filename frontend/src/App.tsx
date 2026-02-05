import { useState } from 'react';
import axios from 'axios';
import './App.css';

interface MetricScores {
  [key: string]: number;
}

interface SwotAnalysis {
  strengths: string[];
  weaknesses: string[];
  opportunities: string[];
  threats: string[];
}

interface EvaluationResult {
  final_score: number;
  metric_scores: MetricScores;
  swot_analysis: SwotAnalysis;
}

interface JobStatus {
  job_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  result?: EvaluationResult;
  error?: string;
}

// Update this to your backend URL
const API_BASE_URL = 'https://startup-eval-2.onrender.com';

function App() {
  const [idea, setIdea] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<EvaluationResult | null>(null);
  const [error, setError] = useState('');
  const [progress, setProgress] = useState('');

  const pollJobStatus = async (jobId: string): Promise<EvaluationResult> => {
    return new Promise((resolve, reject) => {
      const pollInterval = setInterval(async () => {
        try {
          const response = await axios.get<JobStatus>(
            `${API_BASE_URL}/evaluate/status/${jobId}`
          );

          const { status, result, error: jobError } = response.data;

          // Update progress message
          if (status === 'pending') {
            setProgress('Queued... waiting for processing');
          } else if (status === 'processing') {
            setProgress('Analyzing your idea with 6 AI agents... This may take 30-60 seconds');
          }

          // Job completed successfully
          if (status === 'completed' && result) {
            clearInterval(pollInterval);
            setProgress('');
            resolve(result);
          }

          // Job failed
          if (status === 'failed') {
            clearInterval(pollInterval);
            setProgress('');
            reject(new Error(jobError || 'Evaluation failed'));
          }
        } catch (err) {
          clearInterval(pollInterval);
          setProgress('');
          reject(err);
        }
      }, 2000); // Poll every 2 seconds

      // Timeout after 5 minutes
      setTimeout(() => {
        clearInterval(pollInterval);
        setProgress('');
        reject(new Error('Evaluation timed out. Please try again.'));
      }, 300000);
    });
  };

  const handleSubmit = async () => {
    if (!idea.trim()) return;

    setLoading(true);
    setError('');
    setResult(null);
    setProgress('Submitting your idea...');

    try {
      // Submit the evaluation job
      const submitResponse = await axios.post(`${API_BASE_URL}/evaluate/async`, {
        raw_idea: idea
      });

      const { job_id } = submitResponse.data;
      setProgress('Job submitted! Waiting in queue...');

      // Poll for results
      const evaluationResult = await pollJobStatus(job_id);
      setResult(evaluationResult);

      // Clean up the job after successful retrieval
      try {
        await axios.delete(`${API_BASE_URL}/jobs/${job_id}`);
      } catch {
        // Ignore cleanup errors
      }
    } catch (err: any) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
        err.message ||
        'Failed to evaluate idea. Please make sure the backend is running.'
      );
    } finally {
      setLoading(false);
      setProgress('');
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-8 font-sans">
      <div className="max-w-4xl mx-auto space-y-8">
        <header className="text-center space-y-2">
          <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
            Startup Idea Evaluator
          </h1>
          <p className="text-gray-400">
            Analyze your startup pitch using AI agents
          </p>
        </header>

        <section className="bg-gray-800 p-6 rounded-2xl shadow-xl border border-gray-700">
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Describe your startup idea
          </label>
          <textarea
            className="w-full h-32 bg-gray-900 text-white rounded-lg p-4 focus:ring-2 focus:ring-blue-500 focus:outline-none resize-none border border-gray-700 transition"
            placeholder="e.g. A marketplace for renting high-end specialized camera equipment peer-to-peer..."
            value={idea}
            onChange={(e) => setIdea(e.target.value)}
          />
          <button
            onClick={handleSubmit}
            disabled={loading || !idea.trim()}
            className={`mt-4 w-full py-3 rounded-lg font-bold text-lg transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98] ${loading || !idea.trim()
              ? 'bg-gray-600 cursor-not-allowed opacity-50'
              : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white shadow-lg'
              }`}
          >
            {loading ? 'Analyzing...' : 'Evaluate Idea'}
          </button>

          {/* Progress indicator */}
          {progress && (
            <div className="mt-4 p-4 bg-blue-900/30 border border-blue-700 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className="animate-spin h-5 w-5 border-2 border-blue-400 border-t-transparent rounded-full"></div>
                <span className="text-blue-200">{progress}</span>
              </div>
            </div>
          )}

          {error && (
            <div className="mt-4 p-3 bg-red-900/50 border border-red-700 text-red-200 rounded-lg text-center">
              {error}
            </div>
          )}
        </section>

        {result && (
          <div className="space-y-6 animate-fade-in">
            {/* Final Score */}
            <div className="bg-gray-800 p-6 rounded-2xl shadow-xl border border-gray-700 flex flex-col items-center">
              <h2 className="text-xl font-semibold text-gray-400">Final Score</h2>
              <div className="text-6xl font-black mt-2 text-transparent bg-clip-text bg-gradient-to-br from-green-400 to-emerald-600">
                {result.final_score}
                <span className="text-2xl text-gray-500">/100</span>
              </div>
            </div>

            {/* Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(result.metric_scores).map(([metric, score]) => (
                <div
                  key={metric}
                  className="bg-gray-800 p-5 rounded-xl border border-gray-700 flex justify-between items-center hover:bg-gray-750 transition"
                >
                  <span className="capitalize text-gray-300 font-medium">
                    {metric.replace(/_/g, ' ')}
                  </span>
                  <div className="flex items-center space-x-3">
                    <div className="w-24 h-2 bg-gray-700 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-blue-500 rounded-full"
                        style={{ width: `${(score / 10) * 100}%` }}
                      />
                    </div>
                    <span className="font-bold text-blue-400">{score}/10</span>
                  </div>
                </div>
              ))}
            </div>

            {/* SWOT Analysis */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-gray-800 p-6 rounded-xl border border-green-900/30 shadow-lg">
                <h3 className="text-lg font-bold text-green-400 mb-3 flex items-center">
                  <span className="mr-2">💪</span> Strengths
                </h3>
                <ul className="space-y-2">
                  {result.swot_analysis.strengths.map((item, i) => (
                    <li key={i} className="text-gray-300 text-sm flex items-start">
                      <span className="text-green-500 mr-2">•</span> {item}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-gray-800 p-6 rounded-xl border border-red-900/30 shadow-lg">
                <h3 className="text-lg font-bold text-red-400 mb-3 flex items-center">
                  <span className="mr-2">🔻</span> Weaknesses
                </h3>
                <ul className="space-y-2">
                  {result.swot_analysis.weaknesses.map((item, i) => (
                    <li key={i} className="text-gray-300 text-sm flex items-start">
                      <span className="text-red-500 mr-2">•</span> {item}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-gray-800 p-6 rounded-xl border border-blue-900/30 shadow-lg">
                <h3 className="text-lg font-bold text-blue-400 mb-3 flex items-center">
                  <span className="mr-2">🚀</span> Opportunities
                </h3>
                <ul className="space-y-2">
                  {result.swot_analysis.opportunities.map((item, i) => (
                    <li key={i} className="text-gray-300 text-sm flex items-start">
                      <span className="text-blue-500 mr-2">•</span> {item}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-gray-800 p-6 rounded-xl border border-yellow-900/30 shadow-lg">
                <h3 className="text-lg font-bold text-yellow-400 mb-3 flex items-center">
                  <span className="mr-2">⚠️</span> Threats
                </h3>
                <ul className="space-y-2">
                  {result.swot_analysis.threats.map((item, i) => (
                    <li key={i} className="text-gray-300 text-sm flex items-start">
                      <span className="text-yellow-500 mr-2">•</span> {item}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;