import './../css/main.css';

// materials
import {
    Typography,
    IconButton,
    TextField
} from "@mui/material";
import logo from '../images/logo.png';
import BlueButton from "./../components/BlueButton";

// routing
import { Link, useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';

/**
 * 
 * @returns signUp page
 */
const SignUp = () => {
    //set title in parent 'base' 
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('Sign Up');
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
                    <BlueButton pathName='/Login'>Sign Up</BlueButton>
                </div>
                <div className='div3'>
                    <br />
                    <Typography>Already have an account? Log in <Link to={'/Login'}>here</Link>.</Typography>
                </div>
            </div>
        </>
    );
}

export default SignUp;
