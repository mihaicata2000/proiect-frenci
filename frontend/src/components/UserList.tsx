import React from 'react';

interface UserListProps {
  users: string[];
  selectedUser: string | null;
  onSelectUser: (user: string) => void;
}

const UserList: React.FC<UserListProps> = ({ users, selectedUser, onSelectUser }) => {
  return (
    // className is already "user-list" which is good.
    // Removed inline styles, assuming they are handled by App.css for .user-list and its children
    <div className="user-list">
      <h2>Users</h2>
      {users.length === 0 && <p>No users found. Send a message to populate users.</p>}
      <ul>
        {users.map((user) => (
          <li
            key={user}
            onClick={() => onSelectUser(user)}
            className={user === selectedUser ? 'selected' : ''} // Apply 'selected' class
          >
            {user}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UserList;
