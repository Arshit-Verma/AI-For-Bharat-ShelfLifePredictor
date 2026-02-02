'use client';

import { useState } from 'react';
import { usePrediction } from '@/hooks/usePrediction';
import { api, PredictionInput } from '@/services/api';
import { Thermometer, Droplets, Clock, AlertTriangle, CheckCircle, XCircle, Brain, MessageSquare, Volume2, Play, ChefHat } from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState('prediction');
  const [formData, setFormData] = useState<PredictionInput>({
    food_type: 'dairy',
    temperature: 4,
    humidity: 65,
    storage_type: 'refrigerator',
    days_stored: 2,
  });

  const [chatMessages, setChatMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string }>>([]);
  const [chatInput, setChatInput] = useState('');
  const [loadingChat, setLoadingChat] = useState(false);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  const { result, loading: predicting, predict, error } = usePrediction();

  const handlePredict = async () => {
    try {
      await predict(formData);
    } catch (err) {
      console.error(err);
    }
  };

  const handleVoiceExplanation = async () => {
    if (isPlayingAudio) return;
    setIsPlayingAudio(true);
    try {
      const audioBlob = await api.getVoiceExplanation(formData);
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.onended = () => {
        setIsPlayingAudio(false);
        URL.revokeObjectURL(audioUrl);
      };
      await audio.play();
    } catch (err: any) {
      setIsPlayingAudio(false);
      alert('Failed to play audio');
    }
  };

  const handleChat = async () => {
    if (!chatInput.trim()) return;
    setChatMessages([...chatMessages, { role: 'user', content: chatInput }]);
    setChatInput('');
    setLoadingChat(true);
    try {
      const response = await api.chat(chatInput, '');
      setChatMessages((prev: any) => [...prev, { role: 'assistant', content: response.response || response.error }]);
    } catch (err: any) {
      setChatMessages((prev: any) => [...prev, { role: 'assistant', content: 'Failed to get response' }]);
    } finally {
      setLoadingChat(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-blue-600 p-2 rounded-lg">
                <ChefHat className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-slate-900">ShelfLife AI</h1>
                <p className="text-sm text-slate-500">Smart Food Safety Predictor</p>
              </div>
            </div>
            <nav className="flex gap-2">
              <button onClick={() => setActiveTab('prediction')} className={`px-4 py-2 rounded-lg font-medium ${activeTab === 'prediction' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'}`}>
                <Brain className="inline w-4 h-4 mr-2" /> Predict
              </button>
              <button onClick={() => setActiveTab('voice')} className={`px-4 py-2 rounded-lg font-medium ${activeTab === 'voice' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'}`}>
                <Volume2 className="inline w-4 h-4 mr-2" /> Voice
              </button>
              <button onClick={() => setActiveTab('chat')} className={`px-4 py-2 rounded-lg font-medium ${activeTab === 'chat' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'}`}>
                <MessageSquare className="inline w-4 h-4 mr-2" /> Chat
              </button>
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {activeTab === 'prediction' && (
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-xl font-bold mb-6">Food Details</h2>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">Food Type</label>
                  <select
                    value={formData.food_type}
                    onChange={(e) => setFormData({ ...formData, food_type: e.target.value })}
                    className="w-full px-4 py-3 border-2 border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                  >
                    <option value="dairy">Dairy</option>
                    <option value="meat">Meat</option>
                    <option value="vegetables">Vegetables</option>
                    <option value="fruits">Fruits</option>
                    <option value="bakery">Bakery</option>
                    <option value="seafood">Seafood</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">Storage Type</label>
                  <select
                    value={formData.storage_type}
                    onChange={(e) => setFormData({ ...formData, storage_type: e.target.value })}
                    className="w-full px-4 py-3 border-2 border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                  >
                    <option value="refrigerator">Refrigerator</option>
                    <option value="freezer">Freezer</option>
                    <option value="pantry">Pantry</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">Temperature</label>
                  <div className="relative">
                    <Thermometer className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
                    <input
                      type="number"
                      value={formData.temperature}
                      onChange={(e) => setFormData({ ...formData, temperature: parseFloat(e.target.value) || 0 })}
                      className="w-full pl-10 pr-4 py-3 border-2 border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                      step="0.1"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">Humidity (%)</label>
                  <div className="relative">
                    <Droplets className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
                    <input
                      type="number"
                      value={formData.humidity}
                      onChange={(e) => setFormData({ ...formData, humidity: parseFloat(e.target.value) || 0 })}
                      className="w-full pl-10 pr-4 py-3 border-2 border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                      min="0"
                      max="100"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">Days Stored</label>
                  <div className="relative">
                    <Clock className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
                    <input
                      type="number"
                      value={formData.days_stored}
                      onChange={(e) => setFormData({ ...formData, days_stored: parseFloat(e.target.value) || 0 })}
                      className="w-full pl-10 pr-4 py-3 border-2 border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                      min="0"
                    />
                  </div>
                </div>

                <button
                  onClick={handlePredict}
                  disabled={predicting}
                  className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-4 rounded-xl font-semibold text-lg hover:from-blue-700 hover:to-indigo-700 transition-all disabled:opacity-50 shadow-lg"
                >
                  {predicting ? 'Analyzing...' : 'Predict Shelf Life'}
                </button>

                {error && (
                  <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg text-red-700">
                    {error}
                  </div>
                )}
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-xl font-bold mb-6">Analysis Results</h2>
              
              {result ? (
                <div className="space-y-4">
                  <div className="bg-blue-50 rounded-lg p-4 border-2 border-blue-200">
                    <p className="text-sm font-medium text-blue-900 mb-2">Predicted Remaining Days</p>
                    <p className="text-4xl font-bold text-blue-600">{result.predicted_remaining_days}</p>
                  </div>

                  <div className={`rounded-lg p-4 border-2 ${result.safety_classification === 'Safe' ? 'bg-green-50 border-green-200 text-green-800' : result.safety_classification === 'Consume Soon' ? 'bg-yellow-50 border-yellow-200 text-yellow-800' : 'bg-red-50 border-red-200 text-red-800'}`}>
                    <div className="flex items-center gap-2">
                      {result.safety_classification === 'Safe' && <CheckCircle className="w-5 h-5" />}
                      {result.safety_classification === 'Consume Soon' && <AlertTriangle className="w-5 h-5" />}
                      {result.safety_classification === 'Expired' && <XCircle className="w-5 h-5" />}
                      <span className="font-semibold">{result.safety_classification}</span>
                    </div>
                  </div>

                  {result.issues.length > 0 && (
                    <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4">
                      <p className="font-semibold text-red-900 mb-2">Issues Detected</p>
                      <ul className="list-disc list-inside space-y-1 text-red-700">
                        {result.issues.map((issue, idx) => (
                          <li key={idx}>{issue}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {result.recommendations.length > 0 && (
                    <div className="bg-green-50 border-2 border-green-200 rounded-lg p-4">
                      <p className="font-semibold text-green-900 mb-2">Recommendations</p>
                      <ul className="list-disc list-inside space-y-1 text-green-700">
                        {result.recommendations.map((rec, idx) => (
                          <li key={idx}>{rec}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  <button
                    onClick={handleVoiceExplanation}
                    disabled={isPlayingAudio}
                    className="w-full bg-purple-600 text-white py-3 rounded-lg font-medium hover:bg-purple-700 transition-all disabled:opacity-50"
                  >
                    {isPlayingAudio ? 'Playing...' : <><Play className="inline w-4 h-4 mr-2" /> Listen to Explanation</>}
                  </button>
                </div>
              ) : (
                <div className="text-center py-12 text-slate-500">
                  <p>Enter food details and click Predict to see results</p>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'voice' && (
          <div className="max-w-3xl mx-auto">
            <div className="text-center mb-8">
              <div className="bg-purple-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Volume2 className="w-8 h-8 text-white" />
              </div>
              <h2 className="text-3xl font-bold mb-2">AI Voice Assistant</h2>
              <p className="text-slate-600">Get spoken explanations of your food safety predictions</p>
            </div>

            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-slate-50 rounded-lg p-4">
                  <p className="text-sm text-slate-500">Food Type</p>
                  <p className="font-semibold text-slate-900 capitalize">{formData.food_type}</p>
                </div>
                <div className="bg-slate-50 rounded-lg p-4">
                  <p className="text-sm text-slate-500">Storage</p>
                  <p className="font-semibold text-slate-900 capitalize">{formData.storage_type}</p>
                </div>
                <div className="bg-slate-50 rounded-lg p-4">
                  <p className="text-sm text-slate-500">Temperature</p>
                  <p className="font-semibold text-slate-900">{formData.temperature}°C</p>
                </div>
                <div className="bg-slate-50 rounded-lg p-4">
                  <p className="text-sm text-slate-500">Humidity</p>
                  <p className="font-semibold text-slate-900">{formData.humidity}%</p>
                </div>
              </div>

              <button
                onClick={handleVoiceExplanation}
                disabled={isPlayingAudio}
                className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 rounded-xl font-semibold text-lg hover:from-purple-700 hover:to-pink-700 transition-all disabled:opacity-50 shadow-lg"
              >
                {isPlayingAudio ? 'Playing Audio...' : <><Play className="inline w-5 h-5 mr-2" /> Play Voice Explanation</>}
              </button>

              <div className="mt-4 bg-blue-50 border-2 border-blue-200 rounded-lg p-4 text-blue-700">
                <p className="font-semibold mb-1">Note:</p>
                <p className="text-sm">Voice explanations require a valid ElevenLabs API key configured in backend .env file.</p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'chat' && (
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-6">
              <div className="bg-blue-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <MessageSquare className="w-8 h-8 text-white" />
              </div>
              <h2 className="text-3xl font-bold mb-2">Food Safety Chat</h2>
              <p className="text-slate-600">Ask questions about food storage, safety, and best practices</p>
            </div>

            <div className="bg-white rounded-xl shadow-lg" style={{ height: '500px' }}>
              <div className="h-96 overflow-y-auto p-4 space-y-4 border-b">
                {chatMessages.length === 0 ? (
                  <div className="h-full flex flex-col items-center justify-center text-slate-500">
                    <MessageSquare className="w-12 h-12 mb-4 text-slate-300" />
                    <p>Start a conversation</p>
                  </div>
                ) : (
                  chatMessages.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                      <div className={`max-w-[80%] rounded-lg px-4 py-3 ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-800'}`}>
                        <p className="text-sm leading-relaxed">{msg.content}</p>
                      </div>
                    </div>
                  ))
                )}
                {loadingChat && (
                  <div className="flex justify-start">
                    <div className="bg-slate-100 rounded-lg px-4 py-3 text-slate-800">
                      <div className="flex gap-1">
                        <div className="w-2 h-2 bg-slate-400 rounded-full animate-pulse"></div>
                        <div className="w-2 h-2 bg-slate-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                        <div className="w-2 h-2 bg-slate-400 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              <div className="p-4">
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && !loadingChat && handleChat()}
                    placeholder="Ask about food storage, safety, or your prediction..."
                    className="flex-1 px-4 py-3 border-2 border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                    disabled={loadingChat}
                  />
                  <button
                    onClick={handleChat}
                    disabled={loadingChat || !chatInput.trim()}
                    className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-all disabled:opacity-50"
                  >
                    Send
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
