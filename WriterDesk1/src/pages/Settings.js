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
// Change password request setup
import { authHeader } from '../helpers/auth-header';
import axios from 'axios';

import BlueButton from "../components/BlueButton";
import AlertDialog from "../components/AlertDialog";

import fileDownload from 'js-file-download';

const PASSWORD_LENGTH = 8;
const USERNAME_END = "tue.nl";

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

    const [userRole, setUserRole] = useState('');

    useEffect(() => {
        // Call getTrackable function to show radio button correctly
        getTrackable();
        setUserRole(AuthenticationService.getRole())
    }, []);

    // Create states for the old password, new Password (including conformation) and states for success or error messages.
    const [oldPassword, setOldPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [newPasswordConfirm, setNewPasswordConfirm] = useState("");
    const [successMessage, setSuccessMessage] = useState("");
    const [formError, setFormError] = useState("");

    const [trackableValue, setTrackableValue] = useState('');  // Value for radio buttons to accept or refuse data, can be 'yes' or 'no'.

    const [accountDeletionPopup, setAccountDeletionPopup] = useState(false)
    const [successDeleteDialog, setSuccessDeleteDialog] = useState(false); // Alert that account is successfully deleted.

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
    }

	/**
	 *	Function that makes the api call to delete the user
	 */
    const deleteUser = () => {
        //   The backend url:
        const url = 'https://api.writingdashboard.xyz/usersapi/deleteUserSelf';
        // Make the backend call and set the table data from the response data:
        axios.post(url,{},{headers: authHeader()}).then((response) => {
            setAccountDeletionPopup(false);
            setSuccessDeleteDialog(true);
        })

        return false;
	}

    /**
     * Function to make the backend call to change the trackable value for the current user in the database.
     * @param {string} newTrackable: String value with 'yes' or 'no' to set new trackable value.
     */
    const changeTrackable = (newTrackable) => {
        const formData = new FormData();
        formData.append('newTrackable', newTrackable);
        axios.post('https://api.writingdashboard.xyz/loginapi/setTrackable', formData, {headers: authHeader()})
    }

    /**
     * Function to make the backend call to get the trackable value for the current user.
     */
    const getTrackable = () => {
        axios.get('https://api.writingdashboard.xyz/loginapi/getTrackable', {headers: authHeader()}).then(
          response => {
              setTrackableValue(response.data)
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
        axios.post(`https://api.writingdashboard.xyz/loginapi/setPassword`, data, {headers: authHeader()}).then(response =>{
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

    const handleOwnUserData = () => {
        const url = 'https://api.writingdashboard.xyz/clickapi/getOwnUserData';
        axios.get(url, { headers: authHeader()})
          .then((response) => {
            const fileName = response.headers["custom-filename"];
            fileDownload(response.data, fileName);
          })
          .catch(err => {
            console.log(err.response.data)
          })
    }

    // whether or not the information about the user data is shown.
    const [showUserDataPopup, setShowUserDataPopup] = useState(false)


    // Set password from textfield for email change
    const [passwordForEmail, setPasswordForEmail] = useState("");
    // Set username from textfield
    const [username, setUsername] = useState("");
    // Set repeated username from textfield
    const [usernameConfirm, setUsernameConfirm] = useState("");
    // error bellow mail button
    const [formMailError, setFormMailError] = useState("");
    const [successMailMessage, setSuccessMailMessage] = useState("");
    /**
     * Check if repeated username input is valid.
     * @returns helper text for second username textfield
     */
     const confirmUsername = () => {
        if(username !== "" && username !== usernameConfirm) {
            return "Must match username";
        }
        return "";
    }

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

    const changeEmail = () => {
        // Check if input is valid
        if (passwordForEmail === "" || username === "" || usernameConfirm === "") {
            setFormMailError("One or more fields are empty!");
            return;
        }
        if (checkUsername() !== "" || confirmUsername() !== "") {
            setFormMailError("One or more fields are not complete!");
            return;
        }
        // If input is valid, do post request
        const data = {
            "currentPassword": passwordForEmail,
            "newUsername": username,
        }
        axios.post(`https://api.writingdashboard.xyz/loginapi/setUsername`, data, {headers: authHeader()})
        .then(response =>{
            // Set a success message, reset the field.
            setSuccessMailMessage(response.data);
            // Reset all the fields:
            setPasswordForEmail("");
            setUsername("");
            setUsernameConfirm("");
        }).catch(error =>{
            // Post request failed, user is not created
            setFormMailError(error.response.data);
        });
    }
    return (
        <>
            <div className='title'>
                {/* The logout button: */}
                <BlueButton idStr='logOut' onClick={logout}> Log out </BlueButton>
                <br /><br />
                <Typography variant='h5' style={{color: '#44749D'}}>
                    Data setting
                </Typography>
                <br />
                <RadioGroup
                    aria-labelledby='terms'
                    defaultValue='yes'
                    name='terms group'
                    style={{display: 'inline'}}
                    onChange={(e) => {setTrackableValue(e.target.value); changeTrackable(e.target.value);}}
                    value={trackableValue}
                >
                    <FormControlLabel value="yes" control={<Radio />} label="I accept the data conditions." />
                    <br /><br />
                    <FormControlLabel value="no" control={<Radio />} label="I refuse the data conditions." />
                </RadioGroup>
                <br /> <br />
                <div>
                    <Typography sx={{alignSelf: 'center', alignContent:'inline'}}>
                        View the <a className='userDataLinkPopup' onClick={() => {setShowUserDataPopup(true)}} >user data agreement</a>.
                    </Typography>
                    {showUserDataPopup && <AlertDialog title = "User data agreement"
                        text = "The data conditions allow the application to record user data. The user data includes the URL of the page, the location on the screen, and the timestamp of each click from the user.  The user data is only used to improve the automatic feedback generated within the application. If the purpose of the data changes, the application will ask the user again for permission to save their user data. This data does not include necessary sign-up information, such as the university email address and the password, since that is saved to ensure the functionalities of the application. The sign-up information is not used for any other purposes than logging into the application. The application is still fully available when refusing the data conditions. If the user refuses permission, no user data will be recorded of this user until the moment that they accept the data settings in the future. If the user accepts the permission at first but later revokes the permission, their recorded user data is deleted and no user data will be recorded of this user, until the moment that they accept the data settings in the future. Users can retrieve the recorded user data so far at any time. Users can ask questions regarding their data by sending a mail to i.l.h.rutten@student.tue.nl; a response will be provided within a month."
                        buttonAgree={<Button onClick={() => {setShowUserDataPopup(false)}}>I understand</Button>}
                    />}
                </div>
                <br />
                <BlueButton idStr='downloadMyUserData' onClick={() => {handleOwnUserData()}}>Download my user data</BlueButton>
                <br />
                <br />
                <Typography variant='h5' style={{color: '#44749D'}}>
                    Change password
                </Typography>
                <br />
                <TextField value = {oldPassword} onChange={(e) => {setOldPassword(e.target.value);
                setFormError(""); setSuccessMessage("")}} id='currPass' label='Insert current password.'
                variant='outlined' type = 'password' style={{width: '260px'}} helperText={' '}/>
                <br />
                <TextField value = {newPassword} onChange={(e) => {setNewPassword(e.target.value);
                setFormError(""); setSuccessMessage("")}} id='newPass' label='Insert new password.' variant='outlined' type='password'
                error={checkPassword() !== ""} style={{width: '260px'}} helperText={checkPassword() !== "" ? checkPassword() : " "}
                />
                <br />
                <TextField value = {newPasswordConfirm} onChange={(e) => {setNewPasswordConfirm(e.target.value);
                setFormError(""); setSuccessMessage("")}} id='newPass2' label='Insert new password again.'
                variant='outlined' type='password' style={{width: '260px'}}
                error={confirmPassword() !== ""} helperText={confirmPassword() !== "" ? confirmPassword() : " "}
                />
                <br />
                <BlueButton idStr='updatePassword' variant='contained' onClick={changePassword}>Update password</BlueButton>
                <br />
                {/* If the password change has failed, or we have a successful change, relay this message: */}
                    {formError !== "" && <Typography color="red">{formError}</Typography>}
                    {successMessage !== "" && <Typography>{successMessage}</Typography>}
                <br />
                {userRole !== 'participant' && <div>
                    <Typography variant='h5' style={{color: '#44749D'}}>
                        Change email
                    </Typography>
                    <br />
                    <TextField value = {passwordForEmail} onChange={(e) => {setPasswordForEmail(e.target.value);
                    setFormMailError(""); setSuccessMailMessage("")}} id='currPass' label='Insert password.'
                    variant='outlined' type = 'password' style={{width: '260px'}} helperText={' '}/>
                    <br />
                    <TextField id='changeEmail' label='Insert new username.' variant='outlined'
                        value={username} onChange={(e) => {setUsername(e.target.value); setFormMailError(""); setSuccessMailMessage("")}}
                        error={checkUsername() !== ""} style={{width: '260px'}} helperText={checkUsername() !== "" ? checkUsername() : " "}
                    />
                    <br />
                    <TextField id='changeEmail2' label='Repeat new username.' variant='outlined'
                        value={usernameConfirm} onChange={(e) => {setUsernameConfirm(e.target.value); setFormMailError(""); setSuccessMailMessage("")}}
                        error={confirmUsername() !== ""} style={{width: '260px'}} helperText={confirmUsername() !== "" ? confirmUsername() : " "}
                    />
                    <br />
                    <BlueButton idStr='updateEmail' variant='contained' onClick={changeEmail}>Update email</BlueButton>
                    <br />
                    {/* If the password change has failed, or we have a successful change, relay this message: */}
                        {formMailError !== "" && <Typography color="red">{formMailError}</Typography>}
                        {successMailMessage !== "" && <Typography>{successMailMessage}</Typography>}
                    <br />
                </div>}
                <Typography variant='h5' style={{color: '#44749D'}}>
                    Delete account
                </Typography>
                <br />
                <BlueButton idStr='DeleteMyAccount' variant='contained' onClick={(e) => {setAccountDeletionPopup(true)}}>I want to delete my account.</BlueButton>
                <br /><br />
                {accountDeletionPopup && <AlertDialog title = "Account deletion"
                    text = "Are you sure you want to delete your account?"
                    buttonAgree={<Button onClick={(e) => {deleteUser()}} style={{color: "red"}}>Yes, I want to delete my account!</Button>}
                    buttonCancel={<Button onClick={(e) => {setAccountDeletionPopup(false)}}>Cancel</Button>}
                />}
                {successDeleteDialog && <AlertDialog title = "Successfully deleted account"
                    text = "Your account has been successfully deleted. You will be redirected to the login page."
                    buttonAgree={<Button onClick={(e) => {window.location.reload()}}>Ok</Button>}
                />}
            </div>
        </>
    );
}

export default Settings;