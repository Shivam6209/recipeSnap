// API Configuration
const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8001',
  ENDPOINTS: {
    FULL_ANALYSIS: '/full-analysis',
    ANALYZE_INGREDIENTS: '/analyze-ingredients',
    GENERATE_RECIPES: '/generate-recipes',
    HEALTH_CHECK: '/'
  }
};

export default API_CONFIG; 