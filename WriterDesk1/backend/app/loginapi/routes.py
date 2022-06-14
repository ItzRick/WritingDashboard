from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask import Flask
from flask import jsonify
from flask import request, current_app
from app.loginapi import bp

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import current_user
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from app.extensions import jwt
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
    user = User.query.filter_by(username=username).first() # Get user from database corresponding to username
    if user is None or not user.check_password(password): # When there doesn't exists a user corresponding to username or password doesnt match
        return jsonify(msg = "Bad username or password", access_token = None), 403 # return Unauthorized response status code
    
    access_token = create_access_token(identity=user) # Create new access token, uses user_identitiy_lookup as identity
    return jsonify(
            access_token=access_token,
            user_id = user.id,
            username = user.username,
            role = user.type
        ) 

@jwt.user_identity_loader
def user_identity_lookup(user):
    '''
        Callback funtion will convert any User object used to create a JWT into a JSON serializable format
        Return:
            Returns User.id
    '''
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    '''
        Callback function to automatically load User object when a JWT is present in the request.
        Return:
            Returns User, corresponding to JWT token that is used in route
    '''
    identity = jwt_data["sub"] # get user id from token
    return User.query.filter_by(id=identity).one_or_none()

@bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    '''
        This is a function that uses jwt_required, this route needs a valid JWT token before this endpoint can be called.
        We return the user id, name and role
    '''
    return jsonify(
        id=current_user.id,
        username=current_user.username,
        role = current_user.type
    )
