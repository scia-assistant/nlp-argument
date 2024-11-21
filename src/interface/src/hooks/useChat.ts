import { useState } from 'react';
import { MessageProps } from 'components/Message'
import postRequest from './requests';

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
