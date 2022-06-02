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
import { Link, useOutletContext, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';

// Signup request setup
import axios from 'axios';
const BASE_URL = "https://localhost:5000/loginapi";
const NAVIGATE_TO_URL = "../../Login"

const USERNAME_END = "tue.nl";
const PASSWORD_LENGTH = 8;

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

    const navigate = useNavigate();

    // Check if username input is valid
    const checkUsername = () => {
        if(username === "") {
            return "";
        } else if(!username.endsWith(USERNAME_END)) {
            return "Username is not a TUe email-address";
        }
        return "";
    }

    // Check if repeated username input is valid
    const confirmUsername = () => {
        if(username !== "" && username !== usernameConfirm) {
            return "Does not match Email";
        }
        return "";
    }

    // Check if password input is valid
    const checkPassword = () => {
        if(password === "") {
            return "";
        } else if(password.length < PASSWORD_LENGTH) {
            return "Password needs to contain at least 8 characters";
        } else if((password.match(/[a-z]/g) || []).length < 1) {
            return "Password needs to contain at least 1 lowercase letter";
        } else if((password.match(/[A-Z]/g) || []).length < 1) {
            return "Password needs to contain at least 1 uppercase letter";
        } else if((password.match(/[0-9]/g) || []).length < 1) {
            return "Password needs to contain at least 1 number";
        }
        return "";
    }

    // Check if repeated password input is valid
    const confirmPassword = () => {
        if(password !== "" && password !== passwordConfirm) {
            return "Does not match password";
        }
        return "";
    }

    // Do POST request containing username and password variable, recieve status of response
    const handleClick = () => {
        // Check if input is valid
        if (username === "" || password === "") {
            setFormError("One or more fields are empty!");
            return;
        }
        if (checkUsername() !== "" || confirmUsername() !== "" || checkPassword() !== "" || confirmPassword() !== "") {
            setFormError("One or more fields are not complete!");
            return;
        }

        // If input is valid, do post request
        const data = {
            "username": username,
            "password": password,
        }
        axios.post(`${BASE_URL}/signup`, data).then(response =>{
            // Post request is successful, user is registered
            // Loads login page
            navigate(NAVIGATE_TO_URL, {replace: true});
        }).catch(error =>{
            // Post request failed, user is not created
            console.error("Something went wrong:", error.response.data);
            setFormError(error.response.data);
        });
    }

    // Set username from textfield
    const [username, setUsername] = useState("");

    // Set username from textfield
    const [usernameConfirm, setUsernameConfirm] = useState("");

    // Set password from textfield
    const [password, setPassword] = useState("");

    // Set password from textfield
    const [passwordConfirm, setPasswordConfirm] = useState("");

    // Change page using formError when we find an error
    const [formError, setFormError] = useState("");

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
                        <TextField id='email' label='example@mail.com' variant='outlined' 
                            value={username} onChange={(e) => {setUsername(e.target.value); setFormError("")}}
                            error={checkUsername() !== ""} helperText={checkUsername() !== "" ? checkUsername() : ""}
                        />
                        <br /><br />
                        <Typography>Repeat email:</Typography>
                        <TextField id='email2' label='example@mail.com' variant='outlined' 
                            value={usernameConfirm} onChange={(e) => {setUsernameConfirm(e.target.value); setFormError("")}} 
                            error={confirmUsername() !== ""} helperText={confirmUsername() !== "" ? confirmUsername() : ""}
                        />
                        <br /><br />
                        <Typography>Password:</Typography>
                        <TextField id='password' label='Password' variant='outlined' type='password' 
                            value={password} onChange={(e) => {setPassword(e.target.value); setFormError("")}} 
                            error={checkPassword() !== ""} helperText={checkPassword() !== "" ? checkPassword() : ""}
                        />
                        <br /><br />
                        <Typography>Repeat password:</Typography>
                        <TextField id='password2' label='Password' variant='outlined' type='password' 
                            value={passwordConfirm} onChange={(e) => {setPasswordConfirm(e.target.value); setFormError("")}} 
                            error={confirmPassword() !== ""} helperText={confirmPassword() !== "" ? confirmPassword() : ""}
                        />
                    </div>
                    <br />
                    {formError !== "" && <Typography color="red">{formError}</Typography>}
                    <br />
                    <BlueButton onClick={handleClick}>Sign Up</BlueButton>
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
