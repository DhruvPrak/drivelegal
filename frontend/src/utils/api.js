// src/utils/api.js
// Central place for all API calls to the backend
// If the backend URL changes, we only update it here

const API_BASE_URL = "http://localhost:8000/api/v1";

// ─── LAWS ─────────────────────────────────────────────────────────────────────

export const lawsAPI = {
  
  // Get all laws with optional filters
  getAll: async (filters = {}) => {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${API_BASE_URL}/laws/?${params}`);
    if (!response.ok) throw new Error("Failed to fetch laws");
    return response.json();
  },

  // Get all categories
  getCategories: async () => {
    const response = await fetch(`${API_BASE_URL}/laws/categories`);
    if (!response.ok) throw new Error("Failed to fetch categories");
    return response.json();
  },

  // Get law by ID
  getById: async (id) => {
    const response = await fetch(`${API_BASE_URL}/laws/${id}`);
    if (!response.ok) throw new Error("Failed to fetch law");
    return response.json();
  },
};

// ─── FINES ────────────────────────────────────────────────────────────────────

export const finesAPI = {
  
  // Calculate challan
  calculate: async (section, stateCode, vehicleType, isRepeat = false) => {
    const params = new URLSearchParams({
      section,
      state_code: stateCode,
      vehicle_type: vehicleType,
      is_repeat: isRepeat,
    });
    const response = await fetch(`${API_BASE_URL}/fines/calculate?${params}`);
    if (!response.ok) throw new Error("Failed to calculate fine");
    return response.json();
  },
};

// ─── RTO ──────────────────────────────────────────────────────────────────────

export const rtoAPI = {
  
  // Get nearest RTO offices
  getNearest: async (lat, lng, limit = 5) => {
    const params = new URLSearchParams({ lat, lng, limit });
    const response = await fetch(`${API_BASE_URL}/rto/nearest?${params}`);
    if (!response.ok) throw new Error("Failed to fetch RTO offices");
    return response.json();
  },

  // Get RTO by state
  getByState: async (stateCode) => {
    const response = await fetch(`${API_BASE_URL}/rto/state/${stateCode}`);
    if (!response.ok) throw new Error("Failed to fetch RTOs");
    return response.json();
  },
};