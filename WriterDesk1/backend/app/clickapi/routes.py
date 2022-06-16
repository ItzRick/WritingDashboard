from app.scoreapi import bp

from flask import request, jsonify
from app.models import Clicks, User
from app.database import uploadToDatabase, removeFromDatabase
from sqlalchemy import func
from flask_jwt_extended import jwt_required, current_user

@bp.route('/setClick', methods = ['POST'])
@jwt_required()
def setScore():
    '''
        set score for the current user
        Attributes:
            userId: user id of the currently logged in user
            url: url of current page as given by the front end
        Return:
            Returns 'successfully uploaded click' if it succeeded, or an 
            error message:
                404, if there exists no user with userId
                451, if the current user does not want to get tracked


        TODO: only collect when logged in
        TODO: only collect when user has agreed
    '''
    # get user id from current user
    userId = current_user.id 
    # get the data as sent by the react frontend:
    url = request.form.get('url')

    # TODO: more data?

    # check if userId is exists
    if User.query.filter_by(id=userId).first() is None:
        return 'User not Found', 404
    # check if user wants to be tracked (and this user is not just an participant)
    if current_user.id == '' and current_user.role != 'participant':
        return 'Do not track this user', 451

    # TODO: more checks?

    # create Clicks object
    clickInDB = Clicks(
        userId=userId,
        url=url
    )
    # upload
    uploadToDatabase(clickInDB)

    return 'successfully uploaded click'
