import { useState } from 'react';
import { api, PredictionInput, PredictionResult } from '@/services/api';

export function usePrediction() {
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const predict = async (input: PredictionInput) => {
    setLoading(true);
    setError(null);

    try {
      const data = await api.predict(input);
      setResult(data);
      return data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Failed to get prediction';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return {
    result,
    loading,
    error,
    predict,
    setResult,
  };
}
