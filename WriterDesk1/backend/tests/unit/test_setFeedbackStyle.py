# from app.feedback.feedback import setFeedbackStyle
# from app.models import Files, Explanations
# import os
# import fitz

# def testSetFeedbackStyleNoAlternatives(testClient, initDatabase):
#     '''
#         Test the setFeedbackStyle method from the feedback file in the feedback blueprint, on style feedback without replacements. 
#         Attributes:
#             file: A file which has been added to the database previously, retrieved for the fileId.
#             fileId: fileId of this file that has been previously added to the database.
#             explanationText: The explanationText we set using the method and check we can retrieve later.
#             mistakes: mistakes in the correct format as given to the setFeedbackStyle method. 
#             BASEPATH: Path of the current test_setFeedbackStyle.py file.
#             fileLoc: Location of the file we test this for.
#             explanations: Database for the current file, containing explanations, as retrieved from the database.
#         Arguments:
#             testClient:  The test client we test this for.
#             initDatabase: the database instance we test this for. 
    
#     '''
#     del testClient, initDatabase
#     # Retrieve a fileId from a file in the database:
#     file = Files.query.first()
#     fileId = file.id
#     # Create a mistakes dictionary, to test the method on, such as it will also be generated by the application:
#     mistakes = [
#         ['a', 'tor into thinking it is conversing with a another human, like with the Google Dup',
#          0, 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".',
#          []
#         ],
#         ['must try', 'e hand of asking (written) questions. A must try to cause C to make the wrong identifica',
#          0, 'It appears that a hyphen is missing in this expression.', []
#         ]
#     ]
#     # Set the file location of the test file:
#     BASEPATH = os.path.abspath(os.path.dirname(__file__))
#     fileLoc = os.path.join(BASEPATH, 'testFilesStyle', 'testStyleOnePageTwoMistakes.pdf')
#     # Call the setFeedbackStyle method:
#     setFeedbackStyle(mistakes, fileLoc, fileId)
#     # Retrieve the explanations for this file from the database:
#     explanations = Explanations.query.filter_by(fileId = fileId).all()
#     # Check if all information about this mistake has been added to this database correctly:
#     assert explanations[0].mistakeText == 'a'
#     assert explanations[0].explanation == 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".'
#     assert explanations[0].type == 0
#     assert explanations[1].mistakeText == 'must try'
#     assert explanations[1].explanation == 'It appears that a hyphen is missing in this expression.'
#     assert explanations[1].type == 0
#     # Check if the coordinates of the mistakes have also been found correctly:
#     doc = fitz.open(fileLoc)
#     page = doc.load_page(0)
#     assert page.get_textbox(fitz.Rect(explanations[0].X1, explanations[0].Y1, explanations[0].X2, explanations[0].Y2)) == 'a'
#     assert page.get_textbox(fitz.Rect(explanations[1].X1, explanations[1].Y1, explanations[1].X2, explanations[1].Y2)) == 'must try'

# def testSetFeedbackStyleOneAlternative(testClient, initDatabase):
#     '''
#         Test the setFeedbackStyle method from the feedback file in the feedback blueprint, on style feedback with one replacement each. 
#         Attributes:
#             file: A file which has been added to the database previously, retrieved for the fileId.
#             fileId: fileId of this file that has been previously added to the database.
#             explanationText: The explanationText we set using the method and check we can retrieve later.
#             mistakes: mistakes in the correct format as given to the setFeedbackStyle method. 
#             BASEPATH: Path of the current test_setFeedbackStyle.py file.
#             fileLoc: Location of the file we test this for.
#             explanations: Database for the current file, containing explanations, as retrieved from the database.
#             doc: The file opened by fitz.
#             page: page of the document as opened by fitz.
#         Arguments:
#             testClient:  The test client we test this for.
#             initDatabase: the database instance we test this for. 
    
#     '''
#     del testClient, initDatabase
#     # Retrieve a fileId from a file in the database:
#     file = Files.query.first()
#     fileId = file.id
#     # Create a mistakes dictionary, to test the method on, such as it will also be generated by the application:
#     mistakes = [
#         ['a', 'tor into thinking it is conversing with a another human, like with the Google Dup',
#          0, 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".',
#          ['an']
#         ],
#         ['must try', 'e hand of asking (written) questions. A must try to cause C to make the wrong identifica',
#          0, 'It appears that a hyphen is missing in this expression.', ['must-try']
#         ]
#     ]
#     # Set the file location of the test file:
#     BASEPATH = os.path.abspath(os.path.dirname(__file__))
#     fileLoc = os.path.join(BASEPATH, 'testFilesStyle', 'testStyleOnePageTwoMistakes.pdf')
#     # Call the setFeedbackStyle method:
#     setFeedbackStyle(mistakes, fileLoc, fileId)
#     # Retrieve the explanations for this file from the database:
#     explanations = Explanations.query.filter_by(fileId = fileId).all()
#     # Check if all information about this mistake has been added to this database correctly:
#     assert explanations[0].mistakeText == 'a'
#     assert explanations[0].explanation == 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".'
#     assert explanations[0].type == 0
#     assert explanations[0].replacement1 == 'an'
#     assert explanations[1].mistakeText == 'must try'
#     assert explanations[1].explanation == 'It appears that a hyphen is missing in this expression.'
#     assert explanations[1].type == 0
#     assert explanations[1].replacement1 == 'must-try'
#     # Check if the coordinates of the mistakes have also been found correctly:
#     doc = fitz.open(fileLoc)
#     page = doc.load_page(0)
#     assert page.get_textbox(fitz.Rect(explanations[0].X1, explanations[0].Y1, explanations[0].X2, explanations[0].Y2)) == 'a'
#     assert page.get_textbox(fitz.Rect(explanations[1].X1, explanations[1].Y1, explanations[1].X2, explanations[1].Y2)) == 'must try'

# def testSetFeedbackStyleTwoAlternatives(testClient, initDatabase):
#     '''
#         Test the setFeedbackStyle method from the feedback file in the feedback blueprint, on style feedback with two replacements each. 
#         Attributes:
#             file: A file which has been added to the database previously, retrieved for the fileId.
#             fileId: fileId of this file that has been previously added to the database.
#             explanationText: The explanationText we set using the method and check we can retrieve later.
#             mistakes: mistakes in the correct format as given to the setFeedbackStyle method. 
#             BASEPATH: Path of the current test_setFeedbackStyle.py file.
#             fileLoc: Location of the file we test this for.
#             explanations: Database for the current file, containing explanations, as retrieved from the database.
#             doc: The file opened by fitz.
#             page: page of the document as opened by fitz.
#         Arguments:
#             testClient:  The test client we test this for.
#             initDatabase: the database instance we test this for. 
    
#     '''
#     del testClient, initDatabase
#     # Retrieve a fileId from a file in the database:
#     file = Files.query.first()
#     fileId = file.id
#     # Create a mistakes dictionary, to test the method on, such as it will also be generated by the application:
#     mistakes = [
#         ['a', 'tor into thinking it is conversing with a another human, like with the Google Dup',
#          0, 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".',
#          ['first', 'second']
#         ],
#         ['must try', 'e hand of asking (written) questions. A must try to cause C to make the wrong identifica',
#          0, 'It appears that a hyphen is missing in this expression.', ['first', 'second']
#         ]
#     ]
#     # Set the file location of the test file:
#     BASEPATH = os.path.abspath(os.path.dirname(__file__))
#     fileLoc = os.path.join(BASEPATH, 'testFilesStyle', 'testStyleOnePageTwoMistakes.pdf')
#     # Call the setFeedbackStyle method:
#     setFeedbackStyle(mistakes, fileLoc, fileId)
#     # Retrieve the explanations for this file from the database:
#     explanations = Explanations.query.filter_by(fileId = fileId).all()
#     # Check if all information about this mistake has been added to this database correctly:
#     assert explanations[0].mistakeText == 'a'
#     assert explanations[0].explanation == 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".'
#     assert explanations[0].type == 0
#     assert explanations[0].replacement1 == 'first'
#     assert explanations[0].replacement2 == 'second'
#     assert explanations[1].mistakeText == 'must try'
#     assert explanations[1].explanation == 'It appears that a hyphen is missing in this expression.'
#     assert explanations[1].type == 0
#     assert explanations[1].replacement1 == 'first'
#     assert explanations[1].replacement2 == 'second'
#     # Check if the coordinates of the mistakes have also been found correctly:
#     doc = fitz.open(fileLoc)
#     page = doc.load_page(0)
#     assert page.get_textbox(fitz.Rect(explanations[0].X1, explanations[0].Y1, explanations[0].X2, explanations[0].Y2)) == 'a'
#     assert page.get_textbox(fitz.Rect(explanations[1].X1, explanations[1].Y1, explanations[1].X2, explanations[1].Y2)) == 'must try'

# def testSetFeedbackStyleThreeAlternatives(testClient, initDatabase):
#     '''
#         Test the setFeedbackStyle method from the feedback file in the feedback blueprint, on style feedback with three replacements each. 
#         Attributes:
#             file: A file which has been added to the database previously, retrieved for the fileId.
#             fileId: fileId of this file that has been previously added to the database.
#             explanationText: The explanationText we set using the method and check we can retrieve later.
#             mistakes: mistakes in the correct format as given to the setFeedbackStyle method. 
#             BASEPATH: Path of the current test_setFeedbackStyle.py file.
#             fileLoc: Location of the file we test this for.
#             explanations: Database for the current file, containing explanations, as retrieved from the database.
#             doc: The file opened by fitz.
#             page: page of the document as opened by fitz.
#         Arguments:
#             testClient:  The test client we test this for.
#             initDatabase: the database instance we test this for. 
    
#     '''
#     del testClient, initDatabase
#     # Retrieve a fileId from a file in the database:
#     file = Files.query.first()
#     fileId = file.id
#     # Create a mistakes dictionary, to test the method on, such as it will also be generated by the application:
#     mistakes = [
#         ['a', 'tor into thinking it is conversing with a another human, like with the Google Dup',
#          0, 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".',
#          ['first', 'second', 'third']
#         ],
#         ['must try', 'e hand of asking (written) questions. A must try to cause C to make the wrong identifica',
#          0, 'It appears that a hyphen is missing in this expression.', ['first', 'second', 'third']
#         ]
#     ]
#     # Set the file location of the test file:
#     BASEPATH = os.path.abspath(os.path.dirname(__file__))
#     fileLoc = os.path.join(BASEPATH, 'testFilesStyle', 'testStyleOnePageTwoMistakes.pdf')
#     # Call the setFeedbackStyle method:
#     setFeedbackStyle(mistakes, fileLoc, fileId)
#     # Retrieve the explanations for this file from the database:
#     explanations = Explanations.query.filter_by(fileId = fileId).all()
#     # Check if all information about this mistake has been added to this database correctly:
#     assert explanations[0].mistakeText == 'a'
#     assert explanations[0].explanation == 'Use "an" instead of "a" if the following word starts with a vowel sound, e.g. "an article", "an hour".'
#     assert explanations[0].type == 0
#     assert explanations[0].replacement1 == 'first'
#     assert explanations[0].replacement2 == 'second'
#     assert explanations[0].replacement3 == 'third'
#     assert explanations[1].mistakeText == 'must try'
#     assert explanations[1].explanation == 'It appears that a hyphen is missing in this expression.'
#     assert explanations[1].type == 0
#     assert explanations[1].replacement1 == 'first'
#     assert explanations[1].replacement2 == 'second'
#     assert explanations[1].replacement3 == 'third'
#     # Check if the coordinates of the mistakes have also been found correctly:
#     doc = fitz.open(fileLoc)
#     page = doc.load_page(0)
#     assert page.get_textbox(fitz.Rect(explanations[0].X1, explanations[0].Y1, explanations[0].X2, explanations[0].Y2)) == 'a'
#     assert page.get_textbox(fitz.Rect(explanations[1].X1, explanations[1].Y1, explanations[1].X2, explanations[1].Y2)) == 'must try'