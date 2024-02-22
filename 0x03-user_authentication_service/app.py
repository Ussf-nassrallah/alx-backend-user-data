#!/usr/bin/env python3
''' set up a Flask app '''

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


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
        user = AUTH.register_user(user_email, user_pssw)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": f"{user_email}", "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    ''' handle user login '''
    user_email = request.form.get('email')
    user_pssw = request.form.get('password')

    user = AUTH.valid_login(user_email, user_pssw)
    if not user:
        abort(401)

    session_id = AUTH.create_session(user_email)
    response = jsonify({"email": user_email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    ''' handle user logout '''
    session_id = request.cookies.get("session_id")

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    ''' get user profile '''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": f"{user.email}"}), 200
    abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
