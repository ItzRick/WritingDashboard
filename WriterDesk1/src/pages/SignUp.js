import './../css/main.css';
import './../css/SignUp.css';

// materials
import {
    Typography,
    IconButton,
    TextField,
    Checkbox,
    Button
} from "@mui/material";
import logo from '../images/logo.png';
import BlueButton from "./../components/BlueButton";
import AlertDialog from "../components/AlertDialog";

// routing
import { Link, useOutletContext, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';

// Signup request setup
import axios from 'axios';
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

    // whether or not signup was succesful.
    const [loginAllowed, setLoginAllowed] = useState(false)

    // whether or not the information about the user data is shown.
    const [showUserDataPopup, setShowUserDataPopup] = useState(false)
    // whether or not the information about the user data is shown.
    const [showNeceDataPopup, setShowNeceDataPopup] = useState(false)

    /** 
     * Check if username input is valid.
     * @returns helper text for username textfield
     */
    const checkUsername = () => {
        if(username === "") {
            return "";
        } else if(!username.endsWith(USERNAME_END)) {
            return "Must be a TU/e email-address";
        }
        return "";
    }

    /**
     * Check if repeated username input is valid.
     * @returns helper text for second username textfield
     */
    const confirmUsername = () => {
        if(username !== "" && username !== usernameConfirm) {
            return "Must match Email";
        }
        return "";
    }

    /** 
     * Check if password input is valid.
     * According to URC 1.2-1.5, a valid password has at least 8 characters,
     * with at least 1 lowercase character, uppercase character and number.
     * @returns helper text for password textfield
     */
    const checkPassword = () => {
        if(password === "") {
            return "";
        } else if(password.length < PASSWORD_LENGTH) {
            return "Must contain at least 8 characters";
        } else if((password.match(/[a-z]/g) || []).length < 1) {
            return "Must contain at least 1 lowercase letter";
        } else if((password.match(/[A-Z]/g) || []).length < 1) {
            return "Must contain at least 1 uppercase letter";
        } else if((password.match(/[0-9]/g) || []).length < 1) {
            return "Must contain at least 1 number";
        }
        return "";
    }

    /** 
     * Check if repeated password input is valid.
     * @returns helper text for second password textfield
     */
    const confirmPassword = () => {
        if(password !== "" && password !== passwordConfirm) {
            return "Must match Password";
        }
        return "";
    }

    /**
     * Do POST request containing username and password variable, recieve status of response.
     */
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
        // check if the user accepted the necessary data agreement
        if (!acceptNeceData) {
            setFormError('You must allow the storage and execution of necessary application data!')
            return;
        }

        // If input is valid, do post request
        const data = {
            "username": username,
            "password": password,
            "trackable": acceptUserData,
        }
        const headers = {
            "Content-Type": "application/json"
        }
        axios.post(`https://localhost:5000/loginapi/signup`, data, headers).then(response =>{
            // Post request is successful, user is registered
            // Loads login page
            setLoginAllowed(true);           
        }).catch(error =>{
            // Post request failed, user is not created
            console.error("Something went wrong:", error.response.data);
            setFormError(error.response.data);
        });
    }

    let navigate = useNavigate();

    /** Navigates to the login page */
    const navig = () => {
        setLoginAllowed(false)
        navigate(NAVIGATE_TO_URL, { replace: true });
    }

    // Set username from textfield
    const [username, setUsername] = useState("");

    // Set repeated username from textfield
    const [usernameConfirm, setUsernameConfirm] = useState("");

    // Set password from textfield
    const [password, setPassword] = useState("");

    // Set repeated password from textfield
    const [passwordConfirm, setPasswordConfirm] = useState("");

    // Change page using formError when we find an error
    const [formError, setFormError] = useState("");

    // Set the acceptance of collecting user data from checkbox
    const [acceptUserData, setAcceptUserData] = useState(true);
    // Set the acceptance of collecting necessary data from checkbox
    const [acceptNeceData, setAcceptNeceData] = useState(false);

    return (
        <>
            <div className='parent'>
                <div className='div1'>
                    <IconButton style={{ float: 'left' }} component={Link} to='/'>
                        <img className='logo' src={logo} alt=''/>
                    </IconButton>
                </div>
                <div className='div2'>
                    <div className='text_boxes'>
                        <Typography>Email:</Typography>
                        <TextField id='email' label='example@tue.nl' variant='outlined' 
                            value={username} onChange={(e) => {setUsername(e.target.value); setFormError("")}}
                            error={checkUsername() !== ""} helperText={checkUsername() !== "" ? checkUsername() : " "}
                            fullWidth
                        />
                        <Typography>Repeat email:</Typography>
                        <TextField id='email2' label='example@tue.nl' variant='outlined' 
                            value={usernameConfirm} onChange={(e) => {setUsernameConfirm(e.target.value); setFormError("")}} 
                            error={confirmUsername() !== ""} helperText={confirmUsername() !== "" ? confirmUsername() : " "}
                            fullWidth
                        />
                        <Typography>Password:</Typography>
                        <TextField id='password' label='Password' variant='outlined' type='password' 
                            value={password} onChange={(e) => {setPassword(e.target.value); setFormError("")}} 
                            error={checkPassword() !== ""} helperText={checkPassword() !== "" ? checkPassword() : " "}
                            fullWidth
                        />
                        <Typography>Repeat password:</Typography>
                        <TextField id='password2' label='Password' variant='outlined' type='password' 
                            value={passwordConfirm} onChange={(e) => {setPasswordConfirm(e.target.value); setFormError("")}} 
                            error={confirmPassword() !== ""} helperText={confirmPassword() !== "" ? confirmPassword() : " "}
                            fullWidth
                        />
                        <div style={{display: 'flex', alignSelf: 'flex-end', verticalAlign: 'middle'}}>
                            <Checkbox sx={{alignSelf: 'center'}} onChange={(e) => {setAcceptUserData(!e.target.checked)}} />
                            <Typography sx={{alignSelf: 'center', alignContent:'inline'}}>
                                I do not allow the collection of my <button className='userDataLinkPopup' onClick={() => {setShowUserDataPopup(true)}} >user data</button>.
                            </Typography>
                            {showUserDataPopup && <AlertDialog title = "User data" 
                                text = "The data conditions allow the application to record user data. The user data includes the URL of the page, the location on the screen, and the timestamp of each click from the user.  The user data is only used to improve the automatic feedback generated within the application. If the purpose of the data changes, the application will ask the user again for permission to save their user data. This data does not include necessary sign-up information, such as the university email address and the password, since that is saved to ensure the functionalities of the application. The sign-up information is not used for any other purposes than logging into the application. The application is still fully available when refusing the data conditions. If the user refuses permission, no user data will be recorded of this user until the moment that they accept the data settings in the future. If the user accepts the permission at first but later revokes the permission, their recorded user data is deleted and no user data will be recorded of this user, until the moment that they accept the data settings in the future. Users can retrieve the recorded user data so far at any time. Users can ask questions regarding their data by sending a mail to i.l.h.rutten@student.tue.nl; a response will be provided within a month."
                                buttonAgree={<Button onClick={() => {setShowUserDataPopup(false)}}>I understand</Button>}
                            />}
                        </div>
                        <div style={{display: 'flex', alignSelf: 'flex-end', verticalAlign: 'middle'}}>
                            <Checkbox sx={{alignSelf: 'center'}} onChange={(e) => {setAcceptNeceData(e.target.checked)}} />
                            <Typography sx={{alignSelf: 'center', alignContent:'inline'}}>
                            I allow the storage and execution of <button className='userDataLinkPopup' onClick={() => {setShowNeceDataPopup(true)}} >necessary application data</button>.
                            </Typography>
                            {showNeceDataPopup && <AlertDialog title = "Storing necessary data" 
                                text = "The application needs to store certain data to allow the user to use the application. If the user makes an account, the application will store their sign up information in the database. This data includes their username and hashed password. If the user uploads a document, the application will store the document and its inserted meta data in the database. When the document has been uploaded, the application will generate feedback based on that document, which will also be stored in the database. The user can delete uploaded files and their corresponding feedback on the Documents page. The user can change their username and password in the Settings page. Finally, the user can delete their account, including all sign up information and documents, on the Settings page."
                                buttonAgree={<Button onClick={() => {setShowNeceDataPopup(false)}}>I understand</Button>}
                            />}
                        </div>
                    </div>
                    <br />
                    {formError !== "" && <Typography color="red">{formError}</Typography>}
                    {formError !== "" && <br />}

                    <BlueButton idStr='signButton' onClick={handleClick}>Sign Up</BlueButton>
                    {loginAllowed && <AlertDialog title = "Account created" 
                        text = "You have successfully created an account. Press 'OK' to be directed to the login page."
                        buttonAgree={<Button onClick={navig}>OK</Button>}
                    />}
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
