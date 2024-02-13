import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, declarative_base, backref
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

follower_table = Table(
    "followers",
    Base.metadata, 
    Column("user_from_id", Integer, ForeignKey('users.id'), nullable=False, primary_key=True),   
    Column("user_to_id", Integer, ForeignKey('users.id'), nullable=False, primary_key=True)
)

class User(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    username = Column(String(200), unique = True, nullable = False)
    firstname = Column(String(200))
    lastname = Column(String(200))
    email = Column(String(200), unique= True)
    posters =  relationship('Post', backref="user")
    comments =relationship('Comment', backref="user")

    followers = relationship(
        "User", 
        secondary= follower_table, 
        primaryjoin= (follower_table.c.user_from_id == id), 
        secondaryjoin= (follower_table.c.user_to_id == id),  
        backref= backref("followeds", lazy="dynamic") 
    )

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key = True)
    users_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    comments = relationship('Comment', backref = 'post')
    medias = relationship('Media', backref = 'post')

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key = True)
    comment_text = Column(String(500))
    auth_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable = False)

class Media(Base):
    __tablename__ = 'medias'
    id = Column(Integer, primary_key = True)
    type = Column(String(300))
    url = Column(String(300))
    post_id = Column(Integer, ForeignKey('posts.id'), nullable = False
    )
    
## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
    

