from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import request

from dbsetup import Categories, Items, Users

engine = create_engine('sqlite:///catalog.db')
DBsession = sessionmaker(bind = engine)
session = DBsession()

def getUserID(email):
	"""Checks if user's details are in the databse. If True, the user ID is returned;
	if not, nothing is returned"""
	try:
		user = session.query(Users).filter_by(email = email).one()
		return user.id
	except:
		return None

def createUser(login_session):
	"""takes the users google plus information from login_session, stores it in the database,
	and returns the users id from the databse"""
	newUser = Users(name = login_session['username'], email = login_session['email'], 
		picture = login_session['picture'])
	session.add(newUser)
	session.commit()
	return newUser.id