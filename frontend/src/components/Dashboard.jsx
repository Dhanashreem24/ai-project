import React, { useState, useEffect } from 'react';
import CameraFeed from './CameraFeed';
import Analytics from './Analytics';
import { AlertTriangle, CheckCircle, Shield, Activity } from 'lucide-react';

const Dashboard = () => {
  const [status, setStatus] = useState(null);
  const [history, setHistory] = useState([]);
  
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/status');
        const data = await res.json();
        setStatus(data);
        
        setHistory(prev => {
          const newHistory = [...prev, { time: new Date().toLocaleTimeString(), alert: data.alert ? 1 : 0, safe: data.alert ? 0 : 1 }];
          if (newHistory.length > 20) newHistory.shift();
          return newHistory;
        });
      } catch (e) {
        console.error("Backend not running or unreachable");
      }
    };
    
    const interval = setInterval(fetchStatus, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: '2rem', maxWidth: '1400px', margin: '0 auto' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <Shield color="var(--accent)" size={32} />
          <div>
            <h1 style={{ fontSize: '1.75rem', fontWeight: 600 }}>DriveSafe AI</h1>
            <p style={{ color: 'var(--text-muted)' }}>Real-time Driver Behavior Analysis</p>
          </div>
        </div>
        
        <div className="glass-panel" style={{ padding: '0.5rem 1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Activity size={18} color="var(--accent)" />
          <span style={{ fontWeight: 500 }}>System Active</span>
        </div>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 350px', gap: '2rem' }}>
        {/* Main Feed View */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          <div className="glass-panel" style={{ padding: '24px', position: 'relative', overflow: 'hidden' }}>
            <h3 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span className="pulse" style={{ width: 10, height: 10, borderRadius: '50%', backgroundColor: 'var(--danger)', display: 'inline-block' }}></span>
              Live Cabin View
            </h3>
            <CameraFeed alert={status?.alert} />
          </div>
          
          <div className="glass-panel" style={{ padding: '24px' }}>
            <Analytics data={history} />
          </div>
        </div>

        {/* Sidebar Status */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className={`glass-panel stats-card`} style={{ 
            borderLeft: `4px solid ${status?.alert ? 'var(--danger)' : 'var(--safe)'}`,
            position: 'relative'
          }}>
            <h3 style={{ color: 'var(--text-muted)', fontSize: '1rem' }}>Current Status</h3>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginTop: '0.5rem' }}>
              {status?.alert ? <AlertTriangle color="var(--danger)" size={48} className="pulse" /> : <CheckCircle color="var(--safe)" size={48} />}
              <div>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: status?.alert ? 'var(--danger)' : 'var(--safe)' }}>
                  {status ? (status.alert ? "Distracted" : "Focused") : "Connecting..."}
                </div>
                {status && <div style={{ color: 'var(--text-main)', marginTop: '0.25rem', opacity: 0.8 }}>
                  Confidence: <span style={{ color: 'var(--accent)' }}>{(status.confidence * 100).toFixed(0)}%</span>
                </div>}
              </div>
            </div>
          </div>

          <div className="glass-panel stats-card">
            <h3 style={{ color: 'var(--text-muted)', fontSize: '1rem' }}>Detected Behavior</h3>
            <div className="stat-value" style={{ fontSize: '1.5rem', marginTop: '0.5rem' }}>
              {status ? status.behavior : "Waiting..."}
            </div>
            {status?.message && (
              <div style={{ 
                marginTop: '1rem', 
                padding: '0.75rem', 
                backgroundColor: status.alert ? 'rgba(239, 68, 68, 0.2)' : 'rgba(16, 185, 129, 0.2)', 
                borderRadius: '8px',
                color: status.alert ? '#fca5a5' : '#6ee7b7',
                fontWeight: 'bold',
                textAlign: 'center'
              }}>
                {status.message}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
