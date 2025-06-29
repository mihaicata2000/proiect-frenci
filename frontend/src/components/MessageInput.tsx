import React, { useState } from 'react';

interface MessageInputProps {
  selectedUser: string | null;
  currentUser: string; // The user sending the message
  onSendMessage: (receiver: string, content: string) => Promise<boolean>; // Returns true on success
}

const MessageInput: React.FC<MessageInputProps> = ({ selectedUser, currentUser, onSendMessage }) => {
  const [messageContent, setMessageContent] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!messageContent.trim() || !selectedUser) return;

    const success = await onSendMessage(selectedUser, messageContent);
    if (success) {
      setMessageContent(''); // Clear input only on successful send
    } else {
      // Optionally, handle send failure (e.g., show an error message)
      alert('Failed to send message. Please try again.');
    }
  };

  if (!selectedUser) {
    return null; // Don't show input if no user is selected
  }

  return (
    // Use className from App.css
    <form onSubmit={handleSubmit} className="message-input-form">
      <input
        type="text"
        value={messageContent}
        onChange={(e) => setMessageContent(e.target.value)}
        placeholder={`Message ${selectedUser}...`}
        // Inline styles removed, handled by .message-input-form input in App.css
        disabled={!selectedUser}
      />
      <button type="submit" disabled={!selectedUser || !messageContent.trim()}>
        Send
      </button>
    </form>
  );
};

export default MessageInput;
