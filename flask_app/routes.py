# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context
from .utils.blockchain.database  import database
from .utils.blockchain.blockchain  import Blockchain
from .utils.blockchain.blockchain  import Block
from werkzeug.datastructures   import ImmutableMultiDict
from werkzeug.utils import secure_filename
from pprint import pprint
import json
import random
import os
import functools
import datetime
import cgitb; cgitb.enable()
db = database()


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = 'static/nft_images'
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#######################################################################################
# NFT RELATED
#######################################################################################
@app.route('/nft')
def nft():
	if 'email' in session:
		session['page'] = 'nft'
		return render_template('nft/nft.html')
	else:
		return render_template('login.html')

@app.route('/nft/buy')
def buy(error = ''):
	id = db.get_id_from_email(getUser())

	usertokens = db.query("SELECT * FROM wallet WHERE user_id=" + id)

	usernfts = db.query("SELECT * FROM nft WHERE user_id !=" + id)

	allnfts = db.query("SELECT * FROM nft")

	return render_template('nft/buy.html', user=getUser(), tokens = usertokens[0]['tokens'], usernfts=usernfts, error=error, allnfts=allnfts)

@app.route('/nft/sell')
def sell(error = ''):
	id = db.get_id_from_email(getUser())
	usernfts = db.query("SELECT * FROM nft WHERE user_id=" + id)

	return render_template('nft/sell.html', usernfts=usernfts, error = error, user=getUser())

@app.route('/nft/signup')
def signup(error=''):
	return render_template('nft/signup.html', user=getUser(), error=error)

@app.route('/nft/wallet')
def wallet():
	id = db.get_id_from_email(getUser())
	usernfts = db.query("SELECT * FROM wallet WHERE user_id=" + id)
	nfts = db.query("SELECT * FROM nft")
	return render_template('nft/wallet.html', tokens = usernfts[0]['tokens'], key = usernfts[0]['user_key'], user=getUser(), usernfts=nfts)


@app.route('/processsignup', methods = ['POST'])
def processsignup():
	print("PROCESSING Signup")
	feedback = request.form.to_dict()

	email = feedback['email']
	password = feedback['password']

	# Validating that there is input
	if len(email) == 0 or len(password) == 0:
		return render_template('nft/signup.html', error = 'One or both boxes do not have input!')

	# Validating user does not already exist
	if db.authenticate(email, password, signin=True):
		return signup('Email already taken!')


	print(email, password, "Sign up")

	db.createUser(email, password, 'guest')

	session['role'] = 'guest'

	return render_template('login.html', error = '')

@app.route('/processnft', methods = ['POST'])
def processnft():
	print("PROCESSING NFT")
	feedback = request.form.to_dict()

	# VALIDATING INPUT
	if feedback['token'] == '' or feedback['description'] == '':
		return sell('One or more boxes do not have input!')
	elif not feedback['token'].isdigit():
		return sell('Token amount must be numerical.')
	elif len(feedback['description']) > 100:
		return sell('Please keep descriptions 100 characters or less.')

	print("FEEDBACK:", feedback)

	f = request.files['filename']

	name = None
	if f.filename == '':
		name = str(random.randint(1, 21)) + '.png'	# CHANGE 4 TO AMOUNT OF IMAGES
	else:
		print("FILENAME:", f.filename)
		path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
		f.save(path)

		print("PATH: ")
		name = f.filename
	
	print("NAME:", name)
	print(os.path.join(app.instance_path, 'nft_images', secure_filename(f.filename)))
	
	id = db.get_id_from_email(getUser())

	db.insertRows('nft', ['user_id', 'name', 'description', 'token_amount'], [[id], [name], [feedback['description']], [feedback['token']]])

	print(db.query("SELECT * FROM nft"))
	last_id = db.query("SELECT nft_id FROM nft")[-1]['nft_id']
	print("LAST_ID = ", last_id)

	key = db.get_key_from_id(id)

	db.insertRows("blockchain", ["nft_id"], [[str(last_id)]])

	print("BLOCK:", db.query("SELECT * FROM blockchain"))

	return sell()

@app.route('/processedit', methods = ['POST'])
def processedit():
	form = request.form.to_dict()

	# VALIDATING INPUT
	if form['token_amount'] == '' or form['description'] == '':
		return sell('One or more boxes do not have input!')
	elif not form['token_amount'].isdigit():
		return sell('Token amount must be numerical.')
	elif len(form['description']) > 100:
		return sell('Please keep descriptions 100 characters or less.')
	
	# Making sure you own the NFT
	find_nft = db.query("SELECT user_id FROM nft WHERE nft_id = " + form['id'])


	if str(find_nft[0]['user_id']) != str(db.get_id_from_email(getUser())) or len(find_nft) == 0:
		return sell('You can only edit your own NFTs or existing ones!')

	for k, v in form.items():
		form[k] = '"' + v + '"'
	
	print("FORM:", form)

	print('UPDATE nft SET description = ' + 
		form['description'] + ', token_amount = ' + form['token_amount'] + ' WHERE nft_id = ' + form['id'])

	nft = db.query('UPDATE nft SET description = ' + 
		form['description'] + ', token_amount = ' + form['token_amount'] + ' WHERE nft_id = ' + form['id'])
	

	print("NFT:", nft)

	return sell()

@app.route('/processbuy', methods = ['POST'])
def processbuy():
	form = request.form.to_dict()


	if form['id'].isdigit() and int(form['id']) < 0:
		return buy("ID cannot be negative!")

	buyer_id = db.get_id_from_email(getUser())

	bc = Blockchain()

	# INPUT VALIDATION
	if form['id'] == '':
		return buy('Must enter an id to buy!')
	elif not form['id'].isdigit():
		return buy('ID must be numerical!')
	elif len(db.query("SELECT * FROM nft WHERE nft_id = " + form['id'])) == 0:
		return buy('That ID does not exist!')
	elif int(db.query("SELECT tokens FROM wallet WHERE user_id = " + db.get_id_from_email(getUser()))[0]['tokens']) < int(db.query("SELECT token_amount FROM nft WHERE nft_id = " + form['id'])[0]['token_amount']):
		return buy('You do not have enough tokens')
	elif str(db.query("SELECT user_id FROM nft WHERE nft_id = " + form['id'])[0]['user_id']) == str(db.get_id_from_email(getUser())):
		return buy('You already own that NFT!')
	
	seller_id = db.query("SELECT user_id FROM nft WHERE nft_id = " + form['id'])[0]['user_id']
	print("SELLERID:", seller_id)
	seller_tokens = db.query("SELECT tokens FROM wallet WHERE user_id = " + str(seller_id))[0]['tokens']

	if not bc.check_transaction_validity(buyer_id):
		return buy('You are not a valid user.')
	
	tokens = int(db.query("SELECT tokens FROM wallet WHERE user_id = " + db.get_id_from_email(getUser()))[0]['tokens'])
	cost = int(db.query("SELECT token_amount FROM nft WHERE nft_id = " + form['id'])[0]['token_amount'])
	# Update token amount for buyer
	db.query('UPDATE wallet SET tokens = ' + str(tokens-cost) + ' WHERE user_id = ' + buyer_id)
	# Update token amount for seller
	db.query('UPDATE wallet SET tokens = ' + str(seller_tokens+cost) + ' WHERE user_id = ' + str(seller_id))


	# Update ownership
	db.query("Update nft SET user_id = " + buyer_id + " WHERE nft_id = " + form['id'])

	print(db.query("SELECT * FROM blockchain"))

	blockchain_id = db.query("SELECT blockchain_id FROM blockchain WHERE nft_id = " + form['id'])[0]['blockchain_id']

	date = str(datetime.datetime.now())

	# GET EACH TRANSACTION FROM BLOCKCHAIN ID
	transactions = db.query("SELECT * FROM transactions WHERE blockchain_id = " + str(blockchain_id))

	print(transactions)

	# RE CREATING BLOCKCHAIN
	"""
	for t in transactions:
		prev_hash = db.query("SELECT hashes FROM hash WHERE transaction_id = " + t['transaction_id'])
		if len(prev_hash) == 0:
			prev_hash = 0
		else:
			prev_hash = prev_hash[-1]['hashes']
		b = Block(t['date'], [t['cost'], t['seller_id'], t['buyer_id']], prev_hash, 0)

		bc.append_block(b)
	"""

	# Add to transactions
	db.insertRows("transactions", ["blockchain_id", "cost", "sellerID", "buyerID", "date"], [[str(blockchain_id)], [str(cost)], [str(seller_id)], [buyer_id], [date]])

	# GET PREVIOUS HASH
	transaction_id = db.query("SELECT transaction_id FROM transactions WHERE blockchain_id = " + str(blockchain_id))[0]['transaction_id']
	hashes = db.query("SELECT hashes FROM hash WHERE transaction_id = " + str(transaction_id))

	if len(hashes) == 0:
		hashes = 0
	else:
		hashes = hashes[-1]['hashes']

	new_block = Block(date, [cost, seller_id, buyer_id], hashes, 0)

	curr_hash = bc.mine_transaction(new_block)

	db.insertRows("hash", ["hashes", "transaction_id"], [[curr_hash], [str(transaction_id)]])
	
	
	return buy()

@app.route("/processhistory", methods = ['POST'])
def processhistory():
	form = request.form.to_dict()

	if int(form['id']) < 0:
		return buy("ID cannot be negative!")
	elif not form['id'].isdigit():
		return buy('ID must be numerical!')
	elif len(db.query("SELECT * FROM nft WHERE nft_id = " + form['id'])) == 0:
		return buy('That ID does not exist!')

	id = form['id']

	nft = db.query("SELECT user_id FROM nft WHERE nft_id = " + form['id'])[0]['user_id']

	print(db.query("SELECT * FROM blockchain"))
	bc_id = db.query("SELECT blockchain_id FROM blockchain WHERE nft_id = " + id)[0]['blockchain_id']

	transactions = db.query("SELECT * FROM transactions WHERE blockchain_id = " + str(bc_id))

	
	return render_template("nft/history.html", transactions=transactions, id=id, userid=nft)


#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def getUser():
	return db.reversibleEncrypt('decrypt', session['email']) if 'email' in session else 'Unknown'

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/logout')
def logout():
	session['page'] = 'logout'
	session.pop('email', default=None)
	return redirect('/home')

@app.route('/processlogin', methods = ["POST","GET"])
def processlogin():
	
	form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))

	print("Form:", form_fields)


	if db.authenticate(form_fields['email'], form_fields['password']):
		session['email'] = db.reversibleEncrypt('encrypt', form_fields['email']) 

		if form_fields['email'] == 'owner@email.com' or form_fields['email'] == "dagost37@msu.edu":
			session['role'] = 'owner'
		else:
			session['role'] = 'guest'

		if session['page'] != 'nft':
			return json.dumps({"success": 0})
		else:
			return json.dumps({"success": 1})

	return json.dumps({"success": 2})


#######################################################################################
# OTHER
#######################################################################################
@app.route('/')
def root():
    print("THING:", __file__)
    return render_template("index.html")

@app.route('/personal-projects')
def personal():
    return render_template('personal_projects.html')

@app.route('/school-projects')
def school():
    return render_template('school_projects.html')

@app.route('/home')
def home():
	session['page'] = 'home'
	x     = random.choice(['I was born in Seattle!','I am a huge Mac Miller fan','I disc golf frequently', 'I\'m (embarrassingly) Grandmaster in Overwatch 2', 'I collect coins :)'])
	return render_template('home.html', fun_fact = x)

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

@app.route('/resume')
def resume():
	session['page'] = 'resume'
	resume_data = db.getResumeData()
	pprint(resume_data)
	return render_template('resume.html', resume_data = resume_data)

@app.route('/projects')
def projectpage():
	session['page'] = 'projects'
	return render_template('projects.html')

@app.route('/piano')
def pianopage():
	session['page'] = 'piano'
	return render_template('piano.html')

@app.route('/processfeedback', methods = ['POST'])
def processfeedback():
	session['page'] = 'processfeedback'
	print("PROCESSING FEEDBACK")
	feedback = request.form.to_dict()

	name = feedback['name']
	email = feedback['email']
	comment = feedback['typedfeedback']

	# Prevents a "data too long" error
	if len(comment) > 1000:
		comment = comment[:999]

	db.insertRows('feedback', ['name', 'email', 'comment'], [[name], [email], [comment]])

	feedbackdata = db.query("SELECT * FROM feedback")

	namefeed = []

	# Makes a list with [name, comment] to be formatted in processfeedback.html
	for item in feedbackdata:
		x = []
		for k, v in item.items():
			if k == 'name' or k == 'comment':
				x.append(v)
		namefeed.append(x)
	
	print(namefeed)

	return render_template('processfeedback.html', feed = namefeed)
