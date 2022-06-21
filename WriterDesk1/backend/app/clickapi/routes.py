import os
from app.clickapi import bp

from flask import current_app, request
from app.models import Clicks, User
from app.database import uploadToDatabase
from flask_jwt_extended import jwt_required, current_user

from app.database import recordsToCsv

@bp.route('/addClick', methods = ['POST'])
@jwt_required()
def addClick():
    '''
        set click for the current user, triggered when a user views a document, or clicks an event
        Attributes:
            userId: user id of the currently logged in user
            url: url of the page where the click happened
            eventType: type of event, can be one of [click.button, click.link, view.document, click.highlight]
            actionId: in case of a click: name of the button
                      in case of a view: name of the document
        Return:
            Returns 'successfully uploaded click' if it succeeded, or an 
            error message:
                451, if the current user does not want to get tracked
                400, if the eventType is not one of [click.button, click.link, view.document, click.highlight]

    '''
    # get user id from current user
    userId = current_user.id 
    # get the data as sent by the react frontend:
    url = request.form.get('url', None)
    eventType = request.form.get('eventType', None)
    actionId = request.form.get('actionId', None)

    # check if user wants to be tracked (ignoring trackability for participants)
    if not current_user.trackable and current_user.role != 'participant':
        return 'User clicks not trackable', 451
    # check if eventType is one of [click.button, click.link, view.document]
    if eventType not in ["click.button", "click.link", "view.document", "click.highlight"]:
        return 'Invalid eventType', 400

    # create Clicks object
    clickInDB = Clicks(
        userId=userId,
        url=url,
        eventType=eventType,
        actionId=actionId,
    )
    # upload
    uploadToDatabase(clickInDB)

    return 'successfully uploaded click'

@bp.route('/getParticipantsUserData', methods=['GET'])
@jwt_required()
def getParticipantsUserData():
    '''
        This function retrieves the user data from a set of participants. 
        Participants that do not exist have no information in the returned file.
        Attributes:
            ids: the user ids of all participants user data needs to be
            retreived for.
            output: a list of dictionaries containing all user data for the set
            of participants.
            data: the user data for one participant.
            path: the path to the csv with user data for a set of participants.
            response: http response with the csv file.
        Return:
            response, 200: an http response with the csv file when it was
            created succesfully.
            error 403: if the user accessing this method does not have the
            rights to call it.
    '''
    # check if user is admin OR researcher (i.e. reject if user is neither)
    if current_user.role != 'admin' and current_user.role != 'researcher':
        return 'Method only accessible for admin or researcher users', 403

    # get the ids from the participants
    ids = request.args.getlist('userId')

    output = []
    # go over all user ids
    for id in ids:
        # if the user id does not exist in the database
        if Clicks.query.filter_by(userId=id).first() is None:
            # add an empty row with only the user id to the csv file
            output.append(Clicks(id, None, None).serializeClick())
            continue
        # retrieve the data for the given user id
        data = Clicks.query.filter_by(userId=id).all()
        # add the dictionary to the list of dictionaries
        output.extend(Clicks.serializeList(data))
    
    # create the csv file from the list of dictionaries
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], str(current_user.id), "downloadParticipantsUserData.csv")
    recordsToCsv(path, output)

    # generator to delete file after sending
    def generate():
            with open(path) as f:
                yield from f

            os.remove(path)

    # create response
    response = current_app.response_class(generate(), mimetype='text/csv')
    # set headers to show that the response contains a file and what the name of the file should be
    response.headers.set('Content-Disposition', 'attachment')
    response.headers.set('custom-filename', 'participantsUserData.csv')
    return response, 200
