import {
    Button,
} from '@mui/material';

import { Link } from 'react-router-dom';

/**
 * Default blue action button
 * 
 * @param {*} children content of the button
 * @param {String} pathName location to which the button will bring you. default is '' and routes you to where you are
 * @param {func} onClick function executes when clicked, default is empty function
 * 
 * @returns default blue action button
 */
const BlueButton = ({children, pathName='', onClick= ()=>{} }) => {
    return (
        <Button 
            size='large' variant='contained' sx={{ bgcolor: 'button.main', color: 'button.text' }} 
            component={Link} to={{pathname: pathName}}
            onClick={onClick}
        >
            {children}
        </Button>
    );
}

export default BlueButton