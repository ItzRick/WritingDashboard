import './../css/main.css';

// materials 
import {
    TextField, 
    Typography,
    IconButton,
    Button
} from "@mui/material";
import logo from '../images/logo.png'

// routing
import { Link,useOutletContext, useNavigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react';

// Login request setup
import { AuthenticationService } from '../services/authenticationService';

/**
 * Request login to server based on form on page
 * 
 * 
 * @returns login page
 */
const Login = () => {
    //set title in parent 'base' 
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('Login');
    });

    // Set username from textfield
    const [username, setUsername] = useState("");

    // Set password from textfield
    const [password, setPassword] = useState("");

    // Change page using formError when we find an error
    const [formError, setFormError] = useState(false);

    let navigate = useNavigate();

     /**
     * Do POST request containing username and password variable, go to main page when login succeeds 
     */
    const handleClick = () => {
        AuthenticationService.login(username, password).then(() => {
            navigate("../Main", { replace: true });
        }).catch( error => {
            setFormError(true);
        });
    }

    /**
     * Try to login when pressing the enter key
     */
    const handleKeyPress = (event) => {
      if(event.key === 'Enter'){
        handleClick();
      }
    }
    
    return (
        <>
            <div className='parent'>
                <div className='div1'>
                    <IconButton style={{ float: 'left' }} component={Link} to='/'>
                        <img className='logo' src={logo} alt='' />
                    </IconButton>
                </div>
                <div className='div2'>
                    <div className='text_boxes'>
                        <Typography>Username:</Typography>
                        <TextField id='username' label='Username' variant='outlined' value={username} onChange={(e) => setUsername(e.target.value)} />
                        <br />
                        <Typography>Password:</Typography>
                        <TextField id='password' label='Password' variant='outlined' type='password' onKeyPress={(e) => handleKeyPress(e)} value={password} onChange={(e) => setPassword(e.target.value)}/>
                    </div>
                    <br />
                    {formError && <Typography color="red">Invalid username and/or password</Typography>}
                    <Button id='login' variant="contained" sx={{bgcolor: 'button.main', color: 'button.text'}} onClick={handleClick}>Log in</Button>
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
