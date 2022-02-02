from sqlalchemy import Column, Integer, String, create_engine, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Users(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String)
    email_id = Column(String)
    password = Column(String)
    Gender = Column(String)
    date_of_birth = Column(DateTime)


if __name__ == '__main__':
    engine = create_engine('sqlite:///database.sqlite', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
