import React from 'react';
import PropTypes from 'prop-types';

// css
import "./../css/NavigationLink.css";

// mui components
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Tooltip from '@mui/material/Tooltip';

/**
 * Icon with text linking to a page, to be used in a Drawer
 * @param {string} text Text next to the button icon
 * @param {Icon} Icon Icon of the 
 * @param {bool} open Whether the Drawer (left side bar) is open
 * @param {bool} visible The menu item should be visible for the current, logged on user
 * @returns <NavigationLink />
 */
const NavigationLink = ({text, Icon, open, allowed=false}) => {
    return (
        <ListItem key={text} disablePadding sx={{ 
            display: allowed ? 'block' : 'none'
        }}>
            { /* Tooltip == text that only displays when the drawer is closed */ }
            <Tooltip 
                title={text} 
                placement="right"
                disableHoverListener={open}
                sx={{
                    display: open ? 'initial' : 'none',
                }}
            >
                <ListItemButton
                sx={{
                    minHeight: 48,
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
            </Tooltip>
        </ListItem>
    );
}

NavigationLink.propTypes = {
    text: PropTypes.string,
    open: PropTypes.bool,
    visible: PropTypes.bool,
    //Icon : PropTypes.
}


export default NavigationLink