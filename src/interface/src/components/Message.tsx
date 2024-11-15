import React from 'react';
import 'styles/Message.css';

export interface MessageProps {
  text: string;
  isBot: boolean;
}

const Message: React.FC<MessageProps> = ({ text, isBot }) => {
  return (
    <div className={isBot ? 'message bot-message' : 'message user-message'}>
      {text}
    </div>
  );
};

export default Message;
