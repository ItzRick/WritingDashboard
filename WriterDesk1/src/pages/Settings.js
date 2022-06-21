// materials
import {
    FormControlLabel, 
    Radio, 
    RadioGroup, 
    TextField, 
    Typography,
    Button
} from "@mui/material";

// routing
import { useOutletContext, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
// Import the AuthenticationService for the logout:
import {AuthenticationService} from '../services/authenticationService';
// Import the history to be able to go to the homepage after logout:
import {history} from '../helpers/history';
// Change password request setup
import { authHeader } from '../helpers/auth-header';
import axios from 'axios';

import BlueButton from "../components/BlueButton";
import AlertDialog from "../components/AlertDialog";

const BASE_URL = "https://localhost:5000/loginapi";
const PASSWORD_LENGTH = 8;


/**
 * 
 * @returns Settings Page
 */
const Settings = () => {
    //set title in parent 'base' 
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('Settings');
    });

    // Create states for the old password, new Password (including conformation) and states for success or error messages.
    const [oldPassword, setOldPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [newPasswordConfirm, setNewPasswordConfirm] = useState("");
    const [successMessage, setSuccessMessage] = useState("");
    const [formError, setFormError] = useState("");

    const [accountDeletionPopup, setAccountDeletionPopup] = useState(false)

    /* 
     * Check if password input is valid.
     * According to URC 1.2-1.5, a valid password has at least 8 characters,
     * with at least 1 lowercase character, uppercase character and number.
     * @returns helper text for password textfield
     */
    const checkPassword = () => {
        if(newPassword === "") {
            return "";
        } else if(newPassword.length < PASSWORD_LENGTH) {
            return "Must contain at least 8 characters";
        } else if((newPassword.match(/[a-z]/g) || []).length < 1) {
            return "Must contain at least 1 lowercase letter";
        } else if((newPassword.match(/[A-Z]/g) || []).length < 1) {
            return "Must contain at least 1 uppercase letter";
        } else if((newPassword.match(/[0-9]/g) || []).length < 1) {
            return "Must contain at least 1 number";
        }
        return "";
    }

    /* 
     * Check if repeated password input is valid.
     * @returns helper text for second password textfield
     */
    const confirmPassword = () => {
        if(newPassword !== "" && newPassword !== newPasswordConfirm) {
            return "Must match Password";
        }
        return "";
    }

    let navigate = useNavigate();

    /* 
    * Logs out the user and redirects the user to the homepage.
    */   
    const logout = () => {
        AuthenticationService.logout();
        navigate("/", { replace: true });
    }

    const deleteUser = () => {
        //   The backend url:
        const url = 'https://127.0.0.1:5000/usersapi/deleteUserSelf';
        // Make the backend call and set the table data from the response data:
        axios.post(url,{},{headers: authHeader()}).then((response) => {
        })
    }
    
    /*
     * Do POST request containing new and old password variables, recieve status of response.
     */
    const changePassword = () => {
        // Check if input is valid
        if (oldPassword === "" || newPassword === "" || newPasswordConfirm === "") {
            setFormError("One or more fields are empty!");
            return;
        }
        if (checkPassword() !== "" || confirmPassword() !== "") {
            setFormError("One or more fields are not complete!");
            return;
        }
        // If input is valid, do post request
        const data = {
            "oldPassword": oldPassword,
            "newPassword": newPassword,
        }
        axios.post(`${BASE_URL}/setPassword`, data, {headers: authHeader()}).then(response =>{
            // Set a success message, reset the field.
            setSuccessMessage(response.data);
            // Reset all the fields:
            setOldPassword("");
            setNewPassword("");
            setNewPasswordConfirm("");
        }).catch(error =>{
            // Post request failed, user is not created
            setFormError(error.response.data);
        });
    }
    return (
        <>
            <div className='title'>
                {/* The logout button: */}
                <BlueButton idStr='logOut' onClick={logout}> Log out </BlueButton>
                <br />
                <Typography variant='h5' style={{color: '#44749D'}}>
                    Data setting
                </Typography>
                <br />
                <RadioGroup
                    aria-labelledby='terms'
                    defaultValue='yes'
                    name='terms group'
                    style={{display: 'inline'}}
                >
                    <FormControlLabel value="yes" control={<Radio />} label="I accept the data conditions." />
                    <br /><br />
                    <FormControlLabel value="no" control={<Radio />} label="I refuse the data conditions." />
                </RadioGroup>
                <br />
                <Typography sx={{maxWidth: '60%', margin:'auto'}}>
                The data conditions allow the application to record user data. The user data is the clicks of the user within the application and their time and location. This data is only used to improve the automatic feedback generated within the application. The application is still fully available when refusing the data conditions.
                </Typography>
                <br />
                <Typography variant='h5' style={{color: '#44749D'}}>
                    Change password
                </Typography>
                <br />
                <TextField value = {oldPassword} onChange={(e) => {setOldPassword(e.target.value); 
                setFormError(""); setSuccessMessage("")}} id='currPass' label='Insert current password.' 
                variant='outlined' type = 'password' style={{marginBottom: '1vw'}} />
                <br />
                <TextField value = {newPassword} onChange={(e) => {setNewPassword(e.target.value); 
                setFormError(""); setSuccessMessage("")}} id='newPass' label='Insert new password.' variant='outlined' type='password'
                style={{marginBottom: '1vw'}} 
                error={checkPassword() !== ""} helperText={checkPassword() !== "" ? checkPassword() : " "}
                />
                <br />
                <TextField value = {newPasswordConfirm} onChange={(e) => {setNewPasswordConfirm(e.target.value); 
                setFormError(""); setSuccessMessage("")}} id='newPass2' label='Insert new password again.' 
                variant='outlined' type='password' style={{marginBottom: '1vw'}}
                error={confirmPassword() !== ""} helperText={confirmPassword() !== "" ? confirmPassword() : " "}
                />
                <br />
                <BlueButton idStr='updatePassword' variant='contained' onClick={changePassword}>Update password</BlueButton>
                <br />
                {/* If the password change has failed, or we have a successful change, relay this message: */}
                    {formError !== "" && <Typography color="red">{formError}</Typography>}
                    {successMessage !== "" && <Typography>{successMessage}</Typography>}
                <br /><br /><br />
                <Typography variant='h5' style={{color: '#44749D'}}>
                    Delete account
                </Typography>
                <br />
                <BlueButton idStr='DeleteMyAccount' variant='contained' onClick={(e) => {setAccountDeletionPopup(true)}}>I want to delete my account.</BlueButton>
                {accountDeletionPopup && <AlertDialog title = "Account deletion" 
                    text = "Are you sure you want to delete your account?"
                    buttonAgree={<Button onClick={(e) => {deleteUser()}} style={{color: "red"}}>Yes, I want to delete my account!</Button>}
                    buttonCancel={<Button onClick={(e) => {setAccountDeletionPopup(false)}}>Cancel</Button>}
                />}
            </div>
        </>
    );
}

export default Settings;