import React from 'react';
import { Routes, Route } from 'react-router-dom';

// Import pages if you want to add them to the routes:
import Home from './Pages/Home';
import Upload from './Pages/Upload';
import ListFiles from './Pages/ListFiles';


const Main = () => {
    return (
        // Add routes here:
        <Routes>
            <Route path='/' element={<Home/>}/>
            <Route path='/upload' element={<Upload/>}/>
            <Route path='/listfiles' element={<ListFiles/>}/>
        </Routes>
       
    );   
}

export default Main;