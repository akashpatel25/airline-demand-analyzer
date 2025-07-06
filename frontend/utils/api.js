// frontend/utils/api.js
const API_URL = 'http://localhost:8000/api';

// Correct export syntax
export const fetchRoutes = async () => {
  try {
    const response = await fetch(`${API_URL}/popular-routes`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching routes:', error);
    throw error;
  }
};

export const searchFlights = async (params) => {
    try {
      console.log("Sending flight search:", params);
      const response = await fetch(`${API_URL}/flights`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          origin: params.origin.toUpperCase(),
          destination: params.destination.toUpperCase(),
          date: params.date,
          return_date: params.return_date || null
        })
      });
  
      if (!response.ok) {
        let errorData;
        try {
          errorData = await response.json();
        } catch {
          errorData = { detail: await response.text() };
        }
        
        // Handle validation errors differently
        if (response.status === 422) {
          throw new Error(`Validation error: ${errorData.detail}`);
        }
        
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }
  
      return await response.json();
    } catch (error) {
      console.error("Flight search failed:", {
        message: error.message,
        request: params,
        stack: error.stack
      });
      throw error;
    }
  };