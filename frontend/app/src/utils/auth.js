const TOKEN_KEY = 'auth';
const ACCESS_LEVELS_KEY = 'access_levels';

export const saveTokens = (token, accessLevels = null) => {
  try {
    localStorage.setItem(TOKEN_KEY, token);
    if (accessLevels) {
      localStorage.setItem(
        ACCESS_LEVELS_KEY, 
        typeof accessLevels === 'string' ? accessLevels : JSON.stringify(accessLevels)
      );
    }
    return true;
  } catch (error) {
    console.error('Failed to save authentication data:', error);
    return false;
  }
};

export const clearTokens = () => {
  try {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(ACCESS_LEVELS_KEY);
    return true;
  } catch (error) {
    console.error('Failed to clear authentication data:', error);
    return false;
  }
};

export const getToken = () => {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch (error) {
    console.error('Failed to get authentication token:', error);
    return null;
  }
};

export const getAccessLevels = () => {
  try {
    const levelsStr = localStorage.getItem(ACCESS_LEVELS_KEY);
    return levelsStr ? JSON.parse(levelsStr) : null;
  } catch (error) {
    console.error('Failed to get access levels:', error);
    return null;
  }
};

export const isAuthenticated = () => {
  return !!getToken();
}; 