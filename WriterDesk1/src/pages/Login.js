import './../css/main.css';

// materials 
import { 
    Button, 
    TextField, 
    Typography,
    IconButton 
} from "@mui/material";
import testImage from '../images/placeholder_image.png'

// routing
import { Link } from 'react-router-dom';
import React, { useState } from 'react';


/**
 * 
 * @returns login page
 */
const Login = () => {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleClick = () => {
        let url = "http://localhost:5000/token"

        fetch(url,{
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "username": username,
                "password": password,
            }),
        }).then( res => res.json())
        .then(data =>{
            localStorage.setItem('access_token', data.access_token);

            if (localStorage.getItem("access_token") !== null && localStorage.getItem("access_token")!=="undefined") {
                console.log("Inloggen gelukt!")
              }else{
                  alert(data.error);
              }
        })
        .catch(error => {
            console.error("Error:",error);
        });
    }
    
    return (
        <>
            <div className='parent'>
                <div className='div1'>
                    <IconButton style={{ float: 'left' }} component={Link} to='/LandingPage'>
                        <img className='logo' src={testImage} />
                    </IconButton>
                    <Typography variant='h3'>Login</Typography>
                    <div className='filler2'></div>
                </div>
                <div className='div2'>
                    <div className='text_boxes'>
                        <Typography>Username:</Typography>
                        <TextField id='username' label='Username' variant='outlined' value={username} onChange={(e) => setUsername(e.target.value)} />
                        <br />
                        <Typography>Password:</Typography>
                        <TextField id='password' label='Password' variant='outlined' type='password' value={password} onChange={(e) => setPassword(e.target.value)}/>
                    </div>
                    <br />
                    <Button variant="contained" sx={{bgcolor: 'button.main', color: 'button.text'}} onClick={handleClick}>Log in</Button>
                </div>
                <div className='div3'>
                    <br />
                    <Typography>Don't have an account yet? Sign up <Link to={'/SignUp'}>here</Link>.</Typography>
                    <br />
                    Note: the TU/e mail is the username of TU/e students.
                </div>
            </div>
        </>
    );
}

export default Login;
