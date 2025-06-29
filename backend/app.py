from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50), nullable=False)
    receiver = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Message {self.id}>'

# API endpoint to send a message
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    new_message = Message(
        sender=data['sender'],
        receiver=data['receiver'],
        content=data['content']
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message sent successfully!'}), 201

# API endpoint to retrieve messages for a user
@app.route('/get_messages/<username>', methods=['GET'])
def get_messages(username):
    # Retrieve messages where the user is either the sender or receiver
    messages_sent = Message.query.filter_by(sender=username).all()
    messages_received = Message.query.filter_by(receiver=username).all()

    # Combine and sort messages by timestamp
    all_messages = sorted(
        messages_sent + messages_received,
        key=lambda m: m.timestamp
    )

    output = []
    for message in all_messages:
        message_data = {
            'id': message.id,
            'sender': message.sender,
            'receiver': message.receiver,
            'content': message.content,
            'timestamp': message.timestamp.isoformat() # Use ISO format for JS compatibility
        }
        output.append(message_data)
    return jsonify({'messages': output})

# API endpoint to list all unique users
@app.route('/get_users', methods=['GET'])
def get_users():
    senders = db.session.query(Message.sender).distinct().all()
    receivers = db.session.query(Message.receiver).distinct().all()

    users = set()
    for sender in senders:
        users.add(sender[0])
    for receiver in receivers:
        users.add(receiver[0])

    return jsonify({'users': list(users)})

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Create database tables if they don't exist
    app.run(debug=True)
