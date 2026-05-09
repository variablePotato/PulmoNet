/**
 * API service for backend communication.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const REQUEST_TIMEOUT_MS = Number(import.meta.env.VITE_API_TIMEOUT_MS || 60000);
const MAX_RETRIES = Number(import.meta.env.VITE_API_RETRIES || 1);

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const parseErrorMessage = async (response) => {
  try {
    const payload = await response.json();
    return payload.error || payload.detail || 'Request failed';
  } catch {
    return 'Request failed';
  }
};

const requestJson = async (path, options = {}, attempt = 0) => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
      ...options,
      signal: controller.signal,
    });

    if (!response.ok) {
      throw new Error(await parseErrorMessage(response));
    }

    return await response.json();
  } catch (error) {
    const canRetry = attempt < MAX_RETRIES && (error.name === 'AbortError' || !error.message.includes('Invalid'));
    if (canRetry) {
      await delay(300 * (attempt + 1));
      return requestJson(path, options, attempt + 1);
    }

    if (error.name === 'AbortError') {
      throw new Error('The analysis request timed out. Please try again.');
    }
    throw error;
  } finally {
    clearTimeout(timeoutId);
  }
};

const fileToBase64 = (file) => new Promise((resolve, reject) => {
  const reader = new FileReader();
  reader.onload = () => {
    const result = String(reader.result || '');
    resolve(result.includes(',') ? result.split(',', 2)[1] : result);
  };
  reader.onerror = () => reject(new Error(`Unable to read ${file.name}`));
  reader.readAsDataURL(file);
});

const normalizePredictionResponse = (payload) => {
  if (Array.isArray(payload)) {
    return {
      success: true,
      predictions: payload,
      processing_time_ms: null,
      model: null,
    };
  }

  return {
    success: Boolean(payload.success),
    predictions: payload.predictions || [],
    processing_time_ms: payload.processing_time_ms,
    model: payload.model,
  };
};

export const analyzeImages = async (files) => {
  const images = await Promise.all(files.map(async (file) => ({
    filename: file.name,
    content_type: file.type || 'image/png',
    data: await fileToBase64(file),
  })));

  const payload = await requestJson('/analyze', {
    method: 'POST',
    body: JSON.stringify({ input: { images } }),
  });

  return normalizePredictionResponse(payload);
};

export const submitPrediction = async (files) => analyzeImages(files);

export const getPredictionConfig = async () => requestJson('/predict/config');

export const healthCheck = async () => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10000);
  try {
    const response = await fetch(`${API_BASE_URL}/health`, { signal: controller.signal });
    if (!response.ok) {
      throw new Error(await parseErrorMessage(response));
    }
    return await response.json();
  } finally {
    clearTimeout(timeoutId);
  }
};
