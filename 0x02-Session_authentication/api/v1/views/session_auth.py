#!/usr/bin/env python3
''' session_auth viewer '''

from flask import request, jsonify
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    ''' handle user Login '''
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400

    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    users_list = User.search({'email': email})

    if not users_list or len(users_list) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    else:
        for u in users_list:
            if u.is_valid_password(password):
                from api.v1.app import auth
                sess_id = auth.create_session(u.id)
                reply = jsonify(u.to_json())
                sess_name = getenv('SESSION_NAME')
                reply.set_cookie(sess_name, sess_id)
                return reply

    return jsonify({"error": "wrong password"}), 401
