import React from 'react';
import ReactDOM from 'react-dom/client';
import './css/index.css';
import reportWebVitals from './reportWebVitals';

//pages
import App from './pages/App.js';
import Settings from './pages/Settings';
import LandingPage from './pages/LandingPage';
import SignUp from './pages/SignUp';
import Login from './pages/Login';

import Main from './pages/Main.js';
import Upload from './pages/Upload';
import Progress from './pages/Progress';
import Documents from './pages/Documents';

import FileDownload from './pages/FileDownload';
import Participants from './pages/Participants';
import Users from './pages/Users';

import FeedbackModels from './pages/FeedbackModels';


import ExamplePage from './pages/ExamplePage';


// routing
import { BrowserRouter, Route, Routes } from 'react-router-dom';

// theme
import { ThemeProvider, createTheme } from '@mui/material/styles';
const theme = createTheme({
  // dark blue: #44749D
  // light blue: #C6D4E1
  palette: {
    primary: {
      main: '#44749D',
      contrastText: "#ffffff", // white
    },
    secondary: {
      main: '#C6D4E1',
      contrastText: '#000000', // black
    },
    navigation: {
      main: '#44749D',
      text: '#44749D',
      contrastText: "#44749D", // white
    },
    navigation1: {
      main: '#C6D4E1',
      contrastText: "#ffffff", // white
    },
    error: {
      main: '#ff0015', // red
    },

    //fontFamily: font
  },

  //overriding themes
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
});
//<Route name='LandingPage' path='pages/LandingPage' element={<LandingPage />} />
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<App />}>
            <Route name='Settings' path='Settings' element={<Settings />} />
            <Route name='LandingPage' path='LandingPage' element={<LandingPage />} />
            <Route name='Login' path='Login' element={<Login />} />
            <Route name='SignUp' path='SignUp' element={<SignUp />} />

            <Route name='Main' path='Main' element={<Main />} />
            <Route name='Upload' path='Upload' element={<Upload />} />
            <Route name='Progress' path='Progress' element={<Progress />} />
            <Route name='Documents' path='Documents' element={<Documents />} />

            <Route name='FileDownload' path='FileDownload' element={<FileDownload />} />
            <Route name='Participants' path='Participants' element={<Participants />} />
            <Route name='FeedbackModels' path='FeedbackModels' element={<FeedbackModels />} />

            <Route name='Users' path='Users' element={<Users />} />
            
            <Route path='/' element={<LandingPage />} />

            <Route name='ExamplePage' path='ExamplePage' element={<ExamplePage />} />
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
