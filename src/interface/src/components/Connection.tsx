import React, { useState } from 'react';
import tryToLog from 'hooks/login';
import { useNavigate } from "react-router-dom";
import 'styles/Login.css'



const Connect: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (event: React.FormEvent) => {
    setError("")
    event.preventDefault();
    try {
      await tryToLog(username, password)
      navigate("/chat");
    } catch (error: any) {
      if (error.status === 401)
        setError("Login or Password incorrect !")
      else
        setError("Problem server...")
    }
  };

  return (
    <div className='login-page'>
      <h1 className="login-header1">Welcome to ChatGPTW</h1>
      <h1 className="login-header2">The meaning of the final "W" represents "wish"</h1>
      <form onSubmit={handleLogin}>
        <div>
          <input
            data-testid="login-username"
            className='login-input'
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            data-testid="login-password"
            className='login-input'
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit" data-testid="login-button" className='login-button'>Login</button>
      </form>
      {error && <p data-testid="login-error-display" style={{ color: "red" }}>{error}</p>}
    </div>
  );
};

export default Connect;
