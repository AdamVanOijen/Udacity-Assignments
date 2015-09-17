from flask import Flask, render_template, url_for, redirect, request, flash, make_response, jsonify, g
from flask import session as login_session

from sqlalchemy import create_engine, desc
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker

from dbsetup import Categories, Items, Users
from DBHelpers import getUserID, createUser

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from functools import wraps
import random, string
import json
import httplib2
import requests

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')

DBsession = sessionmaker(bind = engine)
session = DBsession()

CLIENT_ID = json.loads(
	open('client_secrets.json', 'r').read())['web']['client_id']

def login_required(f):
	@wraps(f)#copies arguments list, name, docstring from f to wrapper
	def wrapper(*args, **kwargs):
		try:
			login_session['username']
			if len(kwargs) > 0:
				categoriesUserID = session.query(Categories.userID).filter_by(id = kwargs['id']).one()
				if login_session['user_id'] != categoriesUserID[0]:
					return "you are not authorized to view this page; you must be the creator of the category to make changes"
		except:
			return "you must signed in to view this page"
		return f(*args, **kwargs)
	return wrapper

@app.route('/')
def home():
	"""returns home page"""
	newItems = session.query(Items).order_by(desc(Items.time)).limit(10)
	categories = session.query(Categories)
	return render_template('home.html', newItems = newItems, categories = categories, login_session = login_session)

@app.route('/login')
def login():
	"""returns the page for signing in to googls plus, and a state key that is unique to
	every visit to this page."""
	#generates a random, 32 character long, string each time someone visits the login page.
	state = "".join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	#stores the random string in to the login_session dictionary. session is a dictionary that 
	#strores users information, and keeps track of which information belongs to which user by 
	#checking the user's cookies.
	login_session['state'] = state
	return render_template('login.html', STATE = state)

@app.route('/categories/id/<int:id>/edit', methods = ['GET', 'POST'])
@login_required
def editCategory(id):
	"""returns the page for editing a category. Only users who created the category can edit it,
	this is ensured by checking that the user ID in the login_session object mathces the user ID
	stored with the category in the databse. Items of the category are created, deleted and edited 
	with forms."""
	if request.method == 'POST':
		if request.args.get('itemid'):
			itemID = request.args.get('itemid')
			ItemToEdit = session.query(Items).filter_by(id = itemID).one()
			if ItemToEdit.categories_id == id:
				if request.form['name'] != '':
					name = request.form['name']
					ItemToEdit.name=name
					session.add(ItemToEdit)
					session.commit()
			
				if request.form['description']!= '':
					description = request.form['description']
					ItemToEdit.description=description
					session.add(ItemToEdit)
					session.commit()

				return redirect(url_for('home'))
			else:
				return "the itemID specified, does not correspond to the category specified."
		else: 
			newItem = Items(name = request.form['name'], description = request.form['description'], categories_id= id)
			session.add(newItem)
			session.commit()
			return redirect(url_for('home'))

	if request.method =='GET':
		items = session.query(Items).filter_by(categories_id = id).all()
		return render_template('editCategory.html', items = items, cat_id = id)


@app.route('/categories/id/<int:id>')
def category(id):
	""" retrieves all items from the databse belonging to the given category, and returns a 
	page displaying them"""
	items = session.query(Items).filter_by( categories_id = id ).all()
	categoryName = session.query(Categories.name).filter_by(id = id).one()
	return render_template("Category.html", items = items, categoryName = categoryName[0])

@app.route('/categories/new', methods = ['GET', 'POST'])
@login_required
def addCategory():
	"""returns a page for the user to create a new category if they are signed in. This is 
	ensured by checking that there is a user_id in the user's login_session"""
	login_session['user_id']
	if request.method == 'GET':
		return render_template('addCategory.html')

	if request.method == 'POST':
		categoryName = request.form['name']
		newCategory = Categories(name = categoryName, userID = login_session['user_id'])
		session.add(newCategory)
		session.commit()
		return redirect(url_for('home'))

@app.route('/categories/id/<int:id>/delete', methods = ['GET', 'POST'])
@login_required
def deleteCategory(id):
	if request.method == 'POST':
		CategoryToDelete = session.query(Categories).filter_by(id = id).one()
		session.delete(CategoryToDelete)
		session.commit()
		return redirect(url_for('home'))
	if request.method == 'GET':
		return render_template('deleteCategory.html', id = id)

@app.route('/categories/id/<int:id>/item/id/<int:Itemid>/delete', methods = ['GET','POST'])
@login_required
def deleteItem(id, Itemid):
	"""Returns a page for the user to confirm that they want to delete the chosen item ."""
	ItemToDelete = session.query(Items).filter_by(id = Itemid).one()
	if request.method == 'POST':
		session.delete(ItemToDelete)
		session.commit()
		return redirect(url_for('home'))
	else:
		return render_template('deleteItem.html', ItemToDelete = ItemToDelete, id = id)

@app.route('/gconnect', methods=['POST'])
def gconnect():
	"""After the user agrees to allow the application offline access to their google plus information,
	the user's state key is verified, and an authorization key is sent to the application to be 
	exchanged for an access token through google's oauth2 api. Once the application has recieved an
	access token, the gconnect function checks to see if the access token is valid, and goes on to request
	the user's google plus information and store it in the login_session object. After all this is completed,
	the user is redirectied to the home page."""
	print request.args.get('state')
	if request.args.get('state') != login_session['state']:
		return "invalid state token"

	auth_key = request.data

 	try:
		#contains the projects oauth client ID and client secret which the oauth2
		#api needs to authenticate before upgrading the auth_key to an
		#access token
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		#attempting to upgrade auth_code for an access token
		credentials = oauth_flow.step2_exchange(auth_key)
	except FlowExchangeError:
		return 'failed to upgrade auth code'

	access_token = credentials.access_token

	# Check that the access token is valid.
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'% access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])
	# If there was an error in the access token info, abort.
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'

	# Verify that the access token is used for the intended user.
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is valid for this app.
	if result['issued_to'] != CLIENT_ID:
		response = make_response(json.dumps("Token's client ID does not match app's."), 401)
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response

	stored_credentials = login_session.get('credentials')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'),200)
		response.headers['Content-Type'] = 'application/json'
		return response

	login_session['credentials'] = credentials.access_token
	login_session['gplus_id'] = gplus_id

	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()
	
	#storing the user's google plus information in to the login_session object.
	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']
    
	user_id = getUserID(login_session['email'])
	#if the user has not registered with the application, their details are automatically stored in the
	#database.
	if not user_id:
		user_id = createUser(login_session)
		flash("user registered!")

	login_session['user_id'] = user_id
	print "this is the userID" + str(login_session['user_id'])

	output = ''
	output += '<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	output += '<img src="'
	output += login_session['picture']
	output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
	flash("you are now logged in as %s" % login_session['username'])
	print "done!"
	return output

@app.route('/json')
def jsonData():
	"""returns all category and item information from the databse, in JSON format."""
	CategoriesObjects = session.query(Categories).all()
	ItemsObjects = session.query(Items).all()
	CategoriesList = []
	ItemsList = []

	for c_index  in CategoriesObjects: 
		CategoriesList.append(c_index.serialize)

	for i_index in ItemsObjects:
		ItemsList.append(i_index.serialize)

	return jsonify( categories = CategoriesList, items = ItemsList)

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)