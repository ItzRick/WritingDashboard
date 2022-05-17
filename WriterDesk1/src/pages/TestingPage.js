import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';


/**
 * 
 * @returns Documents Page
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