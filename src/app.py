from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config
from flask_cors import CORS

app=Flask(__name__)

conexion=MySQL(app)
CORS(app)


#Método para listar todos los usuarios
@app.route('/users', methods=['GET'])
def list_users():
    try:
        cursor = conexion.connection.cursor()
        sqlSentence = "SELECT account_number, user_name, province, city, parish, balance FROM users"
        cursor.execute(sqlSentence)
        datos = cursor.fetchall()

        listuser = []
        for row in datos:
            user = {'account_number': row[0], 'user_name': row[1], 'province': row[2], 'city': row[3], 'parish': row[4], 'balance': row[5]}
            listuser.append(user)
        return jsonify({'usuarios': listuser, 'mensaje': "Usuarios listados con éxito"})
    except Exception as ex:
        return jsonify({'mensaje': "Error al listar los usuarios"})


#Método para buscar un usuario por el número de cuenta
@app.route('/users/<account>', methods=['GET'])
def search_user(account):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT account_number, user_name, province, city, parish, balance FROM users WHERE account_number = %s"
        cursor.execute(sql, (account,))
        info = cursor.fetchone()
        if info is not None:
            user = {'account_number': info[0], 'user_name': info[1], 'province': info[2], 'city': info[3], 'parish': info[4], 'balance': info[5]}
            return jsonify({'usuario': user, 'mensaje': "Usuario encontrado con éxito"})
        else:
            return jsonify({'mensaje': "El usuario no existe"})
    except Exception as ex:
        return jsonify({'mensaje': "Ocurrió un error en la consulta"})


#Método para registrar un nuevo usuario
@app.route('/users', methods=['POST'])
def register_user():
    try:
        cursor = conexion.connection.cursor()
        sqlSentence = """INSERT INTO users(account_number, user_name, province, city, parish, balance) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sqlSentence, (
            request.json['account_number'],
            request.json['user_name'],
            request.json['province'],
            request.json['city'],
            request.json['parish'],
            request.json['balance']
        ))
        conexion.connection.commit()
        return jsonify({'mensaje': "Usuario registrado con éxito"})
    except Exception as ex:
        return jsonify({'mensaje': "Error al registrar el usuario"})


#Para los errores
def page_not_found(error):
    return "<h1>La página a la que intentas acceder, no existe</h1>", 404  


if(__name__=='__main__'):
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.run()