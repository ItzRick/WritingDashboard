import React, {useState} from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';

// import '../App.css';

//import components
import Input from './Input'
import Button from './Button'



async function loginUser(credentials) {
    const url = 'http://localhost:5000/signUpStudent';
        const headers = {
            Accept: 'application/json'
        };
        const data = JSON.stringify(credentials);
        axios.post(url, data, headers).then((response) => {
            console.log(response.data);
        });

/*
    return fetch('http://localhost:5000/signUpStudent', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials)
    })
      .then(data => data.json())*/
}

const SignUpForm = ({setToken}) => {
    const [username, setUserName] = useState();
    const [password, setPassword] = useState();
    const [passwordRepeat, setPasswordRepeat] = useState();
    
    const handleSubmit = async e => {
        e.preventDefault();
        console.log(username, password, passwordRepeat);
        if (password === passwordRepeat) {
            console.log("Pass match");
            const token = await loginUser({
                username,
                password
            });
        } else {
            console.log("Error: no pass match");
        }
        //setToken(token);
    }

    // the actual component
    return (
    <div className='SignUpForm'>
        <h1>SignUp Page</h1>
        <form onSubmit={handleSubmit}>
            <Input text="Username" type="text" onChange={e => setUserName(e.target.value)}/>
            <Input text="Password" type="password" onChange={e => setPassword(e.target.value)}/>
            <Input text="Repeat Password" type="password" onChange={e => setPasswordRepeat(e.target.value)}/>
            <Button text="Sign Up" type="submit" />
        </form>
    </div> 
    );
}

SignUpForm.propTypes = {
    setToken: PropTypes.func.isRequired,
}

export default SignUpForm;