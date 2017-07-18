from flask import Flask, render_template, request, json
from models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://your-username:your-password@localhost/BucketList'
db.init_app(app)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
 
    # validate the received values
    if _name and _email and _password:
        return json.dumps({'html':'<span>All fields entered</span>'})
    else:
        return json.dumps({'html':'<span>Missing fields</span>'})

if __name__ == "__main__":
    app.run()