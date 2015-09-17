from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Users(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key =True)
	name = Column(String, nullable =False)
	email = Column(String, nullable = False)
	picture = Column(String, nullable = True)
	categories = relationship("Categories")
	@property
	def serialize(self):
		return {
		'id':self.id,
		'name':self.name,
		'email':self.email
		}

class Categories(Base):
	__tablename__ = "categories"

	id = Column(Integer, primary_key = True)
	name = Column(String, nullable = False)
	userID = Column(Integer, ForeignKey('users.id'))
	items = relationship("Items", cascade = "delete, delete-orphan", single_parent=True)

	@property
	def serialize(self):
	    return{
	    	'id':self.id,
	    	'name':self.name,
	    	'userID': self.userID
	    }


class Items(Base):
	__tablename__ = "items"

	id = Column(Integer, primary_key = True)
	name = Column(String, nullable = False)
	description = Column(String, nullable = False)
	time = Column(DateTime)
	categories_id = Column(Integer, ForeignKey('categories.id'))

	@property
	def serialize(self):
	    return{
	    	'id': self.id,
	    	'name': self.name,
	    	'description': self.description,
	    	'time': str(self.time),
	    	'categories_id': self.categories_id
	    }

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)