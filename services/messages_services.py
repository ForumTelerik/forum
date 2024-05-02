from data.models import UserInfo, Message
from data.database import read_query, update_query, insert_query

#TODO edit msg

def create(message_text, sender_id, receiver_id):
    return insert_query(
        'INSERT INTO messages(text, sender_id, receiver_id) VALUES(?,?,?)',
        (message_text, sender_id, receiver_id))


def get_all_conversations(user_id: int):
    data = read_query('''SELECT DISTINCT u.username, u.email, u.first_name, u.last_name
               FROM users u
               JOIN messages m
               ON u.user_id = m.receiver_id
               WHERE m.sender_id = ?''', (user_id,))
    
    return [UserInfo.from_query(*row) for row in data]


def get_conversation(sender_id: int, receiver_id: int):
    data = read_query('''SELECT message_id, text, sender_id, receiver_id
                      FROM messages
                      WHERE sender_id=? AND receiver_id=?''', 
                      (sender_id, receiver_id))
    
    return [Message.from_query(*row) for row in data]
