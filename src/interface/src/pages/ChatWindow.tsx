import React from 'react';
import ChatInput from 'components/ChatInput';
import Message from 'components/Message';
import useChat from 'hooks/useChat';
import 'styles/ChatWindow.css'

const ChatWindow: React.FC = () => {
  const { messages, sendMessage } = useChat();

  return (
    <div className="chat-window">
      <div className="scrollable">
        {messages.map((msg, index) => (
          <Message key={index} text={msg.text} isBot={msg.isBot} dataTestid={`message-${index}`} />
        ))}
      </div>
      <ChatInput onSend={sendMessage} />
    </div>
  );
};

export default ChatWindow;
