#!/usr/bin/env python3
''' set up a Flask app '''

from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
auth = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    ''' handle GET "/" '''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    ''' post a new user '''
    user_email = request.form.get('email')
    user_pssw = request.form.get('password')
    try:
        user = auth.register_user(user_email, user_pssw)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": f"{user_email}", "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    ''' handle user login '''
    email = request.form.get('email')
    password = request.form.get('password')

    user = auth.valid_login(email, password)
    if not user:
        abort(401)

    session_id = auth.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
