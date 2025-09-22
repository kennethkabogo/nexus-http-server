import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';

function App() {
  const [token, setToken] = useState(localStorage.getItem('jwt_token'));
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState('');

  useEffect(() => {
    if (token) {
      localStorage.setItem('jwt_token', token);
    } else {
      localStorage.removeItem('jwt_token');
    }
  }, [token]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoginError('');

    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        setToken(data.token);
      } else {
        setLoginError(data.message || 'Login failed');
      }
    } catch (error) {
      console.error('Login error:', error);
      setLoginError('Network error or server unreachable');
    }
  };

  const handleLogout = () => {
    setToken(null);
    setUsername('');
    setPassword('');
  };

  if (!token) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: '#f0f2f5' }}>
        <div style={{ padding: '40px', borderRadius: '8px', boxShadow: '0 4px 8px rgba(0,0,0,0.1)', backgroundColor: 'white', textAlign: 'center' }}>
          <h2>Login</h2>
          <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              style={{ padding: '10px', borderRadius: '4px', border: '1px solid #ccc' }}
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{ padding: '10px', borderRadius: '4px', border: '1px solid #ccc' }}
            />
            <button type="submit" style={{ padding: '10px 20px', borderRadius: '4px', border: 'none', backgroundColor: '#007bff', color: 'white', cursor: 'pointer' }}>
              Login
            </button>
            {loginError && <p style={{ color: 'red', marginTop: '10px' }}>{loginError}</p>}
          </form>
        </div>
      </div>
    );
  }

  return (
    <div>
      <header style={{ padding: '10px 20px', backgroundColor: '#007bff', color: 'white', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Dashboard</h1>
        <button onClick={handleLogout} style={{ padding: '8px 15px', borderRadius: '4px', border: 'none', backgroundColor: '#dc3545', color: 'white', cursor: 'pointer' }}>
          Logout
        </button>
      </header>
      <Dashboard token={token} /> {/* Pass token to Dashboard if needed */}
    </div>
  );
}

export default App;