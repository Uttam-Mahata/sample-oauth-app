import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

interface User {
  name: string;
  email: string;
  picture: string;
}

const API_BASE_URL = 'http://localhost:8000';

// Configure axios to send credentials (cookies) with every request
axios.defaults.withCredentials = true;

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/me`);
      setUser(response.data);
    } catch (error) {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = () => {
    // Redirect to the backend login route
    window.location.href = `${API_BASE_URL}/login`;
  };

  const logout = async () => {
    try {
      // We can either redirect to backend logout or just call it
      window.location.href = `${API_BASE_URL}/logout`;
    } catch (error) {
      console.error('Logout failed', error);
    }
  };

  if (loading) {
    return <div className="App">Loading...</div>;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>FastAPI + React Google OAuth</h1>
        
        {user ? (
          <div className="profile-card">
            <img src={user.picture} alt={user.name} className="profile-pic" />
            <h2>Welcome, {user.name}</h2>
            <p>{user.email}</p>
            <button onClick={logout} className="logout-button">Logout</button>
          </div>
        ) : (
          <div className="login-container">
            <p>Please sign in to continue</p>
            <button onClick={login} className="login-button">
              Sign in with Google
            </button>
          </div>
        )}
      </header>
    </div>
  )
}

export default App