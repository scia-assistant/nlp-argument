
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import ChatWindow from 'pages/ChatWindow';
import Login from 'pages/login';
import 'styles/App.css'; // Import global styles if needed

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/chat" element={<ChatWindow />} />
      </Routes>
    </Router>
  );
};

export default App;

