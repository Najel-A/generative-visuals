import React, { useState } from 'react';
import { Upload, Play, Music, Video, AlertCircle, CheckCircle, Sparkles, AudioWaveform } from 'lucide-react';
import axios from 'axios';

const AudioVisualApp = () => {
  const [isProcessingPage, setIsProcessingPage] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [processingStages, setProcessingStages] = useState({
    audioAnalysis: { status: 'pending', progress: 0 },
    beatDetection: { status: 'pending', progress: 0 },
    visualGeneration: { status: 'pending', progress: 0 }
  });
  const [audioFeatures, setAudioFeatures] = useState(null);

  const updateProcessingStage = (stage, status, progress) => {
    setProcessingStages(prev => ({
      ...prev,
      [stage]: { status, progress }
    }));
  };

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    setError(null);

    if (!file) {
      setError('Please select a file');
      return;
    }

    if (!file.type.startsWith('audio/')) {
      setError('Please select a valid audio file');
      return;
    }

    if (file.size > 50 * 1024 * 1024) {
      setError('File size should be less than 50MB');
      return;
    }

    setSelectedFile(file);
  };

  const handleProcess = async () => {
    if (!selectedFile) return;

    setIsProcessing(true);
    setIsProcessingPage(true);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });

      if (response.data) {
        setAudioFeatures(response.data);
        setProcessingStages({
          audioAnalysis: { status: 'complete', progress: 100 },
          beatDetection: { status: 'complete', progress: 100 },
          visualGeneration: { status: 'complete', progress: 100 },
        });
      }
    } catch (error) {
      setError("Failed to process audio file: " + error.message);
    } finally {
      setIsProcessing(false);
    }
  };

  const ProcessingStage = ({ title, icon: Icon, status, progress }) => (
    <div className="relative mb-6">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-blue-500/10 rounded-lg">
            <Icon className="w-5 h-5 text-blue-500" />
          </div>
          <span className="text-white font-medium">{title}</span>
        </div>
        <div className="flex items-center space-x-2">
          {status === 'complete' && <CheckCircle className="w-5 h-5 text-green-500" />}
          <span className="text-blue-400 font-medium">{progress}%</span>
        </div>
      </div>
      <div className="w-full bg-gray-700 rounded-full h-2">
        <div
          className="bg-blue-600 h-2 rounded-full transition-all duration-500 ease-in-out"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
    </div>
  );

  const Feature = ({ icon: Icon, title, description }) => (
    <div className="group relative overflow-hidden rounded-xl bg-gradient-to-br from-blue-500/10 to-purple-500/10 p-6 hover:from-blue-500/20 hover:to-purple-500/20 transition-all duration-300">
      <div className="absolute inset-0 bg-grid-white/5 mask-gradient" />
      <div className="relative z-10">
        <div className="mb-4 inline-block rounded-lg bg-blue-500/10 p-3">
          <Icon className="h-6 w-6 text-blue-400" />
        </div>
        <h3 className="mb-2 text-xl font-semibold text-white">{title}</h3>
        <p className="text-gray-400">{description}</p>
      </div>
    </div>
  );

  const LandingPage = () => (
    <div className="min-h-screen bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-900 via-gray-900 to-black">
      <div className="relative px-6 py-24 sm:px-8 sm:py-32 lg:px-12">
        <div className="relative mx-auto max-w-2xl">
          <div className="text-center">
            <h1 className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-5xl font-bold tracking-tight text-transparent sm:text-6xl">
              ABBz Audio Visual Experience
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-300">
              Transform your audio into stunning visuals powered by AI
            </p>
          </div>

          {error && (
            <div className="mt-8 rounded-lg bg-red-500/10 p-4 text-red-400">
              <div className="flex items-center space-x-2">
                <AlertCircle className="h-5 w-5" />
                <span>{error}</span>
              </div>
            </div>
          )}

          <div className="mt-12 grid gap-6 sm:grid-cols-2">
            <Feature
              icon={Music}
              title="Audio Analysis"
              description="Advanced AI algorithms detect percussion and harmonic elements in your audio"
            />
            <Feature
              icon={AudioWaveform}
              title="Visual Engine"
              description="Transform your audio into stunning visuals using our AI-powered rendering engine"
            />
          </div>

          <div className="mt-12 overflow-hidden bg-black/50 backdrop-blur-lg rounded-xl p-12 border border-gray-700">
            <label className="group relative flex cursor-pointer flex-col items-center justify-center gap-4 border-2 border-dashed border-gray-700 bg-black/50 p-12 text-center hover:border-gray-600 hover:bg-black/60">
              <div className="rounded-full bg-blue-500/10 p-4 transition-colors group-hover:bg-blue-500/20">
                <Upload className="h-8 w-8 text-blue-400" />
              </div>
              <div>
                <span className="text-lg font-medium text-white">
                  {selectedFile ? selectedFile.name : 'Drop your audio file here'}
                </span>
                <p className="mt-1 text-sm text-gray-400">
                  Supported formats: MP3, WAV, OGG (max 50MB)
                </p>
              </div>
              <input
                type="file"
                className="hidden"
                onChange={handleFileSelect}
                accept="audio/*"
              />
            </label>
          </div>

          {selectedFile && !error && (
            <button
              onClick={handleProcess}
              disabled={isProcessing}
              className="mt-8 w-full rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 px-8 py-4 font-medium text-white shadow-lg shadow-blue-500/25 hover:from-blue-500 hover:to-purple-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-black disabled:opacity-50"
            >
              <div className="flex items-center justify-center space-x-2">
                {isProcessing ? (
                  <div className="h-5 w-5 animate-spin rounded-full border-b-2 border-white" />
                ) : (
                  <>
                    <Play className="h-5 w-5" />
                    <span>Process Audio</span>
                  </>
                )}
              </div>
            </button>
          )}
        </div>
      </div>
    </div>
  );

  const ProcessingPage = () => (
    <div className="min-h-screen bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-900 via-gray-900 to-black p-8 relative flex items-center justify-center">
      
      {/* Go Back Button */}
      <button
        onClick={() => {
          setIsProcessingPage(false);
          setIsProcessing(false);
          setProcessingStages({
            audioAnalysis: { status: 'pending', progress: 0 },
            beatDetection: { status: 'pending', progress: 0 },
            visualGeneration: { status: 'pending', progress: 0 }
          });
        }}
        className="absolute top-4 left-4 rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition-colors hover:bg-blue-700"
      >
        Go Back to Home
      </button>
    
      {/* Main Processing Display */}
      <div className="w-full max-w-5xl bg-black/60 backdrop-blur-lg rounded-3xl p-16 shadow-xl flex flex-col items-center justify-center space-y-8 mb-16">
        {audioFeatures ? (
          <div className="space-y-6 text-center">
            <h2 className="text-3xl font-bold text-white">Audio Analysis Results</h2>
            <div className="grid gap-4 grid-cols-2 md:grid-cols-4">
              {[
                { label: 'Duration', value: audioFeatures.duration ? `${audioFeatures.duration.toFixed(2)}s` : 'N/A' },
                { label: 'Channels', value: audioFeatures.numberOfChannels ?? 'N/A' },
                { label: 'Sample Rate', value: audioFeatures.sampleRate ? `${audioFeatures.sampleRate}Hz` : 'N/A' },
                { label: 'Detected Beats', value: audioFeatures.beats ? audioFeatures.beats.length : 'N/A' }
              ].map((item) => (
                <div key={item.label} className="rounded-lg bg-gray-800/50 p-6">
                  <div className="text-sm text-gray-400">{item.label}</div>
                  <div className="mt-2 text-2xl font-semibold text-white">{item.value}</div>
                </div>
              ))}
            </div>
          </div>
        ) : (
            <div className="flex flex-col items-center justify-center py-10 -mt-10">
                <div className="mb-24 inline-block rounded-full bg-blue-500/10 p-28">
                    <div className="h-56 w-56 animate-spin rounded-full border-8 border-blue-400 border-t-transparent border-solid" />
                </div>
                <div className="text-3xl font-semibold text-white">Processing Audio...</div>
            </div>

          
        )}
      </div>
    
      {/* Wider Processing Status */}
      <div className="absolute bottom-5 left-1/2 transform -translate-x-1/2 w-full max-w-3xl rounded-lg bg-gray-800/60 p-3 shadow-lg backdrop-blur-lg">
        <h3 className="mb-1 text-lg font-medium text-white text-center">Processing Status</h3>
        <div className="grid grid-cols-3 gap-6">
          <ProcessingStage
            title="Audio Analysis"
            icon={Music}
            {...processingStages.audioAnalysis}
          />
          <ProcessingStage
            title="Beat Detection"
            icon={Sparkles}
            {...processingStages.beatDetection}
          />
          <ProcessingStage
            title="Visual Generation"
            icon={Video}
            {...processingStages.visualGeneration}
          />
        </div>
      </div>
    </div>
  );
  
  
  

  

  return isProcessingPage ? <ProcessingPage /> : <LandingPage />;
};

export default AudioVisualApp;
