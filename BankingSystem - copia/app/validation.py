from datetime import datetime
import re

import unicodedata


def normalize_input(data):
    return unicodedata.normalize('NFKD', data)


# valido el email
def validate_email(email):
    email = normalize_input(email)
    patron = r'^[a-z]+\.[a-z]+@urosario\.edu\.co$'
    return bool(re.fullmatch(patron, email))

# valido la edad
def validate_dob(dob):
    try:
        fecha_nac = datetime.strptime(dob, "%Y-%m-%d")
        today = datetime.today()
        anio_limite = today.year - 16
        if fecha_nac.year < anio_limite:
            return True
        elif fecha_nac.year == anio_limite:
            if fecha_nac.month < today.month or (fecha_nac.month == today.month and fecha_nac.day <= today.day):
                return True
        return False
    except ValueError:
        return False


# valido el usuario
def validate_user(user):
    patron = r'^[a-z]+(\.[a-z]+)$'
    return bool(re.fullmatch(patron, user))


# valido el dni
def validate_dni(dni):
    return dni.isdigit() and len(dni) == 10 and dni.startswith("1000000000")


# valido la contraseña
def validate_pswd(pswd):
    patron = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#*@\$%&\-!+=?])[A-Za-z\d#*@\$%&\-!+=?]{8,35}$'
    return bool(re.fullmatch(patron, pswd))


def validate_name(name):
    patron = r'^[a-z]$'
    return bool(re.fullmatch(patron, name))
