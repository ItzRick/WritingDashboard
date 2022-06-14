from app import db

from flask import jsonify
from flask import request
from app.loginapi import bp

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import current_user
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from app.extensions import jwt
from app.models import User

@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

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
        return jsonify(msg = "Bad username or password", access_token = None), 403 # return Unauthorized response status code
    
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    return jsonify(
            access_token=access_token, 
            refresh_token=refresh_token,
            user_id = user.id,
            username = user.username,
            role = user.role
        ) 

@jwt.user_identity_loader
def user_identity_lookup(user):
# callback funtion will convert any User object used to create a JWT into a JSON serializable format
    print(user.id)
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
# callback function to automatically load  User object when a JWT is present in the request. 
    identity = jwt_data["sub"] # get user id from token
    return User.query.filter_by(id=identity).one_or_none()

@bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    print('test')
    return jsonify(
        id=current_user.id,
        username=current_user.username,
        role = current_user.role
    )

@jwt_required()
@bp.route("/setRole", methods=["POST"])
def setRole():
    '''
        This function handles setting the role of a user with given userId. This function is only available to admins
        Function requires a user to be logged in, use helpers > auth-header.js
        Attributes:
            userId: id of the user of whom we want to change the role
            newRole: intended role of the user
            targetUser: user with id == userId
        Return:
            Returns success if it succeeded, or an 
            error message:
                404, if there exists no user with userId
                404, if the role name is not one of ['admin', 'participant', 'researcher', 'student']
                403, if the current user is not an admin
    '''
    # retrieve data from call
    userId = request.form.get('userId')
    newRole = request.form.get('newRole')
    # get targetUser
    targetUser = User.query.filter_by(id=userId).first()

    # check if userId exists
    if targetUser is None:
        return 'user with userId not found', 404
    # check if role is valid
    if newRole not in ['admin', 'participant', 'researcher', 'student']:
        return 'Invalid role', 404
    # check if current_user is Admin
    if current_user.role != 'admin':
        return "Method only accessible for admin users", 403 # return Unauthorized response status code
    
    
    # update role
    targetUser.role = newRole
    # update the database
    db.session.commit()
    return 'success'

@jwt_required()
@bp.route("/setPassword", methods=["POST"])
def setPassword():
    '''
        This function handles setting the password for the user
        Function requires a user to be logged in, use helpers > auth-header.js
        Attributes:
            newPassword: intended password for the user
            current_user: the user currently logged in
        Return:
            Returns success if it succeeded, or an 
            error message:
                404, if the current user's id does not exist in User table
    '''
    # retrieve data from call
    newPassword = request.form.get('newPassword')

    # check if current_user is actually in Users
    if User.query.filter_by(userId=current_user.id).first() is None:
        return 'user not found', 404
    
    # set password using user function
    current_user.set_password(newPassword)
    # update the database
    db.session.commit()
    return 'success'