import { type FC, useState, useEffect } from 'react';
import { FloatingAssistant } from '../components/FloatingAssistant';
import api from '../services/api';

interface Exercise {
  id: number;
  name: string;
  muscle_group: string;
  description: string;
  youtube_url: string;
}

const Library: FC = () => {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [selectedExercise, setSelectedExercise] = useState<Exercise | null>(null);
  const [showVideoModal, setShowVideoModal] = useState(false);

  useEffect(() => {
    const fetchExercises = async () => {
      try {
        const response = await api.get('/exercises');
        setExercises(response.data);
      } catch (error) {
        console.error('Error fetching exercises:', error);
      }
    };
    fetchExercises();
  }, []);

  const getYoutubeEmbedUrl = (url: string) => {
    const videoId = url.split('v=')[1];
    return `https://www.youtube.com/embed/${videoId}`;
  };

  return (
    <div className="container" style={{ padding: '20px' }}>
      <h1>Biblioteca de Ejercicios</h1>
      
      <div className="exercises-grid" style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
        gap: '20px',
        marginTop: '20px'
      }}>
        {exercises.map((exercise) => (
          <div key={exercise.id} className="exercise-card" style={{
            padding: '20px',
            border: '1px solid #ddd',
            borderRadius: '8px',
            background: 'white'
          }}>
            <h3>{exercise.name}</h3>
            <p><strong>Grupo Muscular:</strong> {exercise.muscle_group}</p>
            <p>{exercise.description}</p>
            <div style={{ display: 'flex', gap: '10px' }}>
              <button 
                onClick={() => {
                  setSelectedExercise(exercise);
                  setShowVideoModal(true);
                }}
                style={{
                  background: '#007bff',
                  color: 'white',
                  border: 'none',
                  padding: '8px 16px',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                Ver Tutorial
              </button>
              <button 
                onClick={() => {
                  // TODO: Implementar añadir a rutina
                }}
                style={{
                  background: '#28a745',
                  color: 'white',
                  border: 'none',
                  padding: '8px 16px',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                Añadir a Rutina
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Modal para video tutorial */}
      {showVideoModal && selectedExercise && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0,0,0,0.7)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 1000
        }}>
          <div style={{
            background: 'white',
            padding: '20px',
            borderRadius: '8px',
            width: '80%',
            maxWidth: '800px'
          }}>
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              marginBottom: '15px'
            }}>
              <h3>{selectedExercise.name}</h3>
              <button
                onClick={() => setShowVideoModal(false)}
                style={{
                  background: 'none',
                  border: 'none',
                  fontSize: '24px',
                  cursor: 'pointer'
                }}
              >
                ×
              </button>
            </div>
            <iframe
              width="100%"
              height="450"
              src={getYoutubeEmbedUrl(selectedExercise.youtube_url)}
              title={`Tutorial de ${selectedExercise.name}`}
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>
        </div>
      )}

      <FloatingAssistant onSendMessage={(msg) => console.log('Message:', msg)} />
    </div>
  );
}

export default Library;
