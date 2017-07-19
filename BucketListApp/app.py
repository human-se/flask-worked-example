from flask import Flask, render_template, request, json, session
from models import *
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://your-username:your-password@localhost/BucketList'
db.init_app(app)

@app.route("/")
def main():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
	if not session.get('logged_in'):
		return render_template('signup.html')
	else:
		return render_template('index.html')

@app.route('/signUp',methods=['POST'])
def signUp():
	# read the posted values from the UI
	_name = request.form['inputName']
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']
 
	# validate the received values
	if _name and _email and _password:
		user = User.query.filter_by(user_email = _email.lower()).first()
		if not user:
			db.session.add(User(_name,_email,_password))
			try:
				db.session.commit()
				session['logged_in'] = True
				return json.dumps({'html':'<span>User added</span>'})
			except Exception as e:
				db.session.rollback()
				db.session.flush()
				return json.dumps({'html':'<span>' + e + '</span>'})
		return json.dumps({'html':'<span>Email not unique</span>'})
	else:
		return json.dumps({'html':'<span>Missing fields</span>'})

@app.route('/showLogin')
def showLogin():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']

	if _email and _password:
		query = db.session.query(User).filter(User.user_email.in_([_email]))
		result = query.first()

	if not result:
		return json.dumps({'html':'<span>Email not found</span>'})
	if result.check_password(_password):
		session['logged_in'] = True
		return json.dumps({'html':'<span>Logged in</span>'})
	else:
		return json.dumps({'html':'<span>Password not correct</span>'})

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run()