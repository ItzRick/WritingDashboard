# Code WritingDashboard
Please find the code of the WritingDashboard application inside this zip file. This code is divided in two parts, code for the frontend, which can be found inside the ./public and ./src folders (where . is the root of the zip-file). And the backend, for which the code can be found in the ./backend folder. Testcases for this backend can be found in the ./backend/tests folder. 
# The code 
## The frontend code
As said before, the code for the frontend can be found inside the ./src and ./public folder. Part of this code needs to be checked and part of this code does not need to be checked. 
## Code not to be checked
Firstly, everything inside ./public does not need to be checked, since this folder only contains a favicon, general information about the website, such as the title and the description of the website. Furthermore, this folder contains the pdf.worker.js and pdf.worker.js.map files, which have not been created by the team during this project. The manifest.json file inside this folder has also been automatically generated. 

Inside the .src folder there are also some files, which do not need to be checked as these have been automatically generated and only very slightly changed. This holds for the ./src/App.test.js, ./src/reportWebVitals.js, /src/setupProxy and ./src/setupTests.js files. 

All files inside the ./src/css folder have been newly created, but do not need to be checked, as these files are not part of the code. So this holds for the ./src/css/App.css, ./src/css/Document.css, ./src/css/index.css, ./src/css/Navigation.css, ./src/css/Progress.css, ./src/css/roledialog.css, ./src/css/Signup.css and ./src/css/styles.css files.
## Code to be checked
The other files inside the ./src folder are changed in such a manner that they need to be checked. These are either files which are automatically generated/ taken from other sources with significant changes or have been created by the team of WritingDashboard. 

So the ./src/index.js file is the first file for which this holds, which has been automatically generated but changed significantly. 

All ./src/components folder also need to be checked, since these files have been created from scratch. The first file for which this holds is ./src/components/AlertDialog.js, although this file is quite related to the Dialog example from the react material UI library. The next file, ./src/components/Base.js has been automatically generated, but then changed so significantly that it needs to be checked either way. This also holds for ./src/components/BaseOut.js, which is practically the same as this earlier mentioned base page. The ./src/components/BlueButton.js, ./src/components/NavigationLink.js, ./src/components/ProgressVisualization.js, ./src/components/RoleDialog.js and ./src/components/UploadSingleFile.js files has been created from scratch and therefore need to be checked. The ./src/components/ShowPDF.js file has also been changed significantly, but elements of this file have been taken from different sources. 

All files inside the .src/helpers directory are created from scratch and will therefore need to be checked. So, the ./src/helpers/auth-header.js and ./src/helpers/history.js files need to be checked. 

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
