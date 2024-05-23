from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy import select, delete


from connect_database import engine

if not database_exists(engine.url): create_database(engine.url)

class Base(DeclarativeBase):
    ...

class Chats(Base):
    __tablename__ = "Chats_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_name = Column(String(25), nullable=False)
    chat_messages = Column(JSON, nullable=False)
    

def update_in_database(chat_name: str, chat_messages: dict):
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        result = session.scalar(select(Chats).where(Chats.chat_name == chat_name))

        if result:
            result.chat_messages = chat_messages
            session.commit()
        else:
            session.add(
                Chats(
                    chat_name=chat_name,
                    chat_messages=chat_messages
                )
            )
            session.commit()
            
            
def delete_in_database(chat_name: str):
    with Session(engine) as session:
        session.execute(delete(Chats).where(Chats.chat_name == chat_name))
        session.commit()

def get_history():
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        result = session.scalars(select(Chats))
        obs = result.fetchall()
        return obs