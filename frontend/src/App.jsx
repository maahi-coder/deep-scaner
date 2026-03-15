import { useState, useRef } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { UploadCloud, FileVideo, FileImage, ShieldAlert, Cpu, CheckCircle2, Loader2, X } from 'lucide-react';
import clsx from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs) { return twMerge(clsx(inputs)); }

export default function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const fileInputRef = useRef(null);

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) processFile(droppedFile);
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) processFile(selectedFile);
  };

  const processFile = (selectedFile) => {
    setFile(selectedFile);
    setResult(null);
    if (selectedFile.type.startsWith('image/') || selectedFile.type.startsWith('video/')) {
      const url = URL.createObjectURL(selectedFile);
      setPreview(url);
    } else {
      setPreview(null);
    }
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    const isVideo = file.type.startsWith('video/');
    const endpoint = isVideo ? 'http://localhost:8000/analyze/video' : 'http://localhost:8000/analyze/image';

    try {
      const response = await axios.post(endpoint, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert('Error connecting to Backend. Ensure api.py is running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background text-white selection:bg-primary/40 font-sans flex flex-col relative overflow-hidden">
      
      {/* Dynamic Background Elements */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="absolute top-[-20%] left-[-10%] w-[50vw] h-[50vw] rounded-full bg-primary/10 blur-[150px] animate-[pulse_8s_ease-in-out_infinite]" />
        <div className="absolute bottom-[-20%] right-[-10%] w-[50vw] h-[50vw] rounded-full bg-secondary/10 blur-[150px] animate-[pulse_10s_ease-in-out_infinite_reverse]" />
        <div className="absolute top-1/2 left-1/2 min-w-full min-h-full -translate-x-1/2 -translate-y-1/2 bg-[url('https://transparenttextures.com/patterns/cubes.png')] opacity-5" />
      </div>

      {/* Modern Navbar */}
      <nav className="relative z-20 w-full px-8 py-6 flex items-center justify-between border-b border-white/5 glass">
        <div className="flex items-center gap-4">
          <img src="/logo.png" alt="Logo" className="w-12 h-12 object-contain filter drop-shadow-[0_0_10px_rgba(0,240,255,0.8)]" />
          <h1 className="text-xl md:text-3xl font-syncopate font-bold tracking-widest text-white text-glow hidden sm:block">
            AI <span className="text-primary">DETECTOR</span>
          </h1>
        </div>
        <div className="font-orbitron text-sm text-primary tracking-widest border border-primary/30 px-4 py-2 rounded-full uppercase shadow-[0_0_15px_rgba(0,240,255,0.2)]">
          System Online
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1 w-full max-w-6xl mx-auto px-4 sm:px-6 z-10 flex flex-col items-center py-12 md:py-20">
        
        <motion.div 
          initial={{ opacity: 0, scale: 0.9 }} 
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          className="text-center mb-16"
        >
          <motion.h2 
            initial={{ y: 20 }} animate={{ y: 0 }}
            className="text-4xl md:text-5xl lg:text-6xl font-black font-syncopate tracking-tighter mb-4 text-gradient uppercase text-glow"
          >
            AI-BASED FAKE
            <br /> IMAGE AND VIDEO DETECTOR
          </motion.h2>
          <p className="text-gray-400 max-w-2xl mx-auto text-lg md:text-xl font-light leading-relaxed mt-6">
            Leveraging Convolutional Neural Networks (CNN) and advanced computer vision to detect facial anomalies, texture inconsistencies, and synthetic manipulations.
          </p>
        </motion.div>

        {/* Neural Upload Bay */}
        <motion.div
           initial={{ opacity: 0, y: 30 }}
           animate={{ opacity: 1, y: 0 }}
           transition={{ delay: 0.2, duration: 0.5 }}
           className="w-full max-w-4xl glass-card rounded-3xl p-3 md:p-6 shadow-[0_0_60px_rgba(0,240,255,0.1)] border-t border-primary/20"
        >
          {!file ? (
            <div
              onDragOver={handleDrop}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className="w-full h-80 border-2 border-dashed border-primary/40 rounded-2xl bg-black/40 hover:bg-primary/5 hover:border-primary transition-all flex flex-col items-center justify-center cursor-pointer group relative overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-b from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
              <Cpu className="w-16 h-16 text-primary mb-6 animate-pulse group-hover:scale-110 transition-transform drop-shadow-[0_0_15px_rgba(0,240,255,1)]" />
              <p className="text-2xl font-orbitron text-white mb-2 tracking-wide font-semibold text-glow">INITIALIZE UPLOAD</p>
              <p className="text-gray-500 font-sans tracking-wide">Drag media here or click to browse</p>
              <div className="mt-8 flex gap-3 opacity-50 font-orbitron text-xs">
                <span className="px-3 py-1 bg-white/5 rounded border border-white/10">.MP4</span>
                <span className="px-3 py-1 bg-white/5 rounded border border-white/10">.JPG</span>
                <span className="px-3 py-1 bg-white/5 rounded border border-white/10">.PNG</span>
              </div>
            </div>
          ) : (
            <div className="bg-[#040508] border border-white/10 rounded-2xl p-6 relative overflow-hidden">
              <div className="flex justify-between items-center mb-6">
                <div className="flex items-center gap-4">
                  <div className="p-4 bg-primary/10 rounded-xl border border-primary/20">
                    {file.type.startsWith('video') ? <FileVideo className="w-8 h-8 text-primary" /> : <FileImage className="w-8 h-8 text-secondary" />}
                  </div>
                  <div>
                    <h3 className="text-xl font-bold font-orbitron tracking-wider text-white truncate max-w-[200px] md:max-w-md">{file.name}</h3>
                    <p className="text-gray-500 font-mono text-sm">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                  </div>
                </div>
                <button 
                  onClick={() => { setFile(null); setPreview(null); setResult(null); }}
                  className="w-10 h-10 flex items-center justify-center bg-white/5 hover:bg-danger/20 hover:text-danger rounded-full transition-colors"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              {preview && (
                <div className="w-full h-[400px] bg-black/50 border border-white/5 rounded-xl mb-6 flex justify-center items-center overflow-hidden relative group">
                  {file.type.startsWith('video') ? (
                    <video src={preview} controls className="w-full h-full object-contain" />
                  ) : (
                    <img src={preview} alt="Target" className="w-full h-full object-contain" />
                  )}
                  {loading && (
                    <div className="absolute inset-0 bg-primary/10 backdrop-blur-sm flex items-center justify-center z-10 border-[4px] border-primary animate-pulse">
                      <div className="absolute inset-0 bg-[url('https://transparenttextures.com/patterns/cubes.png')] opacity-20 mix-blend-overlay"></div>
                      <div className="text-center font-orbitron font-bold text-2xl text-primary drop-shadow-[0_0_20px_rgba(0,240,255,1)] flex flex-col items-center">
                        <Loader2 className="w-16 h-16 animate-spin mb-4" />
                        RUNNING FORENSIC INFERENCE...
                      </div>
                    </div>
                  )}
                </div>
              )}

              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="w-full py-5 rounded-xl font-orbitron font-black text-xl tracking-widest uppercase transition-all flex items-center justify-center gap-3 relative overflow-hidden group hover:scale-[1.01] active:scale-[0.99] disabled:opacity-50 disabled:pointer-events-none bg-primary text-background shadow-[0_0_40px_rgba(0,240,255,0.4)] hover:shadow-[0_0_60px_rgba(0,240,255,0.6)]"
              >
                {loading ? 'ANALYZING NEURAL MAP...' : 'EXECUTE SCAN'}
              </button>
            </div>
          )}
          <input type="file" ref={fileInputRef} onChange={handleFileChange} className="hidden" accept="image/*,video/*" />
        </motion.div>

        {/* Results Deck */}
        <AnimatePresence>
          {result && !loading && (
            <motion.div
              initial={{ opacity: 0, y: 50, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, height: 0 }}
              className="w-full max-w-4xl mt-12"
            >
              <div className={cn(
                "rounded-3xl border p-1 lg:p-2 backdrop-blur-3xl relative shadow-2xl",
                result.is_fake ? "bg-danger/10 border-danger/50 shadow-[0_0_80px_rgba(255,0,60,0.3)]" : "bg-primary/10 border-primary/50 shadow-[0_0_80px_rgba(0,240,255,0.15)]"
              )}>
                <div className="glass-card bg-[#040508]/90 rounded-2xl p-6 md:p-10 flex flex-col md:flex-row items-center gap-8 relative overflow-hidden">
                  
                  {/* Holographic Watermark effect */}
                  <div className={cn("absolute -top-32 -right-32 w-64 h-64 blur-[100px] rounded-full opacity-30 pointer-events-none", result.is_fake ? 'bg-danger' : 'bg-primary')} />

                  <div className="shrink-0 relative z-10">
                    <div className={cn(
                      "w-32 h-32 rounded-full flex items-center justify-center border-4 shadow-2xl",
                      result.is_fake ? "bg-danger/20 border-danger shadow-danger/40" : "bg-primary/20 border-primary shadow-primary/40"
                    )}>
                      {result.is_fake ? (
                        <ShieldAlert className="w-16 h-16 text-danger animate-pulse" />
                      ) : (
                        <CheckCircle2 className="w-16 h-16 text-primary" />
                      )}
                    </div>
                  </div>

                  <div className="flex-1 w-full text-center md:text-left z-10">
                    <h3 className={cn(
                      "text-3xl md:text-4xl font-syncopate font-black mb-3 text-glow",
                      result.is_fake ? "text-danger text-glow-danger" : "text-primary break-words"
                    )}>
                      {result.message}
                    </h3>
                    
                    {result.analysis && <p className="text-gray-400 font-sans mt-2 mb-6 text-sm">{result.analysis}</p>}

                    <div className="mt-8 space-y-4 font-orbitron">
                      <div className="flex justify-between items-end">
                        <span className="text-sm tracking-widest text-gray-400 uppercase">CNN Confidence Score</span>
                        <span className="text-3xl font-bold tracking-wider">{result.confidence.toFixed(1)}%</span>
                      </div>
                      <div className="w-full h-3 rounded-full bg-white/5 border border-white/10 overflow-hidden relative">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${result.confidence}%` }}
                          transition={{ duration: 1.5, ease: "easeOut" }}
                          className={cn("h-full relative", result.is_fake ? "bg-danger shadow-[0_0_15px_rgba(255,0,60,1)]" : "bg-primary shadow-[0_0_15px_rgba(0,240,255,1)]")}
                        >
                          <div className="absolute inset-0 bg-white/20 w-full animate-[shimmer_2s_infinite]" />
                        </motion.div>
                      </div>
                    </div>

                    {result.total_frames !== undefined && (
                      <div className="mt-8 grid grid-cols-3 gap-4 font-mono text-sm bg-black/50 p-4 rounded-xl border border-white/10">
                        <div className="text-center">
                          <span className="text-gray-500 block text-xs mb-1 font-orbitron">TOTAL FRAMES</span>
                          <span className="text-xl font-bold text-white">{result.total_frames}</span>
                        </div>
                        <div className="text-center border-l border-white/10">
                          <span className="text-danger block text-xs mb-1 font-orbitron">FAKE DETECTED</span>
                          <span className="text-xl font-bold text-danger">{result.fake_frames}</span>
                        </div>
                        <div className="text-center border-l border-white/10">
                          <span className="text-primary block text-xs mb-1 font-orbitron">REAL DETECTED</span>
                          <span className="text-xl font-bold text-primary">{result.real_frames}</span>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}
