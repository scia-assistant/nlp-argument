import { useState } from 'react';
import postRequest from './requests';

export interface MessageProps {
  text: string;
  isBot: boolean;
}

function useChat() {
  const [messages, setMessages] = useState<MessageProps[]>([]);

  const sendMessage = async (text: string) => {
    setMessages([...messages, { text, isBot: false }]);

    // Simulate bot response
    const botResponse: string = await postRequest(text);
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: botResponse, isBot: true },
    ]);
  };
  return { messages, sendMessage };
};

export default useChat;
