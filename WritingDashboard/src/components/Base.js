import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

// components
import NavigationLink from "./NavigationLink";
import { styled, useTheme } from '@mui/material/styles';
import {
  Tooltip,
  Box,
  Drawer,
  AppBar,
  Toolbar,
  List,
  CssBaseline,
  Typography,
  Divider,
  IconButton,
} from '@mui/material';
import {
  Menu,
  FileUpload,
  Timeline,
  Article,
  Group,
  Build,
  Person,
  Settings,
  ListAlt,
  Home,
} from '@mui/icons-material';

// routing
import { Link, Outlet, useNavigate } from 'react-router-dom';

// tracking
import { useContext } from 'react';
import { TrackingContext } from '@vrbo/react-event-tracking';

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
const CustomDrawerHeader = styled('div', { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    display: 'flex',
    alignItems: 'center',
    padding: theme.spacing(0, 1),
    justifyContent: 'center',
    ...(open && {
      justifyContent: 'flex-end',
    }),
    ...(!open && {
      justifyContent: 'center',
    }),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar,
  }));

/**
 * Makes styled AppBar
 */
const CustomAppBar = styled(AppBar, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
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
 * @param {bool} enableNav - The navigation drawer, on the left, is visible
 * @returns Base page for logged in user
 */
const Base = ({
  enableNav = true,
}) => {

  // context as given by the Tracking Provider
  const tc = useContext(TrackingContext);

  const [admin, setAdmin] = useState(false); // true when user has admin rights
  const [researcher, setResearcher] = useState(false); // true when user has researcher rights

  //handle opening and closing the drawer (left side menu)
  const [open, setOpen] = useState(false);
  const handleDrawer = () => {
    setOpen(!open);
    // handle tracking when the drawer is used
    if (tc.hasProvider) {
      tc.trigger({
        eventType: 'click.button', //send eventType
        buttonId: 'drawerHandle', //send buttonId
      })
    }
  };

  // provides title to the base page using the context of the outlet
  const [title, setTitle] = useState("");

  // general theme, defined in index.js
  const theme = useTheme();

  let navigate = useNavigate();

  // give rights depending on the role of the user that is logged in
  // manage admin and researcher sidebar visibility
  useEffect(() => {
    const user = JSON.parse(localStorage.getItem('currentUser'));
    if (user === null) {
      navigate("../Login", { replace: true });
    } else {
      if (user.role === 'admin') {
        setAdmin(true);
      }
      if (user.role === 'researcher' || user.role === 'admin') {
        setResearcher(true);
      }
    }
  }, []);

  return (
    <Box sx={{ display: 'flex' }} color="textPrimary" className='baseRoot'>
      <CssBaseline />
      <CustomAppBar
        position='fixed'
        sx={{
          bgcolor: 'appBar.background',
          ...(open && { width: `calc(100% - ${drawerWidth}px)`, ml: `${drawerWidth}px` }),
          ...(!open && {
            width: enableNav ? `calc(100% - ${theme.spacing(7)} + 1px)` : `100%`,
            [theme.breakpoints.up('sm')]: {
              width: enableNav ? `calc(100% - ${theme.spacing(8)} + 1px)` : `100%`,
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
          <Settings style={{ opacity: '0', margin: '8' }} />
          <Typography variant="h6" component="div" sx={{ color: "appBar.text", }}> {title} </Typography>
          <Tooltip title="Settings">
            <IconButton
              id='settings'
              sx={{
                justifySelf: "flex-end",
                color: "appBar.icon",
              }}
              onClick={() => {
                // handle tracking when the link is activated
                if (tc.hasProvider) {
                  tc.trigger({
                    eventType: 'click.link', //send eventType
                    buttonId: 'Settings', //send buttonId
                    linkPath: '/Settings' //send linkPath
                  })
                }
              }}
              component={Link} to='/Settings'
            >
              <Person />
            </IconButton>
          </Tooltip>
        </Toolbar>
      </CustomAppBar>

      <CustomDrawer
        variant="permanent"
        open={open}
        sx={{
          display: enableNav ? 'initial' : 'none',
          bgcolor: 'drawer.background',
          height: '100%',
        }}
      >
        <CustomDrawerHeader
          open={open}
          sx={{
            bgcolor: 'drawer.background',
          }}
        >
          <Tooltip title="Menu">
            <IconButton
              sx={{
                color: 'drawer.burger',
                bgcolor: 'inherit',
              }}
              aria-label="open drawer"
              onClick={handleDrawer}
              edge={false}
            >
              <Menu />
            </IconButton>
          </Tooltip>
        </CustomDrawerHeader>
        <Divider sx={{ bgcolor: 'drawer.divider', }} />
        <List
          sx={{
            bgcolor: 'drawer.background',
            height: '100%',
          }}>
          <NavigationLink open={open} text="Main" Icon={Home} allowed={enableNav} pageLink='Main' />
          <NavigationLink open={open} text="Upload" Icon={FileUpload} allowed={enableNav} pageLink='Upload' />
          <NavigationLink open={open} text="Progress" Icon={Timeline} allowed={enableNav} pageLink='Progress' />
          <NavigationLink open={open} text="Documents" Icon={Article} allowed={enableNav} pageLink='Documents' />
          <Divider sx={{
            bgcolor: 'drawer.divider',
            display: admin || researcher ? 'block' : 'none'
          }} />
          <NavigationLink open={open} text="Participants" Icon={Group} allowed={researcher | admin} pageLink='Participants' />
          <NavigationLink open={open} text="Projects" Icon={ListAlt} allowed={researcher | admin} pageLink='Projects' />
          <NavigationLink open={open} text="Feedback Models" Icon={Build} allowed={researcher | admin} pageLink='FeedbackModels' />
          <Divider sx={{
            bgcolor: 'drawer.divider',
            display: admin ? 'block' : 'none'
          }} />
          <NavigationLink open={open} text="Users" Icon={Settings} allowed={admin} pageLink='Users' />
        </List>
      </CustomDrawer>

      <Box component="main" sx={{ flexGrow: 1, p: 3 }} >
        <CustomDrawerHeader />
        <Box className='content' sx={{ height: '93.5%' }}>
          <Outlet context={{ setTitle }} />
        </Box>
      </Box>
    </Box>
  );
}



Base.propTypes = {
  enableNav: PropTypes.bool,
  researcher: PropTypes.bool,
  admin: PropTypes.bool,
  //children:
}


export default Base