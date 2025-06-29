# Simple Messaging App

This is a simple messaging application with a Python/Flask backend and a React frontend.

## Project Structure

```
.
├── backend/
│   ├── venv/                   # Python virtual environment
│   ├── app.py                  # Flask application
│   ├── messages.db             # SQLite database file
│   ├── test_app.py             # Backend unit tests
│   └── ...
├── frontend/
│   ├── node_modules/           # Node.js dependencies
│   ├── public/                 # Public assets for React app
│   ├── src/                    # React app source code
│   │   ├── components/         # React components
│   │   ├── App.tsx             # Main React app component
│   │   ├── App.css             # Main styles
│   │   ├── api.ts              # Frontend API call helpers
│   │   └── ...
│   ├── package.json            # Frontend dependencies and scripts
│   └── ...
├── .gitignore                  # Files and directories to ignore
└── README.md                   # This file
```

## Setup and Running

**Prerequisites:**
*   Python 3.8+ and `pip`
*   Node.js (which includes `npm`) v16+

**1. Backend Setup**

   Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

   Create a Python virtual environment:
   ```bash
   python3 -m venv venv
   ```

   Activate the virtual environment:
   *   On macOS and Linux:
       ```bash
       source venv/bin/activate
       ```
   *   On Windows:
       ```bash
       .\venv\Scripts\activate
       ```

   Install the required Python packages:
   ```bash
   pip install Flask Flask-SQLAlchemy Flask-CORS
   ```

   Run the backend server:
   ```bash
   python app.py
   ```
   The backend will start on `http://localhost:5000`. The `messages.db` SQLite file will be created in the `backend` directory when the server starts and the first database operation occurs.

**2. Frontend Setup**

   In a new terminal, navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

   Install Node.js dependencies:
   ```bash
   npm install
   ```

   Run the React development server:
   ```bash
   npm start
   ```
   The frontend development server will start, usually on `http://localhost:3000`, and should open automatically in your web browser.

**3. Using the App**

*   Open your browser to `http://localhost:3000` (if it doesn't open automatically).
*   Enter a username for yourself to start.
*   To chat with another "user", you would typically open another browser window (perhaps in incognito mode to simulate a different session) and enter a different username.
*   Send messages. Users will appear in the user list as they send or receive messages.

## Running Tests

**Backend Tests**

   Ensure your virtual environment is activated in the `backend` directory.
   ```bash
   cd backend
   source venv/bin/activate # Or .\venv\Scripts\activate
   python -m unittest test_app.py
   ```

**Frontend Tests**

   Navigate to the `frontend` directory.
   ```bash
   cd frontend
   npm test
   ```
   (Note: This will run the default React Jest tests. More specific tests for components would need to be added.)

## Building Frontend for Production

   Navigate to the `frontend` directory.
   ```bash
   cd frontend
   npm run build
   ```
   This will create an optimized static build in the `frontend/build` directory.

## API Endpoints (Backend)

*   `POST /send_message`
    *   JSON Body: `{"sender": "username1", "receiver": "username2", "content": "Hello!"}`
    *   Response: `{"message": "Message sent successfully!"}` (201)
*   `GET /get_messages/<username>`
    *   Response: `{"messages": [{"id": 1, "sender": "...", "receiver": "...", "content": "...", "timestamp": "ISO_string"}, ...]}` (200)
*   `GET /get_users`
    *   Response: `{"users": ["username1", "username2", ...]}` (200)

CORS is enabled for all routes, allowing requests from `http://localhost:3000`.
