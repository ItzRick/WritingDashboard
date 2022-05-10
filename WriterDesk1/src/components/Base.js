import React from 'react';
import PropTypes from 'prop-types';
import Navigation from './Navigation.js';
import NavigationLink from "./NavigationLink";



import { styled, useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import MuiDrawer from '@mui/material/Drawer';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';

// icons
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import FileUpload from '@mui/icons-material/Upload';
import TimelineIcon from '@mui/icons-material/Timeline';
import ArticleIcon from '@mui/icons-material/Article';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import GroupIcon from '@mui/icons-material/Group';
import BuildIcon from '@mui/icons-material/Build';
import PersonIcon from '@mui/icons-material/Person';

//replace with logo
import LogoDevIcon from '@mui/icons-material/LogoDev';

const DRAWERWIDTHOPEN = 240;
const DRAWERWIDTHCLOSE = 65;

const openedMixin = (theme) => ({
  width: DRAWERWIDTHOPEN,
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: 'hidden',
});

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

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'flex-end',
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
}));

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(['width', 'margin'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: DRAWERWIDTHOPEN,
    width: `calc(100% - ${DRAWERWIDTHOPEN}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    width: DRAWERWIDTHOPEN,
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

const Base = ({children, pageName="ERROR: no name provided", enableNav=true}) => {
    const [open, setOpen] = React.useState(false);
    const drawerWidth = DRAWERWIDTHCLOSE;

    const handleDrawer = () => {
        setOpen(!open);
        drawerWidth = open ? DRAWERWIDTHOPEN : DRAWERWIDTHCLOSE;
    };


  return (
    <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <AppBar 
            sx={{ 
                ...(open && {width: `calc(100% - ${DRAWERWIDTHOPEN}px)`, ml: `${DRAWERWIDTHOPEN}px`}),
                ...(!open && {width: `calc(100% - ${DRAWERWIDTHCLOSE}px)`, ml: `${DRAWERWIDTHCLOSE}px`}),
                alignItems: 'center',
            }}
        >
            <Toolbar
                sx = {{
                    
                }}
            >
                <Typography variant="h6" noWrap component="div" sx={{justify:'center'}}> {pageName} </Typography>
                <IconButton
                     sx = {{
                        justify: 'flex-end'
                    }}
                >
                    <MenuIcon />
                </IconButton>
            </Toolbar>
        </AppBar>

        <Drawer variant="permanent" open={open}>
            <DrawerHeader>
                <IconButton
                    color="inherit"
                    aria-label="open drawer"
                    onClick={handleDrawer}
                >
                    <MenuIcon />
                </IconButton>
            </DrawerHeader>
          <Divider />
          <List>
          <NavigationLink text="Main" Icon={LogoDevIcon} open={open}/>  
            <NavigationLink text="Upload" Icon={FileUpload} open={open}/>
            <NavigationLink text="Progress" Icon={TimelineIcon} open={open}/>
            <NavigationLink text="Documents" Icon={ArticleIcon} open={open}/>
            <Divider />
            <NavigationLink text="File Download" Icon={FileDownloadIcon} open={open}/>
            <NavigationLink text="Participants" Icon={GroupIcon} open={open}/>
            <NavigationLink text="Feedback Models" Icon={BuildIcon} open={open}/>
            <Divider />
            <NavigationLink text="Users" Icon={PersonIcon} open={open}/>


          </List>
        </Drawer>

        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
            <DrawerHeader />
            {children}
        </Box>
    </Box>
  );
}



/*
Base.PropTypes = {
    //children:
}*/


export default Base