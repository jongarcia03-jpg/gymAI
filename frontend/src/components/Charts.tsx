import React from 'react';
import type { ChartProps, ChartData } from '../types';

export const Chart: React.FC<ChartProps> = ({ data, type = 'line', title }) => {
  // Por ahora un placeholder - podemos usar recharts o similar después
  return (
    <div className="chart-container">
      <h3>{title}</h3>
      <div className="chart-placeholder" style={{
        width: '100%',
        height: '200px',
        background: '#f0f0f0',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column'
      }}>
        {type} chart with {data.length} data points
        <div style={{ marginTop: '10px', fontSize: '0.9em' }}>
          {data.map((point: ChartData) => (
            <div key={point.id}>
              {point.date} - {point.label}: {point.value}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}