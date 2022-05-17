import React from 'react';
import ReactDOM from 'react-dom/client';
import './css/index.css';
import reportWebVitals from './reportWebVitals';

// routing
import { BrowserRouter, Route, Routes } from 'react-router-dom';

//theme and style
import { ThemeProvider, createTheme } from '@mui/material/styles';

//pages
import Base from './components/Base.js'
import BaseOut from './components/BaseOut.js';

import Settings from './pages/Settings';
import LandingPage from './pages/LandingPage';
import SignUp from './pages/SignUp';
import Login from './pages/Login';

import Main from './pages/Main.js';
import Upload from './pages/Upload';
import Progress from './pages/Progress';
import Documents from './pages/Documents';

import Participants from './pages/Participants';
import Users from './pages/Users';

import FeedbackModels from './pages/FeedbackModels';
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
  //
  palette: {
    drawer: {
      burger: ThemeColors.darkBlue,
      icon: ThemeColors.darkBlue,
      text: ThemeColors.darkBlue,
      background: ThemeColors.lightBlue,
      divider: ThemeColors.darkGray,
    },
    appBar: {
      background: ThemeColors.darkBlue,
      text: ThemeColors.white,
      icon: ThemeColors.white,
    },
    drawerOut: {
      background: ThemeColors.darkBlue,
    },

    //fontFamily: font
  },

  //overriding themes
  /*
  components: {
    MuiDrawer: {
      styleOverrides: {
        paper: {
          background: '#C6D4E1',
        },
        colorPrimary: {
          background: '#44749D',
          color: 'red'
        }
      }
    }
  }
  */
});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      {/* Router encapsules the application */}
      <BrowserRouter>
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
            <Route name='Settings' path='Settings' element={<Settings />} />

            <Route name='Main' path='Main' element={<Main />} />
            <Route name='Upload' path='Upload' element={<Upload />} />
            <Route name='Progress' path='Progress' element={<Progress />} />
            <Route name='Documents' path='Documents' element={<Documents />} />

            <Route name='Participants' path='Participants' element={<Participants />} />
            <Route name='FeedbackModels' path='FeedbackModels' element={<FeedbackModels />} />

            <Route name='Users' path='Users' element={<Users />} />

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
