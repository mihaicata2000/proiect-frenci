import React, { useState, useEffect, useCallback } from 'react';
import UserList from './components/UserList';
import ChatWindow from './components/ChatWindow';
import MessageInput from './components/MessageInput';
import * as api from './api'; // Using * as api to namespace imports
import './App.css';

function App() {
  const [users, setUsers] = useState<string[]>([]);
  const [selectedUser, setSelectedUser] = useState<string | null>(null);
  const [messages, setMessages] = useState<api.Message[]>([]);
  // For simplicity, let's assume the current user is hardcoded or chosen.
  // In a real app, this would come from authentication.
  const [currentUser, setCurrentUser] = useState<string | null>(null);
  const [usernameInput, setUsernameInput] = useState<string>('');


  const fetchUsers = useCallback(async () => {
    const fetchedUsers = await api.getUsers();
    // Filter out the current user from the list of other users
    setUsers(fetchedUsers.filter(u => u !== currentUser));
  }, [currentUser]);

  const fetchMessages = useCallback(async (user: string) => {
    if (!currentUser) return; // Ensure current user is set
    // We want messages between currentUser and 'user'
    // The backend's get_messages/<username> gets all messages where <username> is sender OR receiver.
    // So, fetching for selectedUser should be enough if backend handles it correctly.
    // However, our current backend get_messages is user-centric (all messages for that user).
    // For a direct chat, we might need to refine this or filter client-side.
    // Let's assume for now `getMessages(selectedUser)` returns all messages involving selectedUser,
    // and we filter them or the backend API `/get_messages/<user1>/<user2>` would be better.
    // Given current backend: fetch all for current user, then filter.
    const fetchedMessages = await api.getMessages(currentUser);

    // Filter messages to show only conversation with selectedUser
    const conversationMessages = fetchedMessages.filter(
      msg => (msg.sender === currentUser && msg.receiver === user) || (msg.sender === user && msg.receiver === currentUser)
    );
    setMessages(conversationMessages.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()));
  }, [currentUser]);


  useEffect(() => {
    if (currentUser) {
      fetchUsers();
    }
  }, [currentUser, fetchUsers]);

  useEffect(() => {
    if (selectedUser && currentUser) {
      fetchMessages(selectedUser);
      // Optional: Set up polling for new messages
      const intervalId = setInterval(() => fetchMessages(selectedUser), 5000); // Poll every 5 seconds
      return () => clearInterval(intervalId);
    } else {
      setMessages([]); // Clear messages if no user is selected
    }
  }, [selectedUser, currentUser, fetchMessages]);

  const handleSelectUser = (user: string) => {
    setSelectedUser(user);
  };

  const handleSendMessage = async (receiver: string, content: string): Promise<boolean> => {
    if (!currentUser) {
      alert("Please set your username first.");
      return false;
    }
    const success = await api.sendMessage(currentUser, receiver, content);
    if (success) {
      // Optimistically add message to UI or re-fetch
      // For simplicity, re-fetch messages for the selected user
      if (selectedUser) {
        fetchMessages(selectedUser);
      }
      fetchUsers(); // Refresh user list in case a new user was messaged
    }
    return success;
  };

  const handleSetCurrentUser = () => {
    if (usernameInput.trim()) {
      setCurrentUser(usernameInput.trim());
    } else {
      alert("Username cannot be empty.");
    }
  };

  if (!currentUser) {
    return (
      // Use classes from App.css for the login view
      <div className="login-container">
        <div className="login-box">
          <h2>Enter Your Username</h2>
          <input
            type="text"
            value={usernameInput}
            onChange={(e) => setUsernameInput(e.target.value)}
            placeholder="Your username"
            // Inline styles removed
          />
          <button onClick={handleSetCurrentUser}>
            Start Chatting
          </button>
        </div>
      </div>
    );
  }

  return (
    // className "app-container" is already set, inline styles removed
    <div className="app-container">
      {/* className "sidebar" is already set, inline styles removed */}
      <div className="sidebar">
        <UserList users={users} selectedUser={selectedUser} onSelectUser={handleSelectUser} />
      </div>
      {/* className "main-chat-area" is already set, inline styles removed */}
      <div className="main-chat-area">
        <ChatWindow messages={messages} currentUser={currentUser} selectedUser={selectedUser} />
        {selectedUser && (
          <MessageInput
            selectedUser={selectedUser}
            currentUser={currentUser}
            onSendMessage={handleSendMessage}
          />
        )}
      </div>
    </div>
  );
}

export default App;
