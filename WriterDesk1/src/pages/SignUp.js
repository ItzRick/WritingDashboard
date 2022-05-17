//import {Component, useEffect, useState} from 'react'
//import axios from "axios";
import './../css/main.css';

import {Link} from 'react-router-dom';


import Typography from '@mui/material/Typography';
import IconButton from "@mui/material/IconButton";
import testImage from '../images/placeholder_image.png'
import {Button, TextField} from "@mui/material";

function App() {

  return (
      <>
        <div className='parent'>
            <div className='div1'>
                <IconButton style={{float:'left'}}>
                    <img className='logo' src={testImage} />
                </IconButton>
                <Typography variant='h3'>Signup</Typography>
                <div className='filler2'></div>
            </div>
            <div className='div2'>
                <div className='text_boxes'>
                    <Typography>Email:</Typography>
                    <TextField id='email' label='example@mail.com' variant='outlined' />
                    <br /><br />
                    <Typography>Repeat email:</Typography>
                    <TextField id='email2' label='example@mail.com' variant='outlined' />
                    <br /><br />
                    <Typography>Password:</Typography>
                    <TextField id='password' label='Password' variant='outlined' type='password' />
                    <br /><br />
                    <Typography>Repeat password:</Typography>
                    <TextField id='password2' label='Password' variant='outlined' type='password' />
                </div>
                <br />
                {/* TODO: do we want to go to main or to login */}
                <Button variant="contained" component={Link} to='/Main'>Sign up</Button>
            </div>
            <div className='div3'>
                <br />
                <Typography>Already have an account? Log in <Link to={'/Login'}>here</Link>.</Typography>
            </div>
        </div>
    </>
  );
 }

 export default App;
