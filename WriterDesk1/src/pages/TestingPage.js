import {
    Button
} from "@mui/material";
import TestingComponent from "./../components/TestingComponent";
import { AuthenticationService } from "../services/authenticationService";
import { useEffect, useState } from "react";

/**
 * page used for testing, to be removed later
 * 
 * @returns Testing Page
 */
const TestingPage = () => {
    const [userLoggedIn, setLoggedIn] = new useState(false);
    const [testRole, setRole] = new useState('');

    const handleLogin = () => {
        AuthenticationService.login('m.l.langedijk@student.tue.nl', 'wachtwoord');
    }

    const handleFLogin = () => {
        AuthenticationService.login('m.l.langedijk@student.tue.nl', 'Fwachtwoord');
    }

    const handleRole = () => {
        AuthenticationService.getRole()
        .then(result => {
            setRole(result);
        }).catch(error =>{
            setRole('');
        });
        //setRole(JSON.parse(localStorage.getItem('currentUser')).role);
    }

    useEffect(() => {
        AuthenticationService.checkAuth()
        .then( () => {
            setLoggedIn(true);
        }).catch(error => {
            setLoggedIn(false);
        });
        console.log('useEffect Function is used');
    });

    return (
    <>
    {testRole != '' &&
        <p>Role: {testRole}</p>
    }
    { userLoggedIn == false &&
        <Button variant="contained" sx={{bgcolor: 'button.main', color: 'button.text'}} onClick={handleLogin}>Login</Button>
    }
    <br/>
    <Button variant="contained" sx={{bgcolor: 'button.main', color: 'button.text'}} onClick={handleFLogin}>False Login</Button>
    <br/>
    <Button variant="contained" sx={{bgcolor: 'button.main', color: 'button.text'}} onClick={handleRole}>Get Role</Button>
        {testRole != '' ? <> {testRole} </> : <> no role </>}
    </>
    )
}




export default TestingPage;