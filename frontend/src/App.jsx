import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Activity, Eye, Brain, AlertTriangle, 
  MessageSquare, CheckCircle2, User, Camera, Zap
} from 'lucide-react';

const WEBSOCKET_URL = "ws://127.0.0.1:8000/ws";

export default function App() {
  const [isConnected, setIsConnected] = useState(false);
  const [data, setData] = useState({
    image: null,
    status: "Bekleniyor...",
    alert_msg: "Bağlantı kuruluyor...",
    attention_score: 100,
    fatigue_score: 0,
    metrics: { ear: 0, pitch: 0, yaw: 0 },
    coach_msg: ""
  });
  const wsRef = useRef(null);

  useEffect(() => {
    connectWebSocket();
    return () => {
      if (wsRef.current) wsRef.current.close();
    };
  }, []);

  const connectWebSocket = () => {
    wsRef.current = new WebSocket(WEBSOCKET_URL);
    
    wsRef.current.onopen = () => {
      setIsConnected(true);
      setData(prev => ({...prev, status: "Hazır", alert_msg: "Sistem aktif. Analiz başlıyor..."}));
    };

    wsRef.current.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data);
        setData(parsed);
      } catch (err) {
        console.error("Parse error:", err);
      }
    };

    wsRef.current.onclose = () => {
      setIsConnected(false);
      setData(prev => ({...prev, status: "Bağlantı Koptu", alert_msg: "Yeniden bağlanılıyor..."}));
      setTimeout(connectWebSocket, 3000);
    };
  };

  // Determine colors based on status
  let statusColor = "text-gray-400";
  let glowClass = "";
  let StatusIcon = Activity;

  if (data.status === "Dikkatli") {
    statusColor = "text-emerald-400";
    glowClass = "status-glow-green";
    StatusIcon = CheckCircle2;
  } else if (data.status === "Dikkati Dağılmış") {
    statusColor = "text-amber-400";
    glowClass = "status-glow-orange";
    StatusIcon = AlertTriangle;
  } else if (data.status === "Yorgun / Uykulu") {
    statusColor = "text-rose-500";
    glowClass = "status-glow-red";
    StatusIcon = Zap;
  }

  return (
    <div className="min-h-screen bg-[#0f111a] text-white p-4 md:p-8 font-sans overflow-hidden relative">
      {/* Background aesthetic blobs */}
      <div className="absolute top-[-10%] left-[-10%] w-[40vw] h-[40vw] bg-purple-900/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40vw] h-[40vw] bg-blue-900/20 rounded-full blur-[120px] pointer-events-none" />
      
      {/* Header */}
      <header className="flex justify-between items-center mb-8 relative z-10">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-indigo-500/10 rounded-2xl border border-indigo-500/20">
            <Brain className="w-8 h-8 text-indigo-400" />
          </div>
          <div>
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">
              CogniSense AI
            </h1>
            <p className="text-gray-400 text-sm">Gerçek Zamanlı Dikkat ve Yorgunluk Analizi</p>
          </div>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 px-4 py-2 rounded-full glass-panel text-sm font-medium">
            <div className={`w-2.5 h-2.5 rounded-full ${isConnected ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`} />
            {isConnected ? 'Sistem Aktif' : 'Bağlantı Koptu'}
          </div>
          <button className="p-2.5 rounded-xl glass-panel hover:bg-white/5 transition-colors">
            <User className="w-5 h-5 text-gray-300" />
          </button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 relative z-10">
        
        {/* Main Video Feed Area */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          <motion.div 
            className={`glass-panel rounded-3xl overflow-hidden relative aspect-video flex items-center justify-center transition-all duration-500 ${glowClass}`}
            layout
          >
            {data.image ? (
              <img 
                src={`data:image/jpeg;base64,${data.image}`} 
                alt="Webcam Feed" 
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="flex flex-col items-center text-gray-500 gap-4">
                <Camera className="w-16 h-16 animate-pulse" />
                <p>Kamera başlatılıyor...</p>
              </div>
            )}
            
            {/* Overlay Status Badge */}
            <AnimatePresence mode="wait">
              <motion.div 
                key={data.status}
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className={`absolute top-6 left-6 px-5 py-2.5 rounded-full glass-panel border flex items-center gap-3 backdrop-blur-md font-semibold text-lg`}
              >
                <StatusIcon className={`w-5 h-5 ${statusColor}`} />
                <span className={statusColor}>{data.status}</span>
              </motion.div>
            </AnimatePresence>
          </motion.div>

          {/* Alert Message Box */}
          <AnimatePresence>
            {data.alert_msg && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass-panel rounded-2xl p-6 flex items-start gap-4 border-l-4 border-indigo-500"
              >
                <div className="p-3 bg-indigo-500/10 rounded-xl">
                  <MessageSquare className="w-6 h-6 text-indigo-400" />
                </div>
                <div>
                  <h3 className="text-gray-300 text-sm font-medium mb-1">Durum Güncellemesi</h3>
                  <p className="text-white text-lg font-medium">{data.alert_msg}</p>
                  {data.coach_msg && (
                     <p className="text-indigo-300 mt-2 italic flex items-center gap-2">
                       <Zap className="w-4 h-4"/> AI Koç: {data.coach_msg}
                     </p>
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Sidebar Analytics */}
        <div className="lg:col-span-4 flex flex-col gap-6">
          
          {/* Main Scores */}
          <div className="glass-panel rounded-3xl p-6 flex flex-col gap-6">
            <h2 className="text-xl font-bold mb-2">Metrik Analizi</h2>
            
            <div className="space-y-6">
              {/* Attention Score */}
              <div>
                <div className="flex justify-between items-end mb-2">
                  <span className="text-gray-400 font-medium">Dikkat Skoru</span>
                  <span className="text-2xl font-bold text-emerald-400">{Math.round(data.attention_score)}%</span>
                </div>
                <div className="h-3 w-full bg-gray-800 rounded-full overflow-hidden">
                  <motion.div 
                    className="h-full bg-gradient-to-r from-emerald-500 to-emerald-300"
                    initial={{ width: 0 }}
                    animate={{ width: `${data.attention_score}%` }}
                    transition={{ type: "spring", stiffness: 100 }}
                  />
                </div>
              </div>

              {/* Fatigue Score */}
              <div>
                <div className="flex justify-between items-end mb-2">
                  <span className="text-gray-400 font-medium">Yorgunluk Seviyesi</span>
                  <span className="text-2xl font-bold text-rose-400">{Math.round(data.fatigue_score)}%</span>
                </div>
                <div className="h-3 w-full bg-gray-800 rounded-full overflow-hidden">
                  <motion.div 
                    className="h-full bg-gradient-to-r from-rose-500 to-rose-300"
                    initial={{ width: 0 }}
                    animate={{ width: `${data.fatigue_score}%` }}
                    transition={{ type: "spring", stiffness: 100 }}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Raw Telemetry */}
          <div className="glass-panel rounded-3xl p-6 flex-1 flex flex-col">
            <div className="flex items-center gap-2 mb-6">
              <Eye className="w-5 h-5 text-gray-400" />
              <h2 className="text-lg font-bold">Biyometrik Veriler</h2>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <MetricCard 
                label="Göz Açıklığı (EAR)" 
                value={data.metrics.ear.toFixed(3)} 
                highlight={data.metrics.ear < 0.22}
              />
              <MetricCard 
                label="Baş Açısı (Pitch)" 
                value={`${data.metrics.pitch.toFixed(1)}°`} 
                highlight={Math.abs(data.metrics.pitch) > 20}
              />
              <MetricCard 
                label="Baş Dönüşü (Yaw)" 
                value={`${data.metrics.yaw.toFixed(1)}°`} 
                highlight={Math.abs(data.metrics.yaw) > 25}
              />
              <div className="glass-panel bg-white/5 rounded-2xl p-4 flex flex-col justify-center items-center text-center">
                <span className="text-xs text-gray-400 mb-1">Analiz Motoru</span>
                <span className="text-sm font-semibold text-indigo-400">Aktif</span>
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
}

function MetricCard({ label, value, highlight }) {
  return (
    <div className={`glass-panel rounded-2xl p-4 flex flex-col gap-1 transition-colors duration-300 ${highlight ? 'bg-rose-500/20 border-rose-500/50' : 'bg-white/5'}`}>
      <span className="text-xs text-gray-400">{label}</span>
      <span className={`text-xl font-bold ${highlight ? 'text-rose-400' : 'text-white'}`}>{value}</span>
    </div>
  );
}
