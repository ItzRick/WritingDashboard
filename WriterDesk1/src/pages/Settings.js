// materials
import {Button, FormControlLabel, Radio, RadioGroup, TextField, Typography} from "@mui/material";

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect, useState } from 'react';



/**
 * 
 * @returns Settings Page
 */
const Settings = () => {
    const PASSWORD_LENGTH = 8;
    //set title in parent 'base' 
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('Settings');
    });

    const [oldPassword, setOldPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [newPasswordConfirm, setNewPasswordConfirm] = useState("");

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

    // Change page using formError when we find an error
    const [formError, setFormError] = useState("");

    const changePassword = () => {
        console.log(oldPassword);
    }
    return (
        <>
            <div className='title'>
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
                <TextField value = {oldPassword} onChange={(e) => {setOldPassword(e.target.value); setFormError("")}} id='currPass' label='Insert current password.' variant='outlined' type = 'password'
                style={{marginBottom: '1vw'}} />
                <br />
                <TextField value = {newPassword} onChange={(e) => {setNewPassword(e.target.value); setFormError("")}} id='newPass' label='Insert new password.' variant='outlined' type='password'
                style={{marginBottom: '1vw'}} 
                error={checkPassword() !== ""} helperText={checkPassword() !== "" ? checkPassword() : " "}
                />
                <br />
                <TextField value = {newPasswordConfirm} onChange={(e) => {setNewPasswordConfirm(e.target.value)}} id='newPass2' label='Insert new password again.' variant='outlined' type='password'
                style={{marginBottom: '1vw'}}
                error={confirmPassword() !== ""} helperText={confirmPassword() !== "" ? confirmPassword() : " "}
                />
                <br />
                <Button variant='contained' onClick={changePassword}>Update password</Button>
                <br /><br /><br />
                <Typography variant='h5' style={{color: '#44749D'}}>
                    Delete account
                </Typography>
                <br />
                <Button variant='contained'>I want to delete my account.</Button>
            </div>
        </>
    );
}

export default Settings;