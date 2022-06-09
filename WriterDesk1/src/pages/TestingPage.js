// materials
import { } from "@mui/material";

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';

//page used for testing, to be removed later

/**
 * page used for testing, to be removed later
 * 
 * @returns Testing Page
 */
const TestingPage = () => {
    //set title in parent 'base' 
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('TestingPage');
    });
    return (
        <>
            
        </>
    );
}

export default TestingPage;