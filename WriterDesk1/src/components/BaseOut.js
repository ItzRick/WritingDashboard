import {React, useState} from 'react';

// routing
import { Outlet } from 'react-router-dom';


// mui components
import { styled, useTheme } from '@mui/material/styles';
import {
    Box,
    Drawer,
    AppBar,
    Toolbar,
    CssBaseline,
    Typography
} from '@mui/material';


//Width of the opened drawer
const drawerWidth = 240;

// Below functions were made by
// https://mui.com/material-ui/react-drawer/
/**
 * 
 * @param {theme} theme - Given by theme provider in index
 * @returns transition when open
 */
const openedMixin = (theme) => ({
    width: drawerWidth,
    transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
    }),
    overflowX: 'hidden',
});

/**
 * 
 * @param {theme} theme - Given by theme provider in index
 * @returns transition when closed
 */
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

/**
 * Makes styled DrawerHeader
 */
const DrawerHeader = styled('div')(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar,
}));

/**
 * Makes styled AppBar
 */
const CustomAppBar = styled(AppBar, {
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

/**
 * Makes styled Drawer
 */
const CustomDrawer = styled(Drawer, { shouldForwardProp: (prop) => prop !== 'open' })(
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
    
    // provides title to the base page using the context of the outlet
    const [title, setTitle] = useState("");

    return (
        <Box sx={{ display: 'flex', color: 'primary' }}>
            <CssBaseline />
            <CustomAppBar
                position='fixed'
                sx={{
                    bgcolor: 'drawerOut.background',
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
                    justifyContent: 'center',
                }}>
                    <Typography variant="h6" component="div" sx={{color: "appBar.text",}}> {title} </Typography>
                </Toolbar>
            </CustomAppBar>

            <CustomDrawer
                className='classes.drawerOut'
                variant="permanent"
                open={false}
                sx={{
                    display: 'initial',
                    bgcolor: 'drawerOut.background',
                    height: '100%',
                    zIndex: 100
                }}
            >
                <DrawerHeader justify="center" sx={{
                    bgcolor: 'drawerOut.background',
                    height: '100%'
                }}>
                </DrawerHeader>
            </CustomDrawer>

            <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
                <DrawerHeader />
                <Outlet context={{ setTitle }} />
            </Box>
        </Box>
    );
}


export default Base