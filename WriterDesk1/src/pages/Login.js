import './../css/main.css';

// materials 
import { 
    Button, 
    TextField, 
    Typography,
    IconButton 
} from "@mui/material";
import testImage from '../images/placeholder_image.png'

// routing
import { Link } from 'react-router-dom';


/**
 * 
 * @returns login page
 */
const Login = () => {

    return (
        <>
            <div className='parent'>
                <div className='div1'>
                    <IconButton style={{ float: 'left' }} component={Link} to='/LandingPage'>
                        <img className='logo' src={testImage} />
                    </IconButton>
                    <Typography variant='h3'>Login</Typography>
                    <div className='filler2'></div>
                </div>
                <div className='div2'>
                    <div className='text_boxes'>
                        <Typography>Username:</Typography>
                        <TextField id='username' label='Username' variant='outlined' />
                        <br />
                        <Typography>Password:</Typography>
                        <TextField id='password' label='Password' variant='outlined' type='password' />
                    </div>
                    <br />
                    <Button variant="contained" component={Link} to='/Main' sx={{bgcolor: 'button.main', color: 'button.text'}}>Log in</Button>
                </div>
                <div className='div3'>
                    <br />
                    <Typography>Don't have an account yet? Sign up <Link to={'/SignUp'}>here</Link>.</Typography>
                    <br />
                    Note: the TU/e mail is the username of TU/e students.
                </div>
            </div>
        </>
    );
}

export default Login;
