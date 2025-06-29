import React from 'react';
import { Message } from '../api'; // Assuming Message interface is in api.ts

interface ChatWindowProps {
  messages: Message[];
  currentUser: string | null; // To identify messages sent by the current user
  selectedUser: string | null;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ messages, currentUser, selectedUser }) => {
  if (!selectedUser) {
    // This can be styled better, perhaps a dedicated component or class
    return <div style={{ padding: '20px', textAlign: 'center', flexGrow: 1, alignSelf: 'center', justifySelf: 'center' }}>Select a user to see messages.</div>;
  }

  return (
    // className is "chat-window", App.css handles its flex properties and scrolling
    <div className="chat-window">
      <h3>Chat with {selectedUser}</h3>
      {/* The inner div for messages now. App.css's .chat-window handles column-reverse. */}
      {/* This inner div is for the actual message items if needed for additional structure, or can be removed if .chat-window itself holds messages directly */}
      <div className="chat-window-inner">
        {messages.length === 0 && <p>No messages yet. Start the conversation!</p>}
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`message-bubble ${msg.sender === currentUser ? 'sent' : 'received'}`}
          >
            {/* Optionally show sender name for group chats, or if not clear */}
            {/* <p className="sender-name">{msg.sender}</p> */}
            <p className="message-content">{msg.content}</p>
            <small className="timestamp">
              {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} - {new Date(msg.timestamp).toLocaleDateString()}
            </small>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChatWindow;
