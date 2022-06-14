from flask import jsonify

from app.database import getUsers
from app.models import User
from app.usersapi import bp


@bp.route('/users', methods=['GET'])
def usersRetrieve():
    '''
    This function handles the retrieval of users except for users
    with the participant role in the form of a json file.
    '''

    # Retrieve list of files that were uploaded by the current user,
    # ordered by the sorting attribute in the request
    users = getUsers();

    if len(users) != 0:
        # Return http response with list as json in response body
        return jsonify(users)
    else:
        return 'No user available', 400
