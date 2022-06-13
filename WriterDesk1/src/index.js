import React from 'react';
import ReactDOM from 'react-dom/client';
import './css/index.css';
import reportWebVitals from './reportWebVitals';

// routing
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { history } from './helpers/history'; // used for redirects

// authentication
import { ProtectedR, ProtectedA } from './services/ProtectedRoutes';

// theme and style
import { ThemeProvider, createTheme } from '@mui/material/styles';

//    PAGES
// base pages
import Base from './components/Base.js'
import BaseOut from './components/BaseOut.js';
import Projects from './pages/Projects';

// pages outside login
import Settings from './pages/Settings';
import LandingPage from './pages/LandingPage';
import SignUp from './pages/SignUp';
import Login from './pages/Login';
// pages for all users
import Main from './pages/Main.js';
import Upload from './pages/Upload';
import Progress from './pages/Progress';
import Documents from './pages/Documents';
import Document from './pages/Document';
// pages for researchers (and admin)
import Participants from './pages/Participants';
import FeedbackModels from './pages/FeedbackModels';
// page just for admin
import Users from './pages/Users';


//testing page, to be removed later
import TestingPage from './pages/TestingPage';

// theme and style
const ThemeColors = {
  darkBlue: '#44749D',
  lightBlue: '#C6D4E1',
  lightGray: '#EBE7E0',
  darkGray: '#BDB8AD',
  white: '#ffffff',
  black: '#000000',
  red: '#ff0015',
};

const theme = createTheme({
  //main color palatte
  palette: {
    // colors for the drawer
    drawer: {
      burger: ThemeColors.darkBlue,
      icon: ThemeColors.darkBlue,
      text: ThemeColors.darkBlue,
      background: ThemeColors.lightBlue,
      divider: ThemeColors.darkGray,
    },
    // colors for the appbar
    appBar: {
      background: ThemeColors.darkBlue,
      text: ThemeColors.white,
      icon: ThemeColors.white,
    },
    // colors for the drawer in logged out version
    drawerOut: {
      background: ThemeColors.darkBlue,
    },

    button: {
      main: ThemeColors.darkBlue,
      text: ThemeColors.white
	  },
    buttonWarning: {
      main: ThemeColors.red,
      text: ThemeColors.white
    },
    primary: {
      main: ThemeColors.darkBlue,
    },
    secondary: {
      main: ThemeColors.lightBlue,
    }

    //fontFamily: font
  },
});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(     
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      {/* Router encapsules the application */}
      <BrowserRouter history={history}>
        <Routes>
          {/* public part of the router, accessible for public */}
          <Route path='/' element={<BaseOut />}>
            <Route name='LandingPage' path='LandingPage' element={<LandingPage />} />
            <Route name='Login' path='Login' element={<Login />} />
            <Route name='SignUp' path='SignUp' element={<SignUp />} />
            <Route path='/' element={<LandingPage />} />
          </Route>
          {/* TODO: add authentication */}
          {/* Private part of the router, requires authentication */}
          <Route path='/' element={<Base />}>
            {/* For all users */}
            <Route name='Settings' path='Settings' element={<Settings />} />

            <Route name='Main' path='Main' element={<Main />} />
            <Route name='Upload' path='Upload' element={<Upload />} />
            <Route name='Progress' path='Progress' element={<Progress />} />
            <Route name='Documents' path='Documents' element={<Documents />} />
            <Route name='Document' path='Document' element={<Document />} />

             {/* For researcher users */}
            <Route element={<ProtectedR/>}>
              <Route name='Participants' path='Participants' element={<Participants />} />
              <Route name='Projects' path='Projects' element={<Projects />} />
              <Route name='FeedbackModels' path='FeedbackModels' element={<FeedbackModels />} />
            </Route>

            {/* For admin users */}
            <Route element={<ProtectedA/>}>
              <Route name='Users' path='Users' element={<Users />} />
            </Route>
            <Route path='/' element={<Main />} />


            {/* Testing Page, for checking out new stuff */}
            <Route name='TestingPage' path='TestingPage' element={<TestingPage />} />
          </Route>


        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
