//import {Component, useEffect, useState} from 'react'
//import axios from "axios";
import './../css/main.css';
import Base from './../components/Base.js';


import Typography from '@mui/material/Typography';
import IconButton from "@mui/material/IconButton";
import testImage from '../images/placeholder_image.png'
import {Button, TextField} from "@mui/material";

function App() {

  return (
    <Base pageName='' enableNav={false} researcher={true} admin={true}>
        <div className='parent'>
            <div className='div1'>
                <IconButton style={{float:'left'}}>
                    <img className='logo' src={testImage} />
                </IconButton>
                <Typography variant='h3'>Login</Typography>
                <div className='filler2'></div>
            </div>
            <div className='div2'>
                <div className='text_boxes'>
                    <p>Username:</p>
                    <TextField id='username' label='Username' variant='outlined' />
                    <br />
                    <p>Password:</p>
                    <TextField id='password' label='Password' variant='outlined' />
                </div>
                <br />
                <Button variant="contained">Log in</Button>
            </div>
            <div className='div3'>
                <br />
                <Typography>Don't have an account yet? Sign up <a href='google.com'>here</a>.</Typography>
                <br />
                Note: the TU/e mail is the username of TU/e students.
            </div>
        </div>
    </Base>
  );
 }

 export default App;