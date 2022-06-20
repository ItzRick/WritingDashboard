import React from 'react';
import PropTypes from 'prop-types';

// css
import "./../css/Navigation.css";

// components
import { 
    ListItem,
    ListItemText,
    Tooltip,
    ListItemIcon
} from '@mui/material';

// routing
import { Link } from 'react-router-dom';

// tracking
import { useContext } from 'react';
import { TrackingContext } from '@vrbo/react-event-tracking';

/**
 * Icon with text linking to a page, to be used in a Drawer
 * @param {string} text - Text next to the button icon
 * @param {Icon} Icon - Icon of the link
 * @param {bool} open - Whether the Drawer (left side bar) is open
 * @param {bool} visible - The menu item should be visible for the current, logged on user
 * @returns NavigationLink Component
 */
const NavigationLink = ({ text, Icon, open, allowed = false, pageLink }) => {
    // context as given by the Tracking Provider
    const tc = useContext(TrackingContext);
    // handle tracking when the link is activated
    const handleClick = () => {
        if (tc.hasProvider) {
            tc.trigger({
                eventType: 'link',
                buttonId: pageLink, 
            })
        }
    }
    return (
        <ListItem
            key={text}
            disablePadding
            sx={{
                display: allowed ? 'block' : 'none'
            }}
        >
            { /* Tooltip == text that only displays when the drawer is closed */}
            <Tooltip
                title={text}
                placement="right"
                disableHoverListener={open}
                sx={{
                    display: open ? 'initial' : 'none',
                }}
            >

                <ListItem button
                    sx={{
                        minHeight: 48,
                        px: 2.5,
                    }}
                    onClick={handleClick}
                    component={Link} to={{ pathname: pageLink }}
                >
                    <ListItemIcon
                        sx={{
                            color: 'drawer.icon',
                            minWidth: 0,
                            mr: open ? 3 : 'auto',
                            justifyContent: 'center',
                        }}
                    >
                        <Icon/>
                    </ListItemIcon>

                    <ListItemText
                        primary={text}
                        sx={{
                            opacity: open ? 1 : 0, 
                            color: 'drawer.text'
                        }}
                    />
                </ListItem>
            </Tooltip>
        </ListItem>
    );
}

NavigationLink.propTypes = {
    text: PropTypes.string,
    open: PropTypes.bool,
    visible: PropTypes.bool,
}

export default NavigationLink