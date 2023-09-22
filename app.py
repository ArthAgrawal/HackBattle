from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os


app = Flask(__name__)

uploaded_files = []
app.secret_key = 'your secret key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'arth2004'
app.config['MYSQL_DB'] = 'Student_Profiles'


mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(
			'SELECT * FROM accounts WHERE username = % s \
			AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg=msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():


    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'phonenumber' in request.form:
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		phonenumber = request.form['phonenumber']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(
			'SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'name must contain only characters and numbers !'
		else:
			cursor.execute('INSERT INTO accounts VALUES \
			(NULL, % s, % s, % s, % s)',
						(username, password, email,
							phonenumber, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('index.html', msg=msg)


@app.route("/index")
def index():
	if 'loggedin' in session:
		return render_template("index.html")
	return redirect(url_for('login'))


@app.route("/display")
def display():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE id = % s',
					(session['id'], ))
		account = cursor.fetchone()
		return render_template("display.html", account=account)
	return redirect(url_for('login'))


@app.route("/update", methods=['GET', 'POST'])
def update():
	msg = ''
	if 'loggedin' in session:
		if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'phonenumber' in request.form:
			username = request.form['username']
			password = request.form['password']
			email = request.form['email']
			phonenumber = request.form['phonenumber']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute(
				'SELECT * FROM accounts WHERE username = % s',
					(username, ))
			account = cursor.fetchone()
			if account:
				msg = 'Account already exists !'
			elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
				msg = 'Invalid email address !'
			elif not re.match(r'[A-Za-z0-9]+', username):
				msg = 'name must contain only characters and numbers !'
			else:
				cursor.execute('UPDATE accounts SET username =% s,\
				password =% s, email =% s, phonenumber =% s WHERE id =% s', (
					username, password, email, phonenumber,
				(session['id'], ), ))
				mysql.connection.commit()
				msg = 'You have successfully updated !'
		elif request.method == 'POST':
			msg = 'Please fill out the form !'
		return render_template("update.html", msg=msg)
	return redirect(url_for('login'))










@app.route('/a')
def a():
    return render_template('Test.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    uploaded_file = request.files['pdfFile']

    if uploaded_file.filename != '':
        # Save the uploaded PDF file to the "uploads" folder
        pdf_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(pdf_path)

        # Add the filename to the list of uploaded files
        uploaded_files.append(uploaded_file.filename)

        return f'PDF file "{uploaded_file.filename}" uploaded successfully. <a href="/download">View Downloads</a>'

    return 'No file selected for upload.'

@app.route('/download')
def download_pdfs():
    return render_template('download.html', uploaded_files=uploaded_files)

@app.route('/download/<filename>')
def download_pdf(filename):
    # Generate the full path to the uploaded PDF file
    pdf_path = os.path.join('uploads', filename)

    # Check if the file exists
    if os.path.exists(pdf_path):
        # Use Flask's send_file to send the file to the user's browser for download
        return send_file(pdf_path, as_attachment=True)
    else:
        return 'File not found.'



if __name__ == "__main__":
	app.run(host="localhost", port=int("5000"))
