import React, { useState } from 'react';
import tryToLog from 'hooks/login';
import { useNavigate } from "react-router-dom";
import axios from "axios"
import 'styles/Login.css'

interface ApiResponse {
  response: string;
}

axios.defaults.baseURL = "/api";


const Connect: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (event: React.FormEvent) => {
    setError("")
    event.preventDefault();
    const statusLoged = await tryToLog(username, password)
    if (statusLoged === 200)
    {
    
      const token = localStorage.getItem('token');
  console.log(token)

  if (!token) {
    throw new Error("Unauthorized: Token not found.");
  }
try{
  const apiResp = await axios.post<ApiResponse>(
    '/model',
    { question: "toto" },
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  );
  console.log(apiResp)
  navigate("/chat");
}
catch(e){
  console.log(e)
}

    }

    else if (statusLoged === 401)
      setError("Login or Password incorrect !")
    else
      setError("Problem server...")
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
