from flask import request
from flask_restful import Resource

class AuthenticationResource(Resource):
    def post(self):
        # Usar .get() previene errores si no envían el json
        data = request.get_json(force=True, silent=True)
        if not data:
            return {'message': 'Invalid data'}, 400

        username = data.get('username')
        password = data.get('password')

        if username == 'student' and password == 'desingp':
            # Retornamos el mismo token que espera el decorador
            return {'token': 'abcd12345'}, 200
        else:
            return {'message': 'Unauthorized'}, 401