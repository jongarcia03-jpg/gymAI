export interface Workout {
  id: number;
  date: string;
  exercise: string;
  weight: number;
  reps: number;
}

import React from 'react';

export interface ChartData {
  id: number;
  date: string;
  value: number;
  label: string;
}

export interface ChartProps {
  data: ChartData[];
  type: 'line' | 'bar' | 'pie';
  title: string;
}

export interface Workout {
  id: number;
  date: string;
  exercise: string;
  weight: number;
  reps: number;
}

export interface FormEvent extends React.FormEvent<HTMLFormElement> {
  preventDefault(): void;
}

export interface ChangeEvent extends React.ChangeEvent<HTMLInputElement> {
  target: HTMLInputElement;
}

export interface FloatingAssistantProps {
  onSendMessage: (message: string) => void;
}