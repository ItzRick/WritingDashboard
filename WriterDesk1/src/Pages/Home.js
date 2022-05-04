import React from 'react';
import {Link} from 'react-router-dom';
// import '../App.css';

const Home = () => {
    return (
    <div className='Home'>
        <h1>Welcome to my portfolio website</h1>
        <p> Feel free to browse around and learn more about me.</p>
        <Link to="/SignUp">SignUp</Link>
    </div> );
}

export default Home;