from datetime import date
from pydantic import BaseModel, constr


class User(BaseModel):
    user_id: int | None = None
    username: str
    password: str
    email: str  # constr(pattern='^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$')
    first_name: str | None = None
    last_name: str | None = None
    is_admin: bool | None = None

    @classmethod
    def from_query(cls, user_id, username, password, email, first_name, last_name, is_admin):
        return cls(
            user_id=user_id,
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin
        )


class Topic(BaseModel):
    topic_id: int | None = None
    title: str
    user_id: int
    status: str = 'open'
    best_reply_id: int | None = None
    category_id: int

    @classmethod
    def from_query(cls, topic_id, title, user_id, status, best_reply_id, category_id):
        return cls(
            topic_id=topic_id,
            title=title,
            user_id=user_id,
            status='locked' if status == 1 else 'open',
            best_reply_id=best_reply_id,
            category_id=category_id
        )


class Message(BaseModel):
    message_id: int | None = None
    text: str
    sender_id: int
    receiver_id: int


class Category(BaseModel):
    category_id: int | None = None
    name: str
    is_locked: bool | None = None
    is_private: bool | None = None

    @classmethod
    def from_query(cls, category_id, name, is_locked, is_private):
        return cls(
            category_id=category_id,
            name=name,
            is_locked=is_locked,
            is_private=is_private,
        )


class Reply(BaseModel):
    reply_id: int | None = None
    text: str
    user_id: int
    topic_id: int

    @classmethod
    def from_query(cls, reply_id, text, user_id, topic_id):
        return cls(
            reply_id=reply_id,
            text=text,
            user_id=user_id,
            topic_id=topic_id
        )


class Vote(BaseModel):
    user_id: int
    reply_id: int
    type: bool

    @classmethod
    def from_query(cls, user_id, reply_id, type):
        return cls(
            user_id=user_id,
            reply_id=reply_id,
            type=type
        )


class TopicUpdate(BaseModel):
    title: str | None = None
    status: str | None = None
    best_reply_id: int | None = None


class LoginData(BaseModel):
    username: str
    password: str
