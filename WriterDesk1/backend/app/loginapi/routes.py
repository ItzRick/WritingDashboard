from flask import Flask
from flask import jsonify
from flask import request, current_app
from app.loginapi import bp

from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required

from app.database import postUser
from app.models import User

@bp.route('/login', methods=['POST'])
def create_token():
    '''
        This function handles the login request. When a correct combination of an username and password are given we
        respond with an access token (created using Flask_JWT). 
        Attributes:
            username: username as given in frontend
            password: password as given in frontend
            user: instance of User class from database, empty when there isn't a corresponding user for given username
            userid: id of user attribute
            access_token: JWT access token
        Return:
            Returns access_token used for authentication and user_id from user attribute when username and password corresponds to database
            Otherwise returns Unauthorized response status code
    '''
    username = request.json.get("username", None) 
    password = request.json.get("password", None)

    print(username)
    print(password)
    user = User.query.filter_by(username=username).first() # Get user from database corresponding to username
    if user is None or not user.check_password(password): # When there doesn't exists a user corresponding to username or password doesnt match
        return jsonify({"msg": "Bad username or password"}), 401 # return Unauthorized response status code
    
    access_token = create_access_token(identity=user.id)
    userid = user.id
    return jsonify(access_token=access_token, user_id = userid) 

@bp.route('/signup', methods=["POST"])
def registerUser():
    '''
        This function handles the signup request. When there is no user present in the database with the given username,
        a new user is registered with the given username.
        Attributes:
            username: username as given in frontend
            password: password as given in frontend
            isCreated: whether a new user has been registered
        Return:
            Returns request success status code with a message when a new user has been registered
            Otherwise returns bad request status code with an error message
    '''

    # Retrieve data from request
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    # Try to register new user in database
    isCreated = postUser(username, password)

    # Send response based on outcome
    if isCreated:
        # User successfully created
        return "User was successfully created!", 200
    else:
        # User exists already
        return "Account with this email already exists!", 400
    

@bp.route("/who_am_i", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(
        id=current_user.id,
        username=current_user.username,
    )
