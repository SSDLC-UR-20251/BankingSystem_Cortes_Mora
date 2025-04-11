from flask import render_template, redirect, url_for, session, request
from app import app
from app.encryption import decrypt_aes, ofuscar_dni
from app.reading import read_db



@app.route('/')
def index():
    darkmode = request.cookies.get('darkmode', 'light')
    return render_template('index.html', darkmode=darkmode)


@app.route('/deposit', methods=['GET'])
def deposit():
    darkmode = request.cookies.get('darkmode', 'light')
    return render_template('deposit.html', darkmode=darkmode)


@app.route('/register', methods=["GET", "POST"])
def register():
    darkmode = request.cookies.get('darkmode', 'light')
    return render_template('form.html', darkmode=darkmode)


@app.route('/login', methods=["GET"])
def login():
    darkmode = request.cookies.get('darkmode', 'light')
    return render_template("login.html", darkmode=darkmode)


@app.route('/edit_user/<email>', methods=['GET'])
def edit_user(email):
    db = read_db("db.txt")

    if email not in db:
        return redirect(url_for('records', message="Usuario no encontrado"))
    user_info = db[email]
    darkmode = request.cookies.get('darkmode', 'light')
    return render_template('edit_user.html', user_data=user_info, email=email, darkmode=darkmode)


# Formulario de retiro
@app.route('/withdraw', methods=['GET'])
def withdraw():
    email = session.get('email')
    print(email)
    transactions = read_db("transaction.txt")
    current_balance = sum(float(t['balance']) for t in transactions.get(email, []))
    darkmode = request.cookies.get('darkmode', 'light')
    return render_template('withdraw.html', balance=current_balance, darkmode=darkmode)
