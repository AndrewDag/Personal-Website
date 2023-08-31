# Author: Prof. MM Ghassemi <ghassem3@msu.edu>

#--------------------------------------------------
# Import Requirements
#--------------------------------------------------
import os
from flask import Flask

#--------------------------------------------------
# Create a Failsafe Web Application
#--------------------------------------------------
def create_app(debug=False):
	app = Flask(__name__)

	# NEW IN HOMEWORK 3 ----------------------------
	# This will prevent issues with cached static files
	app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
	app.debug = debug
	# The secret key is used to cryptographically-sign the cookies used for storing the session data.
	app.secret_key = 'AKWNF1231082fksejfOSEHFOISEHF24142124124124124iesfhsoijsopdjf'
	# ----------------------------------------------
	os.makedirs(os.path.join(app.instance_path, 'nft_images'), exist_ok=True)

	from .utils.blockchain.database import database
	db = database()
	db.createTables(purge=True)
	
	# NEW IN HOMEWORK 3 ----------------------------
	# This will create a user
	db.createUser(email='owner@email.com' ,password='password', role='owner')
	db.createUser(email='guest@email.com' ,password='password', role='guest')
	db.createUser(email="dagost37@msu.edu", password="tester", role='owner')
	db.createUser(email="test", password="test", role='guest')
	# ----------------------------------------------

	with app.app_context():
		from . import routes
		return app