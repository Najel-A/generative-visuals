export const API_URL = process.env.REACT_APP_API_URL;

export const uploadAudio = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_URL}/upload`, {
      method: 'POST',
      body: formData,
      headers: {
        'Accept': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Upload failed');
    }

    return await response.json();
  } catch (error) {
    throw new Error('API Error: ' + error.message);
  }
};

export const getAnalysis = async (fileId) => {
  try {
    const response = await fetch(`${API_URL}/analysis/${fileId}`);
    if (!response.ok) {
      throw new Error('Analysis failed');
    }
    return await response.json();
  } catch (error) {
    throw new Error('API Error: ' + error.message);
  }
};