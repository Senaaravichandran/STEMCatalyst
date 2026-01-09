import axios from 'axios';

const API_BASE_URL = (process.env.REACT_APP_API_URL || 'http://localhost:5000') + '/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.baseURL}${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.statusText);
    return response;
  },
  (error) => {
    console.error('API Error:', {
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      message: error.message
    });
    return Promise.reject(error);
  }
);

export const ApiService = {
  // Problem solving
  async solveProblem(problemData) {
    try {
      const response = await apiClient.post('/solve', problemData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to solve problem');
    }
  },

  // Concept explanation
  async explainConcept(conceptData) {
    try {
      const response = await apiClient.post('/explain', conceptData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to explain concept');
    }
  },

  // Formula reference
  async getFormulas(formulaData) {
    try {
      const response = await apiClient.post('/formulas', formulaData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get formulas');
    }
  },

  // Study tips
  async getStudyTips(studyData) {
    try {
      const response = await apiClient.post('/study-tips', studyData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get study tips');
    }
  },

  // Search problems
  async searchProblems(searchData) {
    try {
      const response = await apiClient.post('/search-problems', searchData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to search problems');
    }
  },

  // Get available datasets
  async getDatasets() {
    try {
      const response = await apiClient.get('/datasets');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get datasets');
    }
  },

  // Health check
  async healthCheck() {
    try {
      const healthUrl = (process.env.REACT_APP_API_URL || 'http://localhost:5000') + '/health';
      const response = await axios.get(healthUrl);
      return response.data;
    } catch (error) {
      throw new Error('API health check failed');
    }
  },
};

export default ApiService;