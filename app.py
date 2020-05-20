from flask import Flask, render_template, flash, redirect,session, request, url_for, session, logging
#Simulation des données d'un trajet fichier txt
# from data import Trajets
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import json

app = Flask(__name__)
app.debug = True 

#Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'tuto'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MySQL
mysql=MySQL(app)

#simulation d'un trajet fichier txt 
# Trajets = Trajets()

@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/infos')
def infos():
	return render_template('infos.html')
	
@app.route('/a_propos')
def airo():
	return render_template('airo.html')


class RegisterForm(Form):
	name = StringField(u'Nom', [validators.length(min=5, max=50)])
	username = StringField(u'Nom d\'utilisateur', [validators.length(min=5, max=25)])
	email = StringField(u'e-mail', [validators.length(min=10, max=100)])
	password = PasswordField(u'Mot de passe', [validators.length(min=5, max=100), validators.DataRequired(), validators.EqualTo('confirm', message='Mot de passe différent')])
	confirm = PasswordField(u'Confirmation du mot de passe')

#User registration
@app.route('/users', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str((form.password.data)))

		#create cursor
		cur = mysql.connection.cursor()

		cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

		#Appliquer les modif à la base
		mysql.connection.commit()

		#close connection
		cur.close()

		flash('Vous vous êtes bien enregistré et vous pouvez maintenant vous connecter', 'success')
		return redirect(url_for('login'))

	return render_template('users.html', form=form)

#User login
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST' :
		#Get for fields
		username = request.form['username']
		password_candidate = request.form['password']

		#create cursor for DB
		cur = mysql.connection.cursor()

		#Get user by username
		result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

		if result > 0:
			#Store the pwd hash for current username
			data = cur.fetchone()
			password = data['password']

			#Compare passpassaword's hash
			if sha256_crypt.verify(password_candidate,password):
				#Session variables
				session['logged_in'] = True
				session['username'] = username

				flash('Connexion réussie', 'success')
				app.logger.info('PASSWORD MATCHED')
				return redirect(url_for('dashboard'))
			else:
				error = 'Mot de passe incorrect'
				return render_template('login.html', error=error)
				app.logger.info('PASSWORD NOT MATCHED')
			cur.close()
		else:
			error = 'Utilisateur inexistant'
			return render_template('login.html', error=error)
			app.logger.info('UTILISATEUR INEXISTANT')

	return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Vous devez d\'abord vous connecter', 'danger')
            return redirect(url_for('login'))
    return wrap

def listToJsonString(l):
	res = '{"coords": ['
	for cur in l:
		res += (cur.replace('\'', '\"')+",")
	res += ']}'
	print(res)
	return res
#Creating a route to access the dashboard.html page
@app.route('/dashboard')

#Controling access rights with the 'is_logged_in' function coded above
@is_logged_in
def dashboard():
	#create cursor to access database
	cur = mysql.connection.cursor()
	#Get last data from capteur1;
	res = cur.execute("SELECT value10, value25, date, time FROM capteur1 ORDER BY id DESC LIMIT 1;")
	capteur1 = cur.fetchone()

	#Get last trajet for current user
	res1 = cur.execute("SELECT * FROM trajets WHERE username=%s ORDER BY id DESC LIMIT 1;", [session['username']])
	last = cur.fetchone()

	#Get gps coordinates for the last trajet
	res2 = cur.execute("select lat, lng, time, date from gps having (time <= (select time_end from trajets where id=6)AND time >= (select time_beg from trajets where id=6));")
	coords = list(cur.fetchall())

	#Get all data corresponding to last trajet
	res3 = cur.execute("select value10, value25, time from capteur1 having (time <= (select time_end from trajets where id=6)AND time >= (select time_beg from trajets where id=6));")
	data = cur.fetchall()

	#Creating array to match the corresponding pollution data which will be shown on map
	colors = []
	for dat in data:
		if max(dat['value10'],dat['value25']) <= 6:
			colors.append("https://zupimages.net/up/20/18/1iqi.png")

		elif max(dat['value10'],dat['value25']) <= 13 and max(dat['value10'],dat['value25']) > 6:
			colors.append("https://zupimages.net/up/20/18/7vst.png")
			
		elif max(dat['value10'],dat['value25']) <= 20 and max(dat['value10'],dat['value25']) > 13:
			colors.append("https://zupimages.net/up/20/18/vwyq.png")
		
		elif max(dat['value10'],dat['value25']) <= 27 and max(dat['value10'],dat['value25']) > 20:
			colors.append("https://zupimages.net/up/20/18/6lqo.png")
		
		elif max(dat['value10'],dat['value25']) <= 34 and max(dat['value10'],dat['value25']) > 27:
			colors.append("https://zupimages.net/up/20/18/dx5w.png")
		
		elif max(dat['value10'],dat['value25']) <= 41 and max(dat['value10'],dat['value25']) > 34:
			colors.append("https://zupimages.net/up/20/18/niip.png")
		
		elif max(dat['value10'],dat['value25']) <= 49 and max(dat['value10'],dat['value25']) > 41:
			colors.append("https://zupimages.net/up/20/18/w4jt.png")
		
		elif max(dat['value10'],dat['value25']) <= 64 and max(dat['value10'],dat['value25']) > 49:
			colors.append("https://zupimages.net/up/20/18/go8q.png")
		
		elif max(dat['value10'],dat['value25']) <= 79 and max(dat['value10'],dat['value25']) > 67:
			colors.append("https://zupimages.net/up/20/18/go8q.png")
		
		elif max(dat['value10'],dat['value25']) >= 80:
			colors.append("https://zupimages.net/up/20/18/go8q.png")

	#Returns the length of the coords array
	length = len(coords)

	#Returns dashboard.html template with all the updated parameters
	if res > 0 or res1 > 0:
		return render_template('dashboard.html', capteur1=capteur1, last=last, coords=coords, length=length, colors=colors)
	else:
		msg = 'Pas de données à afficher'
		return render_template('dashboard.html', msg=msg, capteur1=capteur1, last=last, coord=coord, length= length)
	#Closing the MySQL cursor to end the database connexion
	cur.close()

@app.route('/api/coordinates')
def coordinates():
  cur = mysql.connection.cursor()
  res = cur.execute("select lat, lng, time from gps having (time <= (select time_end from trajets where id=6)AND time >= (select time_beg from trajets where id=6));")
  addresses = json.dumps(cur.fetchall(),indent=4, sort_keys=True, default=str)
  all_coods = [] # initialize a list to store your addresses

  for add in addresses:
     address_details = {
     "lat": add.lat, 
     "lng": add.lng, 
     "title": add.title}
     all_coods.append(address_details)
  return jsonify({'cordinates': all_coods})
  cur.close()

	
@app.route('/indice_atmo')
@is_logged_in
def atmo():
	return render_template('atmo.html')

@app.route('/mes_trajets')
@is_logged_in
def trajets():
	#create cursor
	cur= mysql.connection.cursor()
	#Get all trajets from db
	res = cur.execute("SELECT * FROM trajets;")
	trajets = cur.fetchall()

	if res > 0:
		return render_template('trajets.html', trajets=trajets)
	else:
		msg = 'Pas de trajets enregistrés'
		return render_template('trajets.html', msg=msg)
	
	cur.close()
	#simulation
	#return render_template('trajets.html', trajets = Trajets)
	
@app.route('/trajet/<string:id>')
@is_logged_in
def trajet(id):
	#create cursor
	cur= mysql.connection.cursor()

	res1 = cur.execute("SELECT * FROM trajets;")
	trajets = cur.fetchall()

	res = cur.execute("SELECT * FROM trajets where id= %s;", [id])
	trajet = cur.fetchone()

	res2 = cur.execute("select lat, lng, time from gps having (time <= (select time_end from trajets where id=%s)AND time >= (select time_beg from trajets where id=%s));", ([id], [id]))
	coords = list(cur.fetchall())

	res3 = cur.execute("select value10, value25, time from capteur1 having (time <= (select time_end from trajets where id=%s)AND time >= (select time_beg from trajets where id=%s));", ([id], [id]))
	data = cur.fetchall()

	colors = []
	
	for dat in data:
		if max(dat['value10'],dat['value25']) <= 6:
			colors.append("https://zupimages.net/up/20/18/1iqi.png")

		elif max(dat['value10'],dat['value25']) <= 13 and max(dat['value10'],dat['value25']) > 6:
			colors.append("https://zupimages.net/up/20/18/7vst.png")
			
		elif max(dat['value10'],dat['value25']) <= 20 and max(dat['value10'],dat['value25']) > 13:
			colors.append("https://zupimages.net/up/20/18/vwyq.png")
		
		elif max(dat['value10'],dat['value25']) <= 27 and max(dat['value10'],dat['value25']) > 20:
			colors.append("https://zupimages.net/up/20/18/6lqo.png")
		
		elif max(dat['value10'],dat['value25']) <= 34 and max(dat['value10'],dat['value25']) > 27:
			colors.append("https://zupimages.net/up/20/18/dx5w.png")
		
		elif max(dat['value10'],dat['value25']) <= 41 and max(dat['value10'],dat['value25']) > 34:
			colors.append("https://zupimages.net/up/20/18/niip.png")
		
		elif max(dat['value10'],dat['value25']) <= 49 and max(dat['value10'],dat['value25']) > 41:
			colors.append("https://zupimages.net/up/20/18/w4jt.png")
		
		elif max(dat['value10'],dat['value25']) <= 64 and max(dat['value10'],dat['value25']) > 49:
			colors.append("https://zupimages.net/up/20/18/go8q.png")
		
		elif max(dat['value10'],dat['value25']) <= 79 and max(dat['value10'],dat['value25']) > 67:
			colors.append("https://zupimages.net/up/20/18/go8q.png")
		
		elif max(dat['value10'],dat['value25']) >= 80:
			colors.append("https://zupimages.net/up/20/18/go8q.png")
		
		


	if res > 0:
		return render_template('trajet.html', trajets=trajets, id=id, trajet=trajet, coords=coords, data=data, colors= colors)
	else:
		msg = 'Pas de trajets enregistrés'
		return render_template('trajets.html', msg=msg)
	
	cur.close()
	#Simulation
	# return render_template('trajet.html', id=id, trajets = Trajets)

#User logout
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('Vous vous êtes bien déconnecté', 'success')
	return redirect(url_for('login'))

class TrajetForm(Form):
	name = StringField(u'Nom du trajet', [validators.length(min=5, max=50)])

@app.route('/add_trajet', methods=['GET', 'POST'])
@is_logged_in
def add_trajet():
	form = TrajetForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data

		#create cursor
		cur = mysql.connection.cursor()

		#execute
		cur.execute("INSERT INTO trajets(name, username) VALUES(%s, %s)", (name, session['username']))

		#commit
		mysql.connection.commit()

		cur.close()

		flash('Trajet ajouté', 'success')

		return redirect(url_for('trajets'))

	return render_template('add_trajet.html', form=form)

#Editer un trajet
@app.route('/edit_trajet/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_trajet(id):
	#check username 
	#Create cursor
	cur = mysql.connection.cursor()
	#get trajet by id
	res = cur.execute("SELECT * FROM trajets WHERE id=%s", [id])
	user = cur.fetchone()
	cur.close()
	if session['username'] == user['username']:
		#Create cursor
		cur = mysql.connection.cursor()
		#get trajet by id
		res = cur.execute("SELECT * FROM trajets WHERE id=%s", [id])
		trajet = cur.fetchone()
		cur.close()

		#Get new parameters in form
		form = TrajetForm(request.form)
		#new parameters for the trajet
		form.name.data = trajet['name']

		#apply new parameters to DB
		if request.method == 'POST' and form.validate():
			name = request.form['name']

			#create cursor
			cur = mysql.connection.cursor()

			#execute
			cur.execute("UPDATE trajets SET name=%s WHERE id=%s", (name, id))

			#commit
			mysql.connection.commit()

			flash('Trajet mis à jour', 'success')

			cur.close()

			return redirect(url_for('trajets'))

		return render_template('edit_trajet.html', form=form)
	else:
		flash('Ce trajet ne vous appartient pas', 'danger')
		
		return redirect(url_for('trajets'))

#Supprimer un trajet
@app.route('/delete_trajet/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def delete_trajet(id):
	#Create cursor
	cur = mysql.connection.cursor()
	#get trajet by id
	res = cur.execute("SELECT * FROM trajets WHERE id=%s", [id])
	user = cur.fetchone()
	cur.close()
	#check username
	if session['username'] == user['username']:
		#Create cursor
		cur = mysql.connection.cursor()
		#get trajet by id
		res = cur.execute("DELETE FROM trajets WHERE id=%s", [id])
		#commit
		mysql.connection.commit()
		cur.close()

		flash('Trajet supprimé', 'success')

		return redirect(url_for('trajets'))
	else:
		flash('Ce trajet ne vous appartient pas', 'danger')
		
		return redirect(url_for('trajets'))


if __name__ == '__main__':
	app.secret_key='secret123'
	app.run(debug = True)
	