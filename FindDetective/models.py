from sqlalchemy import Integer,Column,Text,create_engine,ForeignKey,desc,DateTime

from zope.sqlalchemy import ZopeTransactionExtension
from pyramid_sqlalchemy import BaseObject as Base,Session
from passlib.apps import custom_app_context as blogger_pwd_context
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__='Users'
    idUser=Column(Integer,primary_key=True)
    login=Column(Text)
    password=Column(Text)
    mail=Column(Text)
    def __repr__(self):
        return self.login+' '+str(self.idUser)

    def verify_password(self, password):
        if self.password == password:
            self.set_password(password)

        return blogger_pwd_context.verify(password, self.password)

    def set_password(self, password):
        password_hash = blogger_pwd_context.encrypt(password)
        self.password = password_hash

class Posts(Base):
    __tablename__='Posts'
    idPost=Column(Integer,primary_key=True)
    title=Column(Text)
    text=Column(Text)
    idUser=Column(Integer,ForeignKey('Users.idUser'))

    def __repr__(self):
        return self.title#+' '+str(self.idUser)


def get_posts():
    query = Session.query(Posts).all()
    return query


class Roles(Base):
    __tablename__='Roles'
    idRole=Column(Integer,primary_key=True)
    nameRole=Column(Text)
    description=Column(Text)

    def __repr__(self):
        return self.nameRole

class UsersRoles(Base):
    __tablename__="UserRoles"
    id=Column(Integer,primary_key=True)
    idUser=Column(Integer,ForeignKey('Users.idUser'))
    IdRole=Column(Integer,ForeignKey('Roles.idRole'))

    def __repr__(self):
        return str(self.idUser)+str(self.IdRole)

class Requests(Base):
    __tablename__='Requests'
    idRequest=Column(Integer,primary_key=True)
    title=Column(Text)
    description=Column(Text)
    phone=Column(Text)
    idUser=Column(Integer,ForeignKey('Users.idUser'))
    idPost=Column(Integer,ForeignKey('Posts.idPost'))

    def __repr__(self):
        return self.description
