import React, { useState, useEffect } from 'react';
import { Upload, Play, Music, Video, AlertCircle, CheckCircle, XCircle } from 'lucide-react';
import { CustomAlert } from './CustomAlert';
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

  // Audio Processing Logic
  const analyzeAudio = async (audioFile) => {
    try {
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const reader = new FileReader();

      reader.onload = async (e) => {
        try {
          // Decode audio
          const audioData = await audioContext.decodeAudioData(e.target.result);
          
          // Update audio analysis stage
          updateProcessingStage('audioAnalysis', 'processing', 30);
          
          // Create analyzer node
          const analyser = audioContext.createAnalyser();
          analyser.fftSize = 2048;
          
          // Get frequency data
          const bufferLength = analyser.frequencyBinCount;
          const dataArray = new Uint8Array(bufferLength);
          analyser.getByteFrequencyData(dataArray);
          
          updateProcessingStage('audioAnalysis', 'processing', 60);
          
          // Simple beat detection
          const source = audioContext.createBufferSource();
          source.buffer = audioData;
          source.connect(analyser);
          
          updateProcessingStage('beatDetection', 'processing', 50);
          
          // Simulate beat detection processing
          setTimeout(() => {
            const features = {
              duration: audioData.duration,
              numberOfChannels: audioData.numberOfChannels,
              sampleRate: audioData.sampleRate,
              beats: analyzeBeatPatterns(dataArray)
            };
            
            setAudioFeatures(features);
            updateProcessingStage('beatDetection', 'complete', 100);
            updateProcessingStage('audioAnalysis', 'complete', 100);
            
            // Start visual generation
            generateVisuals(features);
          }, 2000);
          
        } catch (decodeError) {
          throw new Error('Failed to decode audio file');
        }
      };
      
      reader.readAsArrayBuffer(audioFile);
    } catch (error) {
      setError('Failed to process audio file: ' + error.message);
      setIsProcessing(false);
    }
  };

  const analyzeBeatPatterns = (frequencyData) => {
    // Simplified beat detection algorithm
    const beats = [];
    let threshold = 100;
    
    for (let i = 0; i < frequencyData.length; i++) {
      if (frequencyData[i] > threshold) {
        beats.push({
          index: i,
          intensity: frequencyData[i]
        });
      }
    }
    
    return beats;
  };

  const generateVisuals = (features) => {
    updateProcessingStage('visualGeneration', 'processing', 30);
    
    // Simulate visual generation process
    const steps = [60, 90, 100];
    steps.forEach((progress, index) => {
      setTimeout(() => {
        updateProcessingStage('visualGeneration', 'processing', progress);
        if (progress === 100) {
          updateProcessingStage('visualGeneration', 'complete', 100);
          setIsProcessing(false);
        }
      }, 1000 * (index + 1));
    });
  };

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
    
    if (file.size > 50 * 1024 * 1024) { // 50MB limit
      setError('File size should be less than 50MB');
      return;
    }
    
    setSelectedFile(file);
  };

  const handleProcess = async () => {
    if (selectedFile) {
      setIsProcessing(true);
      setIsProcessingPage(true);
  
      // Prepare FormData to send the file in the request body
      const formData = new FormData();
      formData.append("file", selectedFile);
  
      try {
        // Make the POST request directly to the backend URL
        const response = await axios.post(
          "http://127.0.0.1:5000/upload",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          }
        );
  
        // Handle the response data
        if (response.data) {
          setAudioFeatures(response.data);
          updateProcessingStage("audioAnalysis", "complete", 100);
          updateProcessingStage("beatDetection", "complete", 100);
          updateProcessingStage("visualGeneration", "complete", 100);
          setIsProcessing(false);
        }
      } catch (error) {
        setError("Failed to process audio file: " + error.message);
        setIsProcessing(false);
      }
    }
  };
  
  

  const ProcessingStage = ({ title, status, progress }) => (
    <div className="mb-4">
      <div className="flex justify-between items-center mb-2">
        <div className="flex items-center">
          {status === 'complete' && <CheckCircle className="w-5 h-5 text-green-400 mr-2" />}
          {status === 'processing' && <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-400 mr-2" />}
          {status === 'pending' && <div className="w-5 h-5 border-2 border-gray-300 rounded-full mr-2" />}
          <span className="text-white">{title}</span>
        </div>
        <span className="text-blue-400">{progress}%</span>
      </div>
      <div className="w-full bg-gray-700 rounded-full h-2">
        <div 
          className="bg-blue-600 h-2 rounded-full transition-all duration-500 ease-in-out" 
          style={{ width: `${progress}%` }}
        ></div>
      </div>
    </div>
  );

  const LandingPage = () => (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-black flex flex-col items-center justify-center p-8 transition-opacity duration-500">
      <div className="backdrop-blur-lg bg-white/10 rounded-xl p-8 max-w-2xl w-full">
        <h1 className="text-4xl font-bold text-white mb-6 text-center">
          ABBz Audio Visual Experience
        </h1>
        
        {error && (
            <CustomAlert variant="destructive" className="mb-6">
                <AlertCircle className="h-4 w-4" />
                <div>
                <div className="font-semibold">Error</div>
                <div className="text-sm">{error}</div>
                </div>
            </CustomAlert>
        )}

        <div className="space-y-6">
          <div className="bg-white/5 p-6 rounded-lg hover:bg-white/10 transition-colors">
            <div className="flex items-center mb-4">
              <Music className="w-6 h-6 text-blue-400 mr-3" />
              <h2 className="text-xl text-white">Audio Analysis</h2>
            </div>
            <p className="text-gray-300">
              Advanced AI algorithms detect percussion and harmonic elements in your audio
            </p>
          </div>

          <div className="bg-white/5 p-6 rounded-lg hover:bg-white/10 transition-colors">
            <div className="flex items-center mb-4">
              <Video className="w-6 h-6 text-purple-400 mr-3" />
              <h2 className="text-xl text-white">Visual Engine</h2>
            </div>
            <p className="text-gray-300">
              Transform your audio into stunning visuals using our AI-powered rendering engine
            </p>
          </div>

          <div className="mt-8 space-y-4">
            <div className="flex items-center justify-center w-full">
              <label className="w-full flex flex-col items-center px-4 py-6 bg-white/5 rounded-lg cursor-pointer hover:bg-white/10 transition-colors">
                <Upload className="w-8 h-8 text-blue-400" />
                <span className="mt-2 text-base text-white">
                  {selectedFile ? selectedFile.name : 'Select audio file'}
                </span>
                <span className="mt-1 text-sm text-gray-400">
                  Supported formats: MP3, WAV, OGG (max 50MB)
                </span>
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
                className="w-full py-3 px-6 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors flex items-center justify-center space-x-2 disabled:opacity-50"
              >
                {isProcessing ? (
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
                ) : (
                  <>
                    <Play className="w-5 h-5" />
                    <span>Process Audio</span>
                  </>
                )}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );

  const ProcessingPage = () => (
    <div className="min-h-screen bg-black flex flex-col items-center justify-center p-8 animate-fadeIn">
      <div className="w-full max-w-4xl aspect-video bg-gray-900 rounded-lg flex items-center justify-center p-8">
        {audioFeatures ? (
          <div className="text-white space-y-4">
            <h2 className="text-2xl font-bold mb-4">Audio Analysis Results</h2>
            <p>Duration: {audioFeatures.duration.toFixed(2)}s</p>
            <p>Channels: {audioFeatures.numberOfChannels}</p>
            <p>Sample Rate: {audioFeatures.sampleRate}Hz</p>
            <p>Detected Beats: {audioFeatures.beats.length}</p>
          </div>
        ) : (
          <div className="text-white text-xl">Processing Audio...</div>
        )}
      </div>
      
      <div className="mt-8 w-full max-w-4xl bg-gray-900 rounded-lg p-6">
        <h3 className="text-white text-lg mb-4">Processing Status</h3>
        <ProcessingStage 
          title="Audio Analysis" 
          {...processingStages.audioAnalysis} 
        />
        <ProcessingStage 
          title="Beat Detection" 
          {...processingStages.beatDetection} 
        />
        <ProcessingStage 
          title="Visual Generation" 
          {...processingStages.visualGeneration} 
        />
      </div>
 
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
        className="mt-6 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors flex items-center gap-2"
      >
        Go Back to Home
      </button>
    </div>
  );

  return isProcessingPage ? <ProcessingPage /> : <LandingPage />;
};

export default AudioVisualApp;