import React, {useState} from 'react';
import PropTypes from 'prop-types';
// import '../App.css';

//import components
import SignUpForm from '../components/SignUpForm';


const SignUp = () => {
    return (
    <SignUpForm setToken={func}/>
    );
}

const func = () => {}


export default SignUp;