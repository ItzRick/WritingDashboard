import React from 'react';
// import '../App.css';

//import components
import SingUpInput from '../components/SignUpInput'
import Button from '../components/Button'

const SignUp = () => {
    return (
    <div className='SignUp'>

        <h1>SignUp Page</h1>
        <form onSubmit={handleSubmit}>
            <SingUpInput text="Username" type="text" onChange={setUserName} />
            <SingUpInput text="Password" type="text" onChange={setPassword}/>
            <SingUpInput text="Repeat Password" type="text" />
            <Button text="submit" type="submit" />

        </form>
    </div> );
}

const setUserName = e => {
    console.log(e.target.value);
}

const setPassword = e => {
    console.log(e.target.value);
}

const handleSubmit = async e => {
    console.log("sumbit");
}

export default SignUp;