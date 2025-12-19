import axios from 'axios';

const API_BASE = 'https://crewsync-api-62cn.onrender.com/api';

export const api = {
  // Dashboard
  getDashboardStats: () => axios.get(`${API_BASE}/dashboard/stats`),
  
  // Flights
  getAllFlights: () => axios.get(`${API_BASE}/flights`),
  getFlightById: (flightNumber) => axios.get(`${API_BASE}/flights/${flightNumber}`),
  
  // Crew
  getAllCrew: () => axios.get(`${API_BASE}/crew`),
  getCrewById: (empId) => axios.get(`${API_BASE}/crew/${empId}`),
  
  // Recommendations
  getRecommendations: (flightNumber) => axios.get(`${API_BASE}/recommendations/${flightNumber}`),
  
  // Health
  healthCheck: () => axios.get(`${API_BASE}/health`),
};

export default api;
