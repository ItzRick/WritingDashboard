import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';



/**
 * 
 * @returns Progress Page
 */
function Progress() {
    //set title in parent 'base' 
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('Progress');
    });
    return (
        <>
            Progress
        </>
    );
}

export default Progress;