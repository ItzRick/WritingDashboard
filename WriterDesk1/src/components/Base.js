import React from 'react';
import PropTypes from 'prop-types';

// components
import NavigationLink from "./NavigationLink";

// mui components
import { styled, useTheme } from '@mui/material/styles';
import Tooltip from '@mui/material/Tooltip';
import Box from '@mui/material/Box';
import MuiDrawer from '@mui/material/Drawer';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';

// icons
import MenuIcon from '@mui/icons-material/Menu';
import FileUpload from '@mui/icons-material/Upload';
import TimelineIcon from '@mui/icons-material/Timeline';
import ArticleIcon from '@mui/icons-material/Article';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import GroupIcon from '@mui/icons-material/Group';
import BuildIcon from '@mui/icons-material/Build';
import PersonIcon from '@mui/icons-material/Person';
import SettingsIcon from '@mui/icons-material/Settings';
//replace with logo
import LogoDevIcon from '@mui/icons-material/LogoDev';

//Width of the opened drawer
const drawerWidth = 240;

const openedMixin = (theme) => ({
  width: drawerWidth,
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
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

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
 * @param {*} children Children nodes of <base> </base> 
 * @param {bool} enableNav The navigation drawer, on the left, is visible
 * @param {bool} researcher The user is a researcher
 * @param {bool} admin The user is an admin
 * @returns <base></base> wrapper
 */

const Base = ({
  children, 
  pageName="ERROR: no name provided, <Base pageName>", 
  enableNav=true,
  researcher=false,
  admin=false,
}) => {
  const [open, setOpen] = React.useState(false);

  const theme = useTheme();
  
  const handleDrawer = () => {
      setOpen(!open);
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar 
        sx={{ 
          ...(open && {width: `calc(100% - ${drawerWidth}px)`, ml: `${drawerWidth}px`}),
          ...(!open && {
            width: enableNav ? `calc(100% - ${theme.spacing(7)} + 1px)` : `100%`,
            [theme.breakpoints.up('sm')]: {
              width: enableNav ? `calc(100% - ${theme.spacing(8)} + 1px)` : `100%`,
            },
          }),
        }}
      >
        <Toolbar sx={{
          width: '100%',
          display:'flex',
          flexDirection: 'row',
          justifyContent:'space-between',
        }}>
          <div></div>
          <Typography variant="h6" component="div"> {pageName} </Typography>
          <IconButton 
            color="inherit"
            sx={{
              justifySelf:"flex-end",
            }}
          >
            <SettingsIcon />
          </IconButton>
        </Toolbar>
        
      </AppBar>



      <Drawer 
        variant="permanent" 
        open={open}
        sx={{display: enableNav ? 'initial' : 'none',}}
      >
        <DrawerHeader justify="center">
          <Tooltip title="Menu">
            <IconButton
              color="inherit"
              aria-label="open drawer"
              onClick={handleDrawer}
              edge={false}
              justify="center"
              sx={{
                mr:'2px',
              }}
            >
              <MenuIcon />
            </IconButton>
          </Tooltip>
        </DrawerHeader>
        <Divider />
        <List>
          <NavigationLink open={open} text="Main" Icon={LogoDevIcon} allowed={enableNav}/>  
          <NavigationLink open={open} text="Upload" Icon={FileUpload} allowed={enableNav}/>
          <NavigationLink open={open} text="Progress" Icon={TimelineIcon} allowed={enableNav}/>
          <NavigationLink open={open} text="Documents" Icon={ArticleIcon} allowed={enableNav}/>
          <Divider sx={{
            display: admin || researcher ? 'block' : 'none'
          }} />
          <NavigationLink open={open} text="File Download" Icon={FileDownloadIcon} allowed={researcher | admin}/>
          <NavigationLink open={open} text="Participants" Icon={GroupIcon} allowed={researcher | admin}/>
          <NavigationLink open={open} text="Feedback Models" Icon={BuildIcon} allowed={researcher | admin}/>
          <Divider sx={{
            display: admin ? 'block' : 'none'
          }} />
          <NavigationLink open={open} text="Users" Icon={PersonIcon} allowed={admin}/>
        </List>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <DrawerHeader />
        {children}
      </Box>
    </Box>
  );
}



Base.propTypes = {
  pageName: PropTypes.string,
  enableNav: PropTypes.bool,
  researcher: PropTypes.bool,
  admin: PropTypes.bool,
  //children:
}


export default Base