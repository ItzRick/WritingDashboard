import {
    Button,
} from '@mui/material';

import { Link } from 'react-router-dom';

// tracking
import { useContext } from 'react';
import { TrackingContext } from '@vrbo/react-event-tracking';

/**
 * Default blue action button
 * 
 * @param {*} children content of the button
 * @param {String} idStr id of the button, for testing purposes
 * @param {String} pathName location to which the button will bring you. default is '' and routes you to where you are
 * @param {func} onClick function executes when clicked, default is empty function
 * @param {style} addStyle Additional style for the button, in the shape of sx
 * 
 * @returns default blue action button
 */
const BlueButton = ({children, idStr='', pathName='', onClick= ()=>{}, addStyle}) => {
    // context as given by the Tracking Provider
    const tc = useContext(TrackingContext);

    const handleClick = () => {
        if (tc.hasProvider) {
            if (pathName == '') {
                tc.trigger(`BlueButton.click`)
            } else {
                tc.trigger(`BlueButton.link`)
            }
            
        } else {
            // no provider available
        }

        // usual button action
        onClick()
    }
    
    return (
        <Button 
            id={idStr}
            size='large' variant='contained' sx={[{ bgcolor: 'button.main', color: 'button.text' }, addStyle]} 
            component={Link} to={{pathname: pathName}}
            onClick={handleClick}
        >
            {children}
        </Button>
    );
}

export default BlueButton