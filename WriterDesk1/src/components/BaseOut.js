import React from 'react';
import PropTypes from 'prop-types';

// routing
import { Outlet } from 'react-router-dom';


// mui components
import { styled, useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import MuiDrawer from '@mui/material/Drawer';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import CssBaseline from '@mui/material/CssBaseline';


//Width of the opened drawer
const drawerWidth = 240;

// Below functions were made by
// https://mui.com/material-ui/react-drawer/
// open drawer animation
const openedMixin = (theme) => ({
    width: drawerWidth,
    transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
    }),
    overflowX: 'hidden',
});

// close drawer animation
const closedMixin = (theme) => ({
    transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }),
    overflowX: 'hidden',
    width: `calc(${theme.spacing(7)} + 1px)`,
    [theme.breakpoints.up('sm')]: {
        width: `calc(${theme.spacing(8)} + 1px)`,
    },
});

// make DrawerHeader style
const DrawerHeader = styled('div')(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar,
}));

// make AppBar style
const AppBar = styled(MuiAppBar, {
    shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }),
    ...(open && {
        marginLeft: drawerWidth,
        width: `calc(100% - ${drawerWidth}px)`,
        transition: theme.transitions.create(['width', 'margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
    }),
}));

// make Drawer style
const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
    ({ theme, open }) => ({
        width: drawerWidth,
        flexShrink: 0,
        whiteSpace: 'nowrap',
        boxSizing: 'border-box',
        ...(open && {
            ...openedMixin(theme),
            '& .MuiDrawer-paper': openedMixin(theme),
        }),
        ...(!open && {
            ...closedMixin(theme),
            '& .MuiDrawer-paper': closedMixin(theme),
        }),
    }),
);

/**
 * Makes the BasePage
 * 
 * @returns Base page, for non-authenticated user
 */
const Base = () => {
    // general theme, defined in index.js
    const theme = useTheme();
    
    return (
        <Box sx={{ display: 'flex', color: 'primary' }}>
            <CssBaseline />
            <AppBar
                position='fixed'
                sx={{
                    ...({
                        width: `calc(100% - ${theme.spacing(7)} + 1px)`,
                        [theme.breakpoints.up('sm')]: {
                            width: `calc(100% - ${theme.spacing(8)} + 1px)`,
                        },
                    })
                }}
            >
                <Toolbar sx={{
                    width: '100%',
                    display: 'flex',
                    flexDirection: 'row',
                    justifyContent: 'space-between',
                }}>

                </Toolbar>
            </AppBar>

            <Drawer
                className='classes.drawerOut'
                variant="permanent"
                open={false}
                sx={{
                    display: 'initial',
                    color: 'main.primary',
                }}
            >
                <DrawerHeader justify="center">
                </DrawerHeader>
            </Drawer>

            <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
                <DrawerHeader />
                <Outlet />
            </Box>
        </Box>
    );
}



Base.propTypes = {
    //children:
}


export default Base