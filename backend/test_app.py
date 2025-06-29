import unittest
import os
from app import app, db, Message # Import from your main app file
import datetime

class MessageModelCase(unittest.TestCase):
    def setUp(self):
        # Configure the app for testing
        # Use a separate test database or in-memory
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['TESTING'] = True
        self.app_context = app.app_context()
        self.app_context.push() # Push an application context
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop() # Pop the application context
        if os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db')):
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db'))

    def test_create_and_retrieve_message(self):
        # Test creating a message
        timestamp_before = datetime.datetime.utcnow()
        msg1 = Message(sender='Alice', receiver='Bob', content='Hello Bob!')
        db.session.add(msg1)
        db.session.commit()
        timestamp_after = datetime.datetime.utcnow()

        # Test retrieving the message
        retrieved_msg = Message.query.filter_by(sender='Alice').first()
        self.assertIsNotNone(retrieved_msg)
        self.assertEqual(retrieved_msg.receiver, 'Bob')
        self.assertEqual(retrieved_msg.content, 'Hello Bob!')

        # Check timestamp is within expected range
        self.assertTrue(timestamp_before <= retrieved_msg.timestamp <= timestamp_after)

    def test_multiple_messages(self):
        msg1 = Message(sender='Alice', receiver='Bob', content='Meeting at 10?')
        msg2 = Message(sender='Bob', receiver='Alice', content='Sure, sounds good.')
        msg3 = Message(sender='Charlie', receiver='Alice', content='Hi Alice!')

        db.session.add_all([msg1, msg2, msg3])
        db.session.commit()

        alice_sent_count = Message.query.filter_by(sender='Alice').count()
        self.assertEqual(alice_sent_count, 1)

        alice_received_count = Message.query.filter_by(receiver='Alice').count()
        self.assertEqual(alice_received_count, 2)

        bob_messages_to_alice = Message.query.filter_by(sender='Bob', receiver='Alice').all()
        self.assertEqual(len(bob_messages_to_alice), 1)
        self.assertEqual(bob_messages_to_alice[0].content, 'Sure, sounds good.')

if __name__ == '__main__':
    unittest.main()
