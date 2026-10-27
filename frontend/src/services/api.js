
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

async function request(endpoint) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`);

  if (!response.ok) {
    const message = await response.text();
    throw new Error(`API error ${response.status}: ${message}`);
  }

  return response.json();
}

export function getOverview(date) {
  return request(`/api/overview?date=${date}`);
}

export function getAccuracy(startDate, endDate) {
  return request(
    `/api/accuracy?start_date=${startDate}&end_date=${endDate}`
  );
}

export function getForecasts(date) {
  return request(`/api/forecasts?date=${date}`);
}
