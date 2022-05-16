import React from 'react';
import ReactDOM from 'react-dom/client';
import './css/index.css';
import App from './pages/App.js';
import LoginSignUp from './pages/LoginSignUp';
import Login from './pages/Login';
import reportWebVitals from './reportWebVitals';
import {createTheme, ThemeProvider} from "@mui/material";
import SignUp from "./pages/SignUp";
import Home from "./pages/Home";

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

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <Home />
    </ThemeProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
