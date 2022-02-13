from sqlalchemy import Column, Integer, String, create_engine, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = 'Users'

    id = Column(String, primary_key=True)
    user_name = Column(String)
    email_id = Column(String)
    password = Column(String)
    Gender = Column(String)
    date_of_birth = Column(DateTime)
    sender_relation = relationship("ChatHistory")
    groups_relation = relationship("Groups")


class ChatHistory(Base):
    __tablename__ = 'ChatHistory'

    id = Column(String, primary_key=True)
    sender = Column(String, ForeignKey('Users.id'))
    message = Column(String)
    receiver = Column(String)


class Groups(Base):
    __tablename__ = 'ChatGroup'

    id = Column(String, primary_key=True)
    group_name = Column(String)
    group_create_date = Column(DateTime)
    group_founder = Column(String, ForeignKey('Users.id'))
    password = Column(String)


class GroupMembers(Base):
    __tablename__ = 'GroupMembers'

    id = Column(String, primary_key=True)
    group_id = Column(String, ForeignKey('ChatGroup.id'))
    group_member = Column(String, ForeignKey('Users.id'))
    group_role = Column(String)


if __name__ == '__main__':
    engine = create_engine('sqlite:///open-chat.sqlite', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
