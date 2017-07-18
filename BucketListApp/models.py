from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
 
db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'tbl_user'
  user_id = db.Column(db.Integer, primary_key = True)
  user_name = db.Column(db.String(45))
  user_email = db.Column(db.String(45), unique=True)
  user_password = db.Column(db.String(255))
   
  def __init__(self, name, email, password):
    self.user_name = name.title()
    self.user_email = email.lower()
    self.set_password(password)
     
  def set_password(self, password):
    self.user_password = generate_password_hash(password)
   
  def check_password(self, password):
    return check_password_hash(self.user_password, password)