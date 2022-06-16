// materials
import {Button, FormControlLabel, Radio, RadioGroup, TextField, Typography} from "@mui/material";
import BlueButton from "./../components/BlueButton";

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';



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
    return (
        <>
            <div className='title'>
                <BlueButton> Log out </BlueButton>
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
                <TextField id='currPass' label='Insert current password.' variant='outlined'
                style={{marginBottom: '1vw'}} />
                <br />
                <TextField id='newPass' label='Insert new password.' variant='outlined' type='password'
                style={{marginBottom: '1vw'}} />
                <br />
                <TextField id='newPass2' label='Insert new password again.' variant='outlined' type='password'
                style={{marginBottom: '1vw'}} />
                <br />
                <Button variant='contained'>Update password</Button>
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