from app.feedback.retrieveText.convertDocxTxtToText import getTXTText, getDOCXText
from app.feedback.retrieveText.convertPdfToText import getPDFText
from app.feedback.generateFeedback.CohesionFeedback import CohesionFeedback
from app.feedback.generateFeedback.IntegrationContentFeedback import IntegrationContentFeedback
from app.feedback.generateFeedback.LanguageStyleFeedback import LanguageStyleFeedback
from app.feedback.generateFeedback.StructureFeedback import StructureFeedback
from app.fileapi.convert import convertDocx, convertTxt
from app.scoreapi.scores import getCurrentExplanationVersion, removeExplanationsAndScores
from flask import current_app
from decimal import Decimal

def genFeedback(file):
    '''
        Generate the feedback for a specific file, that is run the methods to generate the explanations and scores for 
        the file, for each of the four categories. To do this, we first retrieve the text by means of the get...Text methods. 
        Lastly, we run the getMistakeInformation... methods and add these explanations of the mistakes to the database.
        attributes:
            fileId: The file Id of the file we are currently generating feedback for.
            fileType: The FileType of the file we are currently generating feedback for.
            path: The path of the file we are currently generating feedback for.
            userId: The User id of the user we are currently generating feedback for.
            references: References as retrieved from the get...Text method.
            text: Text as retrieved from the convert text method for the correct filetype.
            textStructure: Text as retrieved from the convert text method for the correct filetype, including all in-line citations.
            feedbackEngines: List with objects to create the feedback for the current file. So one object for language and style, one for Cohesion,
            one for structure and one for source integration and content.
        arguments: 
            file: The file we are generating the feedback for and uploading this feedback for to the database. 
        returns: 
            True if the feedback has been successfully generated and added to the database, false with an error message otherwise.
    '''
    # Retrieve the required information from the file:
    fileId = file.id
    fileType = file.fileType
    path = file.path
    userId = file.userId
    try:
        # Check if the feedback has already been generated:
        if getCurrentExplanationVersion(fileId) >= Decimal(current_app.config['FEEDBACKVERSION']):
            return False, 'Feedback has already been generated!'
        # If feedback has already been generated, remove the current explanations and scores if required:
        else:
            removeExplanationsAndScores(fileId)
        # Initialize empty string for the references:
        references = ''
        # Retrieve the text from each fileType, and convert this file if required:
        if fileType == '.docx':
            text, references = getDOCXText(path)
            path = convertDocx(path)
            textStructure = text
        elif fileType == '.pdf':
            textStructure = getPDFText(path, returnReferencesText=True)
            text, references = getPDFText(path, returnReferences=True)
        elif fileType == '.txt':
            text = getTXTText(path)
            path = convertTxt(path)
            textStructure = text

        # Create the feedbackEngines in a list, one for each skill category:
        feedbackEngines = [
            LanguageStyleFeedback(text, references, fileId, userId, path),
            CohesionFeedback(text, references, fileId, userId, path),
            StructureFeedback(textStructure, references, fileId, userId, path),
            IntegrationContentFeedback(text, references, fileId, userId, path)
        ]

        # For each feedbackEngine, generate the feedback, upload this to the database and delete this feedback object:
        for feedbackEngine in feedbackEngines:
            feedbackEngine.genFeedback()
            feedbackEngine.uploadToDatabase()
            del feedbackEngine
    except Exception as e:
        return False, str(e)
    return True, 'Feedback has been generated!'
