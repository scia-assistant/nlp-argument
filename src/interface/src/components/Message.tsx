import React from 'react';
import 'styles/Message.css';

export interface MessageProps {
  text: string;
  isBot: boolean;
  dataTestid: string;
}

const Message: React.FC<MessageProps> = ({ text, isBot, dataTestid }) => {
  return (
    <div className={isBot ? 'message bot-message' : 'message user-message'} data-testid={dataTestid} >
      {text}
    </div>
  );
};

export default Message;
