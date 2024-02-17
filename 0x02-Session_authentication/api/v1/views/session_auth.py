#!/usr/bin/env python3

from flask import request, jsonify
from api.v1.views import app_views
from models.user import User


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
            from api.v1.app import auth
            sess_id = auth.create_session(u.id)
            reply = jsonify(user.to_json())
            sess_name = os.getenv('SESSION_NAME')
            reply.set_cookie(sess_name, sess_id)
            return reply

    if not User.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
