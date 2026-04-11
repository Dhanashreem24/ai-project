import React, { useRef, useEffect } from 'react';

const CameraFeed = ({ alert }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    let animationFrameId;
    let lastProcessTime = 0;

    // Request webcam access for real-time vibe
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
            
            // Start processing loop once video is available
            const processFrame = async (timestamp) => {
              if (timestamp - lastProcessTime > 500 && videoRef.current && canvasRef.current) {
                const video = videoRef.current;
                const canvas = canvasRef.current;
                
                if (video.readyState === video.HAVE_ENOUGH_DATA) {
                  lastProcessTime = timestamp;
                  canvas.width = video.videoWidth;
                  canvas.height = video.videoHeight;
                  const ctx = canvas.getContext('2d');
                  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                  
                  // Keep quality low for fast inference
                  const base64Image = canvas.toDataURL('image/jpeg', 0.5);
                  
                  try {
                    await fetch('http://localhost:8000/api/predict', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ image_b64: base64Image })
                    });
                  } catch(e) {
                    // Backend unreachable
                  }
                }
              }
              animationFrameId = requestAnimationFrame(processFrame);
            };
            
            animationFrameId = requestAnimationFrame(processFrame);
          }
        })
        .catch(err => console.error("Webcam access denied: ", err));
    }

    return () => {
      if (animationFrameId) cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <div style={{ 
      width: '100%', 
      aspectRatio: '16/9', 
      backgroundColor: '#000',
      borderRadius: '12px',
      overflow: 'hidden',
      position: 'relative',
      border: `2px solid ${alert ? 'var(--danger)' : 'transparent'}`,
      transition: 'border 0.3s ease'
    }}>
      <video 
        ref={videoRef} 
        autoPlay 
        playsInline 
        muted 
        style={{ 
          width: '100%', 
          height: '100%', 
          objectFit: 'cover',
          filter: alert ? 'contrast(1.2) sepia(0.5) hue-rotate(-50deg) saturate(2)' : 'none',
          transition: 'filter 0.3s ease'
        }} 
      />
      <canvas ref={canvasRef} style={{ display: 'none' }} />
      
      {/* Overlay UI elements similar to car dashcams */}
      <div style={{
        position: 'absolute',
        top: 20,
        right: 20,
        color: 'white',
        fontFamily: 'monospace',
        backgroundColor: 'rgba(0,0,0,0.5)',
        padding: '5px 10px',
        borderRadius: '4px'
      }}>
        REC 🔴
      </div>
      
      <div style={{
        position: 'absolute',
        bottom: 20,
        left: 20,
        color: alert ? 'var(--danger)' : 'var(--safe)',
        fontFamily: 'monospace',
        fontSize: '1.25rem',
        fontWeight: 'bold',
        textShadow: '0 2px 4px rgba(0,0,0,0.8)'
      }}>
        {alert ? "WARNING: DISTRACTED DRIVING" : "SYSTEM NORMAL"}
      </div>
    </div>
  );
};

export default CameraFeed;
