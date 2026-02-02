import axios from 'axios';

const API_BASE_URL = '/api';

export interface PredictionInput {
  food_type: string;
  temperature: number;
  humidity: number;
  storage_type: string;
  days_stored: number;
}

export interface PredictionResult {
  food_type: string;
  storage_type: string;
  temperature: number;
  humidity: number;
  days_stored: number;
  predicted_remaining_days: number;
  raw_prediction: number;
  safety_classification: 'Safe' | 'Consume Soon' | 'Expired';
  issues: string[];
  severity: string;
  recommendations: string[];
  feature_importance: Record<string, number>;
}

export const api = {
  async healthCheck() {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  },

  async predict(input: PredictionInput): Promise<PredictionResult> {
    const response = await axios.post(`${API_BASE_URL}/predict`, input);
    return response.data;
  },

  async explain(input: PredictionInput) {
    const response = await axios.post(`${API_BASE_URL}/explain`, input);
    return response.data;
  },

  async getVoiceExplanation(input: PredictionInput): Promise<Blob> {
    const response = await axios.post(`${API_BASE_URL}/voice/explain`, input, {
      responseType: 'blob',
    });
    return response.data;
  },

  async chat(message: string, context?: string) {
    const response = await axios.post(`${API_BASE_URL}/chat`, {
      message,
      context,
    });
    return response.data;
  },

  async getPredictionExplanation(input: PredictionInput) {
    const response = await axios.post(`${API_BASE_URL}/chat/prediction_explanation`, input);
    return response.data;
  },

  async getStorageAdvice(food_type: string, storage_conditions?: Record<string, any>) {
    const response = await axios.post(`${API_BASE_URL}/chat/storage_advice`, {
      food_type,
      storage_conditions,
    });
    return response.data;
  },
};
