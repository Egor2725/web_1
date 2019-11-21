
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from database import db_session, Base
from app import login




class User(UserMixin, Base):        #сама БД  
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, index=True, unique=True)
    password_hash = Column(String)

    def __init__(self, username=None, email=None, password_hash=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):       #хеширование пароля
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):     #проверка пароля
        return check_password_hash(self.password_hash, password)

# @login.user_loader
# def loader_user(id):
#     return User.query.get(int(id))

    



def create_user(username, email, password):     #алгоритм регистрации пользователя и внесение его в БД
    password_hash = generate_password_hash(password)
    # test_user = None
    test_user = User(username = username, email = email, password_hash = password_hash )
    # db_session = sessionmaker(bind=engine)()
    db_session.add(test_user)
    db_session.commit()

# username = input()
# email = input()
# password = input()
# create_user(username, email, password)

User.query.all()