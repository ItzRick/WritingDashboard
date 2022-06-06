import {
    Button
} from "@mui/material";
import TestingComponent from "./../components/TestingComponent";
import { AuthenticationService } from "../services/authenticationService";
import { useState } from "react";

/**
 * page used for testing, to be removed later
 * 
 * @returns Testing Page
 */
const TestingPage = () => {
    const [role, setRole] = new useState('')

    const handleLogin = () => {
        AuthenticationService.login('m.l.langedijk@student.tue.nl', 'wachtwoord');
    }

    const handleFLogin = () => {
        AuthenticationService.login('m.l.langedijk@student.tue.nl', 'Fwachtwoord');
    }

    const handleRole = () => {
        AuthenticationService.getRole()
        .then(role => {
            setRole(role);
        }).catch(error =>{
            setRole('');
        });
        //setRole(JSON.parse(localStorage.getItem('currentUser')).role);
    }
    return (
    <>
    {role != '' &&
        <p>Role: {role}</p>
    }
    <Button variant="contained" sx={{bgcolor: 'button.main', color: 'button.text'}} onClick={handleLogin}>Login</Button>
    <br/>
    <Button variant="contained" sx={{bgcolor: 'button.main', color: 'button.text'}} onClick={handleFLogin}>False Login</Button>
    <br/>
    <Button variant="contained" sx={{bgcolor: 'button.main', color: 'button.text'}} onClick={handleRole}>Get Role</Button>
        {role != '' ? <> {role} </> : <> no role </>}
    </>
    )
}




export default TestingPage;