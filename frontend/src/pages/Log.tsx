import { type FC, useState, useEffect } from 'react';
import { Chart } from '../components/Charts';
import { FloatingAssistant } from '../components/FloatingAssistant';
import api from '../services/api';

interface Exercise {
  id: number;
  name: string;
  muscle_group: string;
}

interface Workout {
  id: number;
  date: string;
  exercise_id: number;
  weight_kg: number;
  reps: number;
  rir?: number;  // Repeticiones en reserva
  rpe?: number;  // Esfuerzo percibido
}

interface NextWeight {
  next_weight: number;
  reason: string;
}

const Log: FC = () => {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [workouts, setWorkouts] = useState<Workout[]>([]);
  const [selectedExercise, setSelectedExercise] = useState<Exercise | null>(null);
  const [nextWeight, setNextWeight] = useState<NextWeight | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Cargar ejercicios
        const exercisesResponse = await api.get('/exercises');
        setExercises(exercisesResponse.data);
        
        // Cargar entrenamientos
        const workoutsResponse = await api.get('/workouts');
        setWorkouts(workoutsResponse.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);

  const getNextWeight = async (exerciseId: number) => {
    try {
      const response = await api.get(`/suggestions/next-weight?exercise_id=${exerciseId}`);
      setNextWeight(response.data);
    } catch (error) {
      console.error('Error getting next weight:', error);
    }
  };

  const addNewWorkout = async (exerciseId: number, weight: number, reps: number) => {
    try {
      const response = await api.post('/workouts', {
        exercise_id: exerciseId,
        weight_kg: weight,
        reps,
        date: new Date().toISOString()
      });
      setWorkouts(prev => [...prev, response.data]);
      getNextWeight(exerciseId);
    } catch (error) {
      console.error('Error adding workout:', error);
    }
  };


  const chartData = workouts.map((w: Workout) => {
    const exercise = exercises.find(ex => ex.id === w.exercise_id);
    return {
      id: w.id,
      date: w.date,
      value: w.weight_kg,
      label: exercise?.name || 'Desconocido'
    };
  });

  return (
    <div className="container" style={{ padding: '20px' }}>
      <h1>Registro de Entrenamientos</h1>

      <div style={{ marginBottom: '30px' }}>
        <h2>Progreso</h2>
        <Chart
          data={chartData}
          type="line"
          title="Progresión de Peso"
        />
      </div>

      <div style={{ marginBottom: '30px' }}>
        <h2>Registrar Entrenamiento</h2>
        <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
          <select 
            onChange={(e) => {
              const exercise = exercises.find(ex => ex.id === Number(e.target.value));
              setSelectedExercise(exercise || null);
              if (exercise) {
                getNextWeight(exercise.id);
              }
            }}
            style={{
              padding: '8px',
              borderRadius: '4px',
              border: '1px solid #ddd'
            }}
          >
            <option value="">Seleccionar ejercicio</option>
            {exercises.map(ex => (
              <option key={ex.id} value={ex.id}>{ex.name}</option>
            ))}
          </select>

          {selectedExercise && nextWeight && (
            <div style={{
              padding: '10px',
              backgroundColor: '#e9ecef',
              borderRadius: '4px'
            }}>
              <strong>Sugerencia: </strong>
              {nextWeight.next_weight}kg ({nextWeight.reason})
            </div>
          )}
        </div>

        {selectedExercise && (
          <form onSubmit={(e) => {
            e.preventDefault();
            const formData = new FormData(e.currentTarget);
            addNewWorkout(
              selectedExercise.id,
              Number(formData.get('weight')),
              Number(formData.get('reps'))
            );
          }}
          style={{ display: 'flex', gap: '10px', alignItems: 'flex-end' }}
          >
            <div>
              <label style={{ display: 'block', marginBottom: '5px' }}>
                Peso (kg)
                <input
                  type="number"
                  name="weight"
                  step="0.5"
                  defaultValue={nextWeight?.next_weight || ""}
                  required
                  style={{
                    display: 'block',
                    padding: '8px',
                    borderRadius: '4px',
                    border: '1px solid #ddd'
                  }}
                />
              </label>
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '5px' }}>
                Repeticiones
                <input
                  type="number"
                  name="reps"
                  required
                  style={{
                    display: 'block',
                    padding: '8px',
                    borderRadius: '4px',
                    border: '1px solid #ddd'
                  }}
                />
              </label>
            </div>
            <button
              type="submit"
              style={{
                padding: '8px 16px',
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Registrar Serie
            </button>
          </form>
        )}
      </div>

      <div className="workouts-list">
        <h2>Últimos Entrenamientos</h2>
        <table style={{
          width: '100%',
          borderCollapse: 'collapse',
          marginTop: '10px'
        }}>
          <thead>
            <tr>
              <th>Fecha</th>
              <th>Ejercicio</th>
              <th>Peso (kg)</th>
              <th>Reps</th>
            </tr>
          </thead>
          <tbody>
            {workouts.map((workout) => {
              const exercise = exercises.find(ex => ex.id === workout.exercise_id);
              return (
                <tr key={workout.id}>
                  <td>{new Date(workout.date).toLocaleDateString()}</td>
                  <td>{exercise?.name || 'Desconocido'}</td>
                  <td>{workout.weight_kg}</td>
                  <td>{workout.reps}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <FloatingAssistant onSendMessage={(msg) => console.log('Message:', msg)} />
    </div>
  );
}

export default Log;