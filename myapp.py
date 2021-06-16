from flask import Flask, render_template, request, session, g, url_for, redirect
from sense_hat import SenseHat
from secrets import users_list
import random


s=SenseHat()

users=[]

users.append(users_list[0])
users.append(users_list[1])
users.append(users_list[2])


app = Flask(__name__)

app.secret_key = "secret_key"

@app.context_processor
def a_processor():
	def roundv(value,digits):
		return round(value,digits)
	return {'roundv':roundv}

@app.route('/logme', methods=['POST','GET'])
def logme():
	session.pop('user_id', None)
	if request.method=='POST':
		username=request.form['username']
		password=request.form['password']
		for user in users:
			if user[1] == username and user[2] == password :
				session['user_id']=user[0]
				return redirect(url_for('index_page'))
		print(request.form['username'])
	return render_template('login.html')

@app.route('/', methods=['POST','GET'])
def index_page():
	if not g.user:
		return redirect(url_for('logme'))
	return render_template('index.html')

@app.before_request
def before_request():
	g.user=None
	if 'user_id' in session:
		for user in users:
			if user[0] == session['user_id']:
				g.user = user
				g.s = s

@app.route('/sense', methods=['POST','GET'])
def sense_data():
	if not g.user:
		return redirect(url_for('logme'))
	if request.method=='POST':
		RED = int(request.form['red'])
		GREEN = int(request.form['green'])
		BLUE = int(request.form['blue'])
		s.clear(RED,GREEN,BLUE)
	return render_template('info.html')

@app.route('/ships', methods=['POST','GET'])
def ships():
	green=[0,200,0]
	black=[0,0,0]
	blue=[0,0,200]
	shipmap=[green]*10+[black]*54
	if not g.user:
		return redirect(url_for('logme'))
	if request.method=='POST':
		X = int(request.form['x'])
		Y = int(request.form['y'])
		if X > 7:
			s.clear(0,0,0)
			random.shuffle(shipmap)
			s.set_pixels(shipmap)
		else:
			s.set_pixel(X,Y,blue)
	return render_template('ships.html')

@app.route('/bonus_ships', methods=['POST','GET'])
def bonus_ships():
	green=[0,200,0]
	black=[0,0,0]
	blue=[0,0,200]
	shipmap=[green]*10+[black]*54
	colour_pixels = s.get_pixels()
	blue_pixels=colour_pixels.count([0,0,200])
	green_pixels = s.get_pixels().count(green)
	if not g.user:
		return redirect(url_for('logme'))
	if request.method=='POST':
		X = int(request.form['x'])
		Y = int(request.form['y'])

		if X>7:
			s.clear(0,0,0)
			random.shuffle(shipmap)
			s.set_pixels(shipmap)
		else:
			if s.get_pixel(X,Y) == green:
				s.set_pixel(X,Y,blue)

	return render_template('bonus_ships.html',blue_pixels=blue_pixels)

if __name__=='__main__':
	s.clear(0,0,0)
	app.run(debug=True, host='0.0.0.0')
