from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import time
from flask import request, jsonify, redirect, url_for, render_template, session, make_response
from app import app
from app.validation import *
from app.reading import *

app.secret_key = 'your_secret_key'

# Variables globales
max_attempts = 3
lockout_time = 5 * 60  # 5 minutos en segundos
user_status = {}

@app.route('/api/users', methods=['POST'])
def create_record():
    data = request.form
    email = data.get('email')
    username = data.get('username')
    nombre = data.get('nombre')
    apellido = data.get('Apellidos')
    password = data.get('password')
    dni = data.get('dni')
    dob = data.get('dob')
    role = data.get('role')
    errores = []
    print(data)
    # Validaciones
    if not validate_email(email):
        errores.append("Email inválido")
    if not validate_pswd(password):
        errores.append("Contraseña inválida")
    if not validate_dob(dob):
        errores.append("Fecha de nacimiento inválida")
    if not validate_dni(dni):
        errores.append("DNI inválido")
    if not validate_user(username):
        errores.append("Usuario inválido")
    if not validate_name(nombre):
        errores.append("Nombre inválido")
    if not validate_name(apellido):
        errores.append("Apellido inválido")
    if not validate_role(role):
        errores.append("Rol inválido")

    if errores:
        return render_template('form.html', error=errores)

    email = normalize_input(email)

    db = read_db("db.txt")
    db[email] = {
        'nombre': normalize_input(nombre),
        'apellido': normalize_input(apellido),
        'username': normalize_input(username),
        'password': normalize_input(password),
        "dni": dni,
        'dob': normalize_input(dob),
        "role": role
    }

    write_db("db.txt", db)
    return redirect("/login")


# Endpoint para el login
@app.route('/api/login', methods=['POST'])
def api_login():
    email = normalize_input(request.form['email'])
    password = normalize_input(request.form['password'])

    db = read_db("db.txt")
    if email not in db:
        error = "Credenciales inválidas"
        return render_template('login.html', error=error)

    # Verificar el estado del usuario
    if email in user_status:
        if user_status[email]['intentos'] >= max_attempts:
            if time.time() < user_status[email]['tiempo_bloqueo']:
                remaining_time = int(user_status[email]['tiempo_bloqueo'] - time.time())
                minutes, seconds = divmod(remaining_time, 60)
                error = f"Cuenta bloqueada. Inténtelo nuevamente en {minutes} minutos y {seconds} segundos."
                return render_template('login.html', error=error)
            else:
                # Resetear intentos después del tiempo de bloqueo
                user_status[email]['intentos'] = 0

    password_db = db.get(email)["password"]

    if password_db == password:
        session['role'] = db[email]['role']
        session['email'] = email  # Almacenar el email del usuario en la sesión
        # Resetear intentos en caso de éxito
        user_status[email] = {'intentos': 0, 'tiempo_bloqueo': 0}
        return redirect(url_for('customer_menu'))
    else:
        # Incrementar el contador de intentos fallidos
        if email not in user_status:
            user_status[email] = {'intentos': 0, 'tiempo_bloqueo': 0}
        user_status[email]['intentos'] += 1
        if user_status[email]['intentos'] >= max_attempts:
            user_status[email]['tiempo_bloqueo'] = time.time() + lockout_time
            remaining_time = int(user_status[email]['tiempo_bloqueo'] - time.time())
            minutes, seconds = divmod(remaining_time, 60)
            error = f"Cuenta bloqueada. Inténtelo nuevamente en {minutes} minutos y {seconds} segundos."
        else:
            error = "Credenciales inválidas"
        return render_template('login.html', error=error)


# Página principal del menú del cliente
@app.route('/customer_menu')
def customer_menu():

    db = read_db("db.txt")

    transactions = read_db("transaction.txt")
    current_balance = 100
    last_transactions = []
    message = request.args.get('message', '')
    error = request.args.get('error', 'false').lower() == 'true'
    return render_template('customer_menu.html',
                           message=message,
                           nombre="",
                           balance=current_balance,
                           last_transactions=last_transactions,
                           error=error,)


# Endpoint para leer un registro
@app.route('/records', methods=['GET'])
def read_record():
    db = read_db("db.txt")
    message = request.args.get('message', '')
    user_role = session.get('role')
    user_email = session.get('email')

    if user_role == 'admin':
        # Mostrar todos los registros para el rol admin
        return render_template('records.html', users=db, role=user_role, message=message)
    elif user_role == 'user':
        # Mostrar solo el registro del usuario para el rol user
        user_record = {user_email: db.get(user_email)}
        return render_template('records.html', users=user_record, role=user_role, message=message)
    else:
        # Redirigir a la página de inicio de sesión si el rol no es válido
        return redirect(url_for('login'))


@app.route('/update_user/<email>', methods=['POST'])
def update_user(email):
    db = read_db("db.txt")
    user_role = session.get('role')
    user_email = session.get('email')

    if user_role == 'admin' or (user_role == 'user' and user_email == email):
        username = request.form['username']
        dni = request.form['dni']
        dob = request.form['dob']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        errores = []

        if not validate_dob(dob):
            errores.append("Fecha de nacimiento inválida")
        if not validate_dni(dni):
            errores.append("DNI inválido")
        if not validate_user(username):
            errores.append("Usuario inválido")
        if not validate_name(nombre):
            errores.append("Nombre inválido")
        if not validate_name(apellido):
            errores.append("Apellido inválido")

        if errores:
            return render_template('edit_user.html',
                                   user_data=db[email],
                                   email=email,
                                   error=errores)

        db[email]['username'] = normalize_input(username)
        db[email]['nombre'] = normalize_input(nombre)
        db[email]['apellido'] = normalize_input(apellido)
        db[email]['dni'] = dni
        db[email]['dob'] = normalize_input(dob)

        write_db("db.txt", db)

        # Redirigir al usuario a la página de records con un mensaje de éxito
        return redirect(url_for('read_record', message="Información actualizada correctamente"))
    else:
        # Redirigir a la página de inicio de sesión si el rol no es válido
        return redirect(url_for('login'))


@app.route('/delete_user/<email>', methods=['POST'])
def delete_user(email):
    user_role = session.get('role')

    if user_role == 'admin':
        db = read_db("db.txt")
        if email in db:
            del db[email]
            write_db("db.txt", db)
            message = "Usuario eliminado correctamente."
        else:
            message = "Usuario no encontrado."
    else:
        message = "No tienes permiso para eliminar usuarios."

    return redirect(url_for('read_record', message=message))
