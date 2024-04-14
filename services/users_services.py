from data.models import User
from data.database import read_query, update_query, insert_query
from helpers import helpers


def get_all():
    data = read_query(
        '''SELECT user_id, username, email, first_name, last_name, is_admin
        FROM users''')

    users = [User.from_query(*row) for row in data]
    return users


def get_by_id(id):
    data = read_query(
        '''SELECT user_id, username, email, first_name, last_name, is_admin
        FROM users WHERE user_id = ?''', (id,))

    user = [User.from_query(*row) for row in data][0]
    return user


def register(user: User):
    """
    Creates user without is_admin
    Handles unique columns violations with try/except in queries
    """
    data = insert_query(
        'INSERT INTO users(username,email,first_name,last_name) VALUES(?,?,?,?)',
        (user.username, user.email, user.first_name, user.last_name)
    )
    if not isinstance(data, int):
        error_msg = helpers.humanize_error_msg(data)
        return error_msg, 400

    generated_id = data
    return f'User {generated_id} was successfully created!', 200


def update(old: User, new: User):
    """
    Merges new user with old, changing is_admin attribute only if request is from admin
    Handles unique columns violations with try/except in queries
    """
    request_sent_from_admin = True  # no authorization logic yet

    new_admin_status = old.is_admin
    if request_sent_from_admin and new.is_admin:
        new_admin_status = new.is_admin

    merged = User(
        user_id=old.user_id,
        username=new.username or old.username,
        email=new.email or old.email,
        first_name=new.first_name or old.first_name,
        last_name=new.last_name or old.last_name,
        is_admin=new_admin_status
    )
    data = update_query(
        'UPDATE users SET username = ?, email = ?, first_name = ?, last_name = ?, is_admin = ? WHERE user_id = ?',
        (merged.username, merged.email, merged.first_name, merged.last_name, merged.is_admin, merged.user_id)
    )

    if data is not True:
        error_msg = helpers.humanize_error_msg(data)
        return error_msg, 400

    return merged, 200
