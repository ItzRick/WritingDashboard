// materials
import { } from "@mui/material";

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';

/**
 * 
 * @returns Participants Page
 */
function Participants() {
    //set title in parent 'base' 
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('Participants');
    });
    return (
        <>
            Participants
        </>
    );
}

export default Participants;