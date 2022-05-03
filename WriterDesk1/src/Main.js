import React from 'react';
import { NavLink, Routes, Route } from 'react-router-dom';

// import Home from './Pages/Home';

const Home = () => {
    <div className='home'>
    <h1>Welcome to my portfolio website</h1>
    <p> Feel free to browse around and learn more about me.</p>
  </div>
}

const Main = () => {
    return (
        <Routes>
            <Route exact path='/' element={<Home/>}/>
        </Routes>
       
    );   
}

export default Main;