from flask import render_template, url_for, flash, redirect, request, abort
from Hackathon import app, bcrypt, db, mail
from Hackathon.forms import RegisterationForm, LoginForm, RequestResetForm, ResetPasswordForm, AddSlotForm, SelectSlotForm
from wtforms.validators import ValidationError
from Hackathon.models import User, ParkingLot
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route("/home")
@app.route("/")
def home():
	return render_template('index.html')

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route("/booking", methods=['GET', 'POST'])
@login_required
def booking():
	form = SelectSlotForm()
	if form.validate_on_submit():
		parkinglot = ParkingLot.query.filter_by(parked=0).order_by(ParkingLot.level).order_by(ParkingLot.slot_no).first()
		print("Parking Level: ", parkinglot.level)
		print("Slot Number  : ", parkinglot.slot_no)
		# return render_template('booking.html', parkinglot=parkinglot)
	parkinglotA = ParkingLot.query.filter_by(level=1).all()
	parkinglotB = ParkingLot.query.filter_by(level=2).all()
	parkinglotC = ParkingLot.query.filter_by(level=3).all()
	parkinglotD = ParkingLot.query.filter_by(level=4).all()
	parkinglotE = ParkingLot.query.filter_by(level=5).all()
	return render_template('booking.html', parkinglotA=parkinglotA, parkinglotB=parkinglotB, parkinglotC=parkinglotC, parkinglotD=parkinglotD, parkinglotE=parkinglotE, form=form)

@app.route("/addslot", methods=['GET', 'POST'])
@login_required
def addslot():
	form = AddSlotForm()
	if form.validate_on_submit():
		parkinglot = ParkingLot(level=form.level.data, slot_no=form.slot_no.data, parked=form.parked.data, company=form.company.data)
		db.session.add(parkinglot)
		db.session.commit()
		return redirect(url_for('addslot'))
	return render_template('addslot.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('booking'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user)
			return redirect(url_for('booking'))
	return render_template('login.html', form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegisterationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(email=form.email.data, password=hashed_password, company=form.company.data)
		db.session.add(user)
		db.session.commit()
		flash('Your Account Has Been Successfully Created. Now you can Log In', 'success')
		return redirect(url_for('login'))
	return render_template('signup.html', form=form)
