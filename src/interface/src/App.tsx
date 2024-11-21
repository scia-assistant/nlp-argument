
import React from 'react';
import ChatWindow from 'components/ChatWindow';
import 'styles/App.css'; // Import global styles if needed

const App: React.FC = () => {
  return (
    <div className="app">
      <h1 className="app-title">Chat Interface</h1>
      <ChatWindow />
    </div>
  );
};

export default App;

