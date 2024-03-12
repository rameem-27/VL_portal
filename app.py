from flask import Flask, render_template, request, redirect ,url_for, flash
from voter_search import search_voter
from aadhaar_search import search_aadhaar
from voter_jinja import jinja_voter
from aadhaar_jinja import jinja_aadhaar
import sqlite3

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def root():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    error=''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('credentials.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM credentials WHERE username=?", (username,))
        queried_data = cursor.fetchone()
        if queried_data and password == queried_data[0]:
            return redirect(url_for('home'))
        else:
            flash('Wrong email or password')
            return redirect(url_for('login'))
    return render_template('login.html')



@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        uid_value = request.form['searchInput']
        x = search_voter(uid_value)
        if x == True:
            return jinja_voter(uid_value)
        elif x == False:
            y = search_aadhaar(uid_value)
            return jinja_aadhaar(uid_value)
    else:
        return render_template('home.html')
    
    
    
@app.route('/remove', methods=['POST'])
def removing_voter():
    if request.method == 'POST':
        data = request.json
        uid_value = data.get('uid_value')
        conn = sqlite3.connect('voters.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM list WHERE uid=?", (uid_value,))
        conn.commit()
        conn.close()
    return render_template('home.html')



    
@app.route('/add',methods=['POST','GET'])
def adding_voter():
    if request.method == 'POST':
        data = request.json
        uid_value = data.get('uid_value')
        aadhaar_conn = sqlite3.connect('aadhaar.db')
        aadhaar_cursor = aadhaar_conn.cursor()
        aadhaar_cursor.execute(f"SELECT * FROM details WHERE uid={uid_value}")
        result = aadhaar_cursor.fetchone()
        uid = result[0]
        name = result[1]
        gender = result[2]
        co = result[3]
        house = result[4]
        yob = result[7]
        aadhaar_conn.close()
        voters_conn = sqlite3.connect('voters.db')
        voters_cursor = voters_conn.cursor()
        voters_cursor.execute('INSERT INTO list (uid, name, gender,co, house, yob) VALUES (?,?,?,?,?,?)', (uid,name,gender,co,house,yob))
        voters_conn.commit()
        voters_conn.close()
    return render_template('home.html')       
        




@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)