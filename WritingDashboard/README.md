# Code WritingDashboard
Please find the code of the WritingDashboard application inside this zip file. This code is divided in two parts, code for the frontend, which can be found inside the ./public and ./src folders (where . is the root of the zip-file). And the backend, for which the code can be found in the ./backend folder. Testcases for this backend can be found in the ./backend/tests folder. 

Within the root directory there are some files located as well. Out of these, there are some files that do not need to be checked. Some of these are ignore files, the .pem files store a key and certificate, the others are automatically generated. The following files do not need to be checked:
* .dockerignore
* .gcloudignore
* .gitignore
* app.yaml
* cert.pem
* dispatch.yaml
* key.pem
* requirements.txt

Then there are also some files that do need to be checked, like the Dockerfiles. The others have been edited enough such that they should be checked as well. These files should be checked:
* Dockerfile
* docker-compose.yml
* nginx.conf
* package.json

Lastly, the root directory also contains this file README.db which should be checked as well.
# The code 
## The frontend code
As said before, the code for the frontend can be found inside the ./src and ./public folder. Part of this code needs to be checked and part of this code does not need to be checked. 
## Code not to be checked
Firstly, everything inside ./public does not need to be checked, since this folder only contains a favicon, general information about the website, such as the title and the description of the website. Furthermore, this folder contains the pdf.worker.js and pdf.worker.js.map files, which have not been created by the team during this project. The manifest.json file inside this folder has also been automatically generated. 
Besides that, everything in the ./src/images folder does not need to be checked either. This folder only contains some images which we use on the website, like our logo for example.

Inside the .src folder there are also some files, which do not need to be checked as these have been automatically generated and only very slightly changed. This holds for the following files: 
* ./src/App.test.js, 
* ./src/reportWebVitals.js, 
* /src/setupProxy, and 
* ./src/setupTests.js

All files inside the ./src/css folder have been newly created, but do not need to be checked, as these files are not part of the code. So this holds for the following files:
* ./src/css/App.css, 
* ./src/css/Document.css, 
* ./src/css/LoginSignUp.css, 
* ./src/css/Navigation.css, 
* ./src/css/Progress.css, 
* ./src/css/SignUp.css, and 
* ./src/css/index.css, 
* ./src/css/main.css, and 
* ./src/css/roledialog.css, 
* ./src/css/styles.css
## Code to be checked
The other files inside the ./src folder are changed in such a manner that they need to be checked. These are either files which are automatically generated/ taken from other sources with significant changes or have been created by the team of WritingDashboard. 

So the ./src/index.js file is the first file for which this holds, which has been automatically generated but changed significantly. 

All ./src/components folder also need to be checked, since most of these files have been created from scratch. The first file AlertDialog.js is quite related to the react material UI library. Base.js, BaseOut.js and ShowPDF.js have been automatically generated, but changed so significantly that they need to be changed either way. The other files were actually made from scratch and should therefore be checked. This means that the following files need to be checked:
* ./src/components/AlertDialog.js
* ./src/components/Base.js
* ./src/components/BaseOut.js
* ./src/components/BlueButton.js
* ./src/components/NavigationLink.js
* ./src/components/ProgressVisualization.js
* ./src/components/RoleDialog.js
* ./src/components/UploadSingleFile.js
* ./src/components/ShowPDF.js
<!---
The first file for which this holds is ./src/components/AlertDialog.js, although this file is quite related to the Dialog example from the react material UI library. The next file, ./src/components/Base.js has been automatically generated, but then changed so significantly that it needs to be checked either way. This also holds for ./src/components/BaseOut.js, which is practically the same as this earlier mentioned base page. The ./src/components/BlueButton.js, ./src/components/NavigationLink.js, ./src/components/ProgressVisualization.js, ./src/components/RoleDialog.js and ./src/components/UploadSingleFile.js files has been created from scratch and therefore need to be checked. The ./src/components/ShowPDF.js file has also been changed significantly, but elements of this file have been taken from different sources. 
-->

All files inside the .src/helpers directory are created from scratch and will therefore need to be checked. So, the following files need to be checked:
* ./src/helpers/auth-header.js, and 
* ./src/helpers/history.js

All files inside ./src/pages are newly created by the WritingDashboard team and will therefore need to be checked, although all files are created from a single template. So this holds for the files files:
* ./src/pages/Document.js, 
* ./src/pages/Documents.js, 
* ./src/pages/FeedbackModels.js, 
* ./src/pages/LandingPage.js, 
* ./src/pages/Login.js, 
* ./src/pages/Main.js, 
* ./src/pages/ParticipantDocuments.js, 
* ./src/pages/Participants.js, 
* ./src/pages/Progress.js, 
* ./src/pages/Projects.js, 
* ./src/pages/Settings.js,
* ./src/pages/SignUp.js,
* ./src/pages/Upload.js, and
* ./src/pages/User.js

These files all need to be checked. 

The files inside the ./src/services folder also need to be checked, as they either have been created from a template or newly created. So, the files:
* ./src/services/authenticationService.js, has been created from scratch,
* ./src/services/ProtectedRoutes.js, has been created from a template, and 
* ./src/services/TrackingWrapper.js, has also been created from a template.
* 
## The backend code
The backend code can be found in the ./backend folder, as mentioned before. Just like for the frontend there is a part of the code that should be checked and a part that doesn't need to be checked.
## Code not to be checked
All init files - besides the main one in ./backend/app - do not need to be checked, since they are generated automatically and at most slightly adjusted. These files are:
* ./backend/app/clickapi/_init_.py
* ./backend/app/feedback/_init_.py
* ./backend/app/fileapi/_init_.py
* ./backend/app/loginapi/_init_.py
* ./backend/app/projectapi/_init_.py
* ./backend/app/scoreapi/_init_.py
* ./backend/app/usersapi/_init_.py
* ./backend/tests/_init_.py

The .txt file ./backend/app/feedback/generateFeedback/CohesionConnectives.txt does not need to be checked either. This file contains a list filled with connectives. This list is used to go over when checking if a word is a connective. This list is taken from the TAACO documentation.

The file ./backend/app/extensions.py is an automatically generated file and does not need to be checked.

The .backend/migrations folder consists entirely out of automatically generated files. Thus these do not need to be checket either. These are the following files: 
* ./backend/migrations/versions/fa0879cf3b3b.py
* ./backend/migrations/README
* ./backend/migrations/alembic.ini
* ./backend/migrations/env.py
* ./backend/migrations/script.py.mako

The following files are all files which were made with the only intention of using these with testing of code. Thus, these are all example documents with which the test code checks the code. These are all files within ./backend/tests/feedbackModels/testFiles, ./backend/tests/feedbackModels/testFilesStructure, ./backend/tests/feedbackModels/testFilesStyle, ./backend/tests/functional/testFiles  and ./backend/tests/unit/testFiles and besides that a test database file ./backend/tests/app_test.db. 

Within the ./backend file there most files are autogenerated as well. The following files do not need to be checked:
* ./backend/.dockerignore
* ./backend/app.py
* ./backend/backend.yaml
* ./backend/requirements.txt
* ./backend/wsgi.py
* ./backend/Dockerfile 
* ./backend/docker-entrypoint.sh
## Code to be checked
All routes.py files need to be checked, since these are all made from scratch. These files are:
* ./backend/app/clickapi/routes.py
* ./backend/app/feedback/routes.py
* ./backend/app/fileapi/routes.py
* ./backend/app/loginapi/routes.py
* ./backend/app/projectapi/routes.py
* ./backend/app/scoreapi/routes.py
* ./backend/app/usersapi/routes.py

The files ./backend/config.py and ./backend/app/_init_.py are automatically generated but have been adjusted and should thus be checked.

All files within ./backend/app/feedback/generateFeedback is made from scratch. This means that all files need to be checked (except for the aforementioned .txt file). These files are:
* ./backend/app/feedback/generateFeedback/BaseFeedback.py
* ./backend/app/feedback/generateFeedback/CohesionFeedback.py
* ./backend/app/feedback/generateFeedback/IntegrationContentFeedback.py
* ./backend/app/feedback/generateFeedback/LanguageStyleFeedback.py
* ./backend/app/feedback/generateFeedback/StructureFeedback.py

All files within ./backend/app/feedback/retrieveText is made from scratch. This means that all files need to be checked. These files are:
* ./backend/app/feedback/retrieveText/convertDocxTxtToText.py
* ./backend/app/feedback/retrieveText/convertPdfToText.py
* ./backend/app/feedback/retrieveText/pageDownload.py

The files ./backend/app/feedback/feedback.py and ./backend/app/feedback/nltkDownload.py are made from scratch as well and should be checked.

All python files within .backend/tests/feedbackModels, .backend/tests/functional and .backend/tests/unit are made from scratch and should be checked as well as .backend/tests/conftest.py. These files are all test files. To run these, you first need to install the requirements by typing "python -m pip install -r backend/requirements.txt" into your ternimal and running this. After all the requirements are installed you can run the test cases by typing "python -m pytest --cov=app" into your terminal and running this will run the test cases. This also looks at the coverage of the test cases.

All files in .cypress\e2e are made from scratch and should be checked. These files are cypress test files. To run these files you should first open a command prompt at the root of the project an then run the following commands: `pip install virtualenv`, `cd backend` and then `py -m venv env`. Now return to the root of the project and run 'backend\\env\\Scripts\\activate'. The virtual environment should now be opened. After this run 'npm install' and 'pip install -r requirements.txt'. When both are complete you can enter the command 'npx cypress open'. A menu should pop up, there you select e2e testing, then you click start e2e testing in chrome (or another browser if desired) and then you can click one of the displayed tests to run them.

The following files are made from scratch and should be checked:
* ./backend/app/fileapi/convert.py
* ./backend/app/scoreapi/scores.py
* ./backend/app/database.py
* ./backend/app/generateParticipants.py
* ./backend/app/models.py

Convert.py converts txt and docx documents to pdf documents and removes files that have been converted to pdf from the folder the files have been converted to, scores.py stores all the scores and explanations of the writing skills and makes retrieving them possible as well, lastly generateParticipants.py makes participants. Database.py manages the database, storing and getting information in and from it. 
Then models.py contains the database models. These reflect to the tables of the database and makes the interaction from the backend to the database a lot more organized and easier.
