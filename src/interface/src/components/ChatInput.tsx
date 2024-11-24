import React, { useState } from 'react';
import 'styles/ChatInput.css';
import { useNavigate } from "react-router-dom";

interface ChatInputProps {
  onSend: (message: string) => void;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSend }) => {
  const [inputValue, setInputValue] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (inputValue.trim()) {
      try {
        await onSend(inputValue);
        setInputValue('');
      } catch (error) {
        navigate("/");
      }
    }
  };

  return (
    <form className="chat-input" onSubmit={handleSubmit}>
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        placeholder="Type your message"
        className="chat-input-field"
      />
      <button type="submit" className="chat-input-button">Send</button>
    </form>
  );
};

export default ChatInput;
