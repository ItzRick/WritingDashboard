// materials
import { 
    Typography 
} from "@mui/material";
import graphPlaceholder from '../images/chartImage.png';

// routing
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
            <div className='subTitle'>
                <Typography variant='h5'>Average score per skill category</Typography>
                <img src={graphPlaceholder} className='graph2' />
                <br /><br />
                <Typography variant='h5'>Progress over time</Typography>
                <img src={graphPlaceholder} className='graph2' />
            </div>
        </>
    );
}

export default Progress;