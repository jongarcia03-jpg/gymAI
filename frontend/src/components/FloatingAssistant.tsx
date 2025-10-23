import React, { useState } from 'react';

interface FloatingAssistantProps {
  onSendMessage: (message: string) => void;
}

export function FloatingAssistant({ onSendMessage }: FloatingAssistantProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      onSendMessage(message);
      setMessage('');
    }
  };

  return (
    <div className={`floating-assistant ${isOpen ? 'open' : ''}`} style={{
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      backgroundColor: 'white',
      borderRadius: '12px',
      boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
      padding: isOpen ? '20px' : '10px',
      transition: 'all 0.3s ease'
    }}>
      {!isOpen ? (
        <button onClick={() => setIsOpen(true)} style={{
          border: 'none',
          background: 'none',
          cursor: 'pointer',
          fontSize: '24px'
        }}>
          💪
        </button>
      ) : (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
            <h4 style={{ margin: 0 }}>Asistente GymAI</h4>
            <button onClick={() => setIsOpen(false)} style={{
              border: 'none',
              background: 'none',
              cursor: 'pointer'
            }}>×</button>
          </div>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              value={message}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setMessage(e.target.value)}
              placeholder="Pregunta algo..."
              style={{
                width: '200px',
                padding: '8px',
                marginRight: '8px',
                border: '1px solid #ddd',
                borderRadius: '4px'
              }}
            />
            <button type="submit" style={{
              padding: '8px 16px',
              background: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}>Enviar</button>
          </form>
        </div>
      )}
    </div>
  );
}