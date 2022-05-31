import './../css/main.css';

// materials 
import {
    TextField, 
    Typography,
    IconButton 
} from "@mui/material";
import logo from '../images/logo.png';
import BlueButton from "./../components/BlueButton";

// routing
import { Link, useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';

/**
 * 
 * @returns login page
 */
const Login = () => {
    //set title in parent 'base' 
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('Login');
    });

    return (
        <>
            <div className='parent'>
                <div className='div1'>
                    <IconButton style={{ float: 'left' }} component={Link} to='/LandingPage'>
                        <img className='logo' src={logo} />
                    </IconButton>
                </div>
                <div className='div2'>
                    <div className='text_boxes'>
                        <Typography>Username:</Typography>
                        <TextField id='username' label='Username' variant='outlined' />
                        <br />
                        <Typography>Password:</Typography>
                        <TextField id='password' label='Password' variant='outlined' type='password' />
                    </div>
                    <br />
                    <BlueButton pathName='/Main'>Log In</BlueButton>
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
