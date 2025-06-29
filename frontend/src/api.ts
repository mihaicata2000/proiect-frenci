import axios from 'axios';

const API_URL = 'http://localhost:5000'; // Assuming backend runs on port 5000

export interface Message {
  id: number;
  sender: string;
  receiver: string;
  content: string;
  timestamp: string; // ISO string format
}

export const getUsers = async (): Promise<string[]> => {
  try {
    const response = await axios.get<{ users: string[] }>(`${API_URL}/get_users`);
    return response.data.users;
  } catch (error) {
    console.error("Error fetching users:", error);
    return [];
  }
};

export const getMessages = async (username: string): Promise<Message[]> => {
  try {
    const response = await axios.get<{ messages: Message[] }>(`${API_URL}/get_messages/${username}`);
    return response.data.messages;
  } catch (error) {
    console.error(`Error fetching messages for ${username}:`, error);
    return [];
  }
};

export const sendMessage = async (sender: string, receiver: string, content: string): Promise<boolean> => {
  try {
    await axios.post(`${API_URL}/send_message`, { sender, receiver, content });
    return true;
  } catch (error) {
    console.error("Error sending message:", error);
    return false;
  }
};
