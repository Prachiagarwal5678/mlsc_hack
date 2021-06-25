from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from Hackathon import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	company = db.Column(db.String(60), nullable=False)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s=Serializer(app.config['SECRET_KEY'])
		try:
			user_id=s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"

class ParkingLot(db.Model):
	id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
	level = db.Column(db.Integer, nullable=False)
	slot_no = db.Column(db.Integer, nullable=False)
	parked = db.Column(db.Boolean, nullable=False)
	in_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	out_time = db.Column(db.DateTime, nullable=True)
	company = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f"Post('{self.level}', '{self.slot_no}', '{self.in_time}')"