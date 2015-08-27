from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dbsetup import Categories, Items, Users

engine = create_engine('sqlite:///catalog.db')
DBsession = sessionmaker(bind = engine)
session = DBsession()

Mike = Users(name = "mike", email = "mikesmail@gmail.com")

Rugby = Categories(name = "rugby", userID = Mike.id)
session.add(Rugby)
session.commit()

RugbyBall = Items(name = "rugby ball", description = "an egg shaped ball used in rugby", categories_id = Rugby.id)
RugbyBoots = Items(name = "rugby boots", description = "spiked boots used in rugby to prevent slipping over in the mud",
	categories_id = Rugby.id)

session.add(RugbyBall)
session.add(RugbyBoots)
session.commit()

Skateboarding = Categories(name = "skateboarding", userID = Mike.id)
session.add(Skateboarding)
session.commit()

Deck = Items(name = "deck", description = "a plank of wood known as a 'skateboard deck'", categories_id = Skateboarding.id)
Trucks = Items(name = "trucks", description = "a piece of metal that connects the wheels to the deck", categories_id = Skateboarding.id)
Wheels = Items(name = "wheels", description = "enables the skateboard to be not useless", categories_id = Skateboarding.id)

session.add(Deck)
session.add(Trucks)
session.add(Wheels)
session.commit()

print "success!"
