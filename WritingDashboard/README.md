# Code WritingDashboard
Please find the code of the WritingDashboard application inside this zip file. This code is divided in two parts, code for the frontend, which can be found inside the ./public and ./src folders (where . is the root of the zip-file). And the backend, for which the code can be found in the ./backend folder. Testcases for this backend can be found in the ./backend/tests folder. 
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

All ./src/components folder also need to be checked, since these files have been created from scratch. This means that the following files need to be checked:
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
Now for the code for the backend, this code can be found in the ./backend folder - as mentioned before. Just like for the frontend there is a part of the code that needs to be checked and a part that does not need to be checked.
## Code not to be checked
* ./backend/app/clickapi/_init_.py

* ./backend/app/feedback/generateFeedback/CohesionConnectives.txt

* ./backend/app/feedback/_init_.py
* ./backend/app/fileapi/_init_.py
* ./backend/app/loginapi/_init_.py
* ./backend/app/projectapi/_init_.py
* ./backend/app/scoreapi/_init_.py
* ./backend/app/usersapi/_init_.py
* ./backend/tests/_init_.py

* ./backend/tests/app_test.db

* ./backend/app/extensions.py

deze is helemaal automatisch gegenereerd
* ./backend/migrations/versions/fa0879cf3b3b.py
* ./backend/migrations/alembic.ini
* ./backend/migrations/script.py.mako
* ./backend/migrations/README
* ./backend/migrations/env.py

* ./backend/tests/feedbackModels/testFiles/
this is filled with 2 pdfs 1 docx and 1 txt to test the stuff
* ./backend/tests/feedbackModels/testFilesStructure/
also filled with pdfs and shit
* ./backend/tests/feedbackModels/testFilesStyle/
also filled with pdfs and shit
* ./backend/tests/functional/testFiles
also filled with pdfs and shit
* ./backend/tests/unit/testFiles
also filled with pdfs and shit

* ./backend/.dockerignore

* ./backend/app.py
* ./backend/backend.yaml
* ./backend/docker-entrypoint.sh (?)
* ./backend/requirements.txt
* ./backend/wsgi.py
* ./backend/Dockerfile (sort of nee)


## Code to be checked
* ./backend/app/clickapi/routes.py

* ./backend/app/feedback/generateFeedback - all except the .txt file
* ./backend/app/feedback/generateFeedback/BaseFeedback.py
* ./backend/app/feedback/generateFeedback/CohesionFeedback.py
* ./backend/app/feedback/generateFeedback/IntegrationContentFeedback.py
* ./backend/app/feedback/generateFeedback/LanguageStyleFeedback.py
* ./backend/app/feedback/generateFeedback/StructureFeedback.py

* ./backend/app/feedback/retrieveText - all 3 of them
* ./backend/app/feedback/retrieveText/convertDocxTxtToText.py
* ./backend/app/feedback/retrieveText/convertPdfToText.py
* ./backend/app/feedback/retrieveText/pageDownload.py

* ./backend/app/feedback/feedback.py
* ./backend/app/feedback/nltkDownload.py
* ./backend/app/feedback/routes.py

* ./backend/app/fileapi/convert.py
* ./backend/app/fileapi/routes.py

* ./backend/app/loginapi/routes.py

* ./backend/app/projectapi/routes.py

* ./backend/app/scoreapi/routes.py
* ./backend/app/scoreapi/scores.py

* ./backend/app/usersapi/routes.py

* ./backend/app/_init_.py (automatisch gegenereerd, maar aangepast)
* ./backend/app/database.py
* ./backend/app/generateParticipants.py
* ./backend/app/models.py

* all python files in ./backend/tests/feedbackModels/

* all python files in ./backend/tests/functional/

* all python files in ./backend/tests/unit/

* ./backend/tests/conftest.py

* ./backend/config.py (sort of)
