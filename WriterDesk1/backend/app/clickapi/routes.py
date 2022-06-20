from app.clickapi import bp

from flask import request
from app.models import Clicks, User
from app.database import uploadToDatabase
from flask_jwt_extended import jwt_required, current_user

@bp.route('/setClick', methods = ['POST'])
@jwt_required()
def setClick():
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


    '''
    # get user id from current user
    userId = current_user.id 
    # get the data as sent by the react frontend:
    url = request.form.get('url')

    # TODO: more data?

    # check if userId is exists
    if User.query.filter_by(id=userId).first() is None:
        return 'User not Found', 404
    # check if user wants to be tracked (ignoring trackability for participants)
    if not current_user.trackable and current_user.role != 'participant':
        return 'User clicks not trackable', 451

    # TODO: valid url?


    # TODO: more checks?

    # create Clicks object
    clickInDB = Clicks(
        userId=userId,
        url=url
    )
    # upload
    uploadToDatabase(clickInDB)

    return 'successfully uploaded click'
