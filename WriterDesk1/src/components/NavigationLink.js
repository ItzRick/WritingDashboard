import React from 'react';
import PropTypes from 'prop-types';

import "./../css/NavigationLink.css";

import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';

/**
 * 
 * @param {*} param0 
 * @returns 
 */
const NavigationLink = ({text, Icon, open}) => {
    return (
        <ListItem key={text} disablePadding sx={{ display: 'block' }}>
            <ListItemButton
            sx={{
                minHeight: 48,
                justifyContent: open ? 'initial' : 'center',
                px: 2.5,
            }}
            >
            <ListItemIcon
                sx={{
                minWidth: 0,
                mr: open ? 3 : 'auto',
                justifyContent: 'center',
                }}
            >
                <Icon />
            </ListItemIcon>
            <ListItemText primary={text} sx={{ opacity: open ? 1 : 0 }} />
            </ListItemButton>
        </ListItem>
    );
}

NavigationLink.propTypes = {
    text: PropTypes.string,
    open: PropTypes.bool,
    
}


export default NavigationLink