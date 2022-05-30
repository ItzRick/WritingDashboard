import './../css/LoginSignUp.css';

// materials
import {
  Button,
  Typography,
  Box,
} from "@mui/material";
import logo from '../images/logo.png'

// routing
import { Link } from 'react-router-dom';

/**
 * 
 * @returns landing page, main page when not logged in
 */
const LandingPage = () => {

  return (
    <Box classname='center'>
      <Box className='center'>
        <Box sx={{
          display: 'inline-flex',
        }}>
          <Typography className='titleChild' variant='h2'> Writing </Typography>
          <img className='logo titleChild' src={logo} />
          <Typography variant='h2' className='titleChild'> Dashboard </Typography>
        </Box>
      </Box>
      <br />
      <Typography variant='h5'>Improve your academic writing.</Typography>
      <br />
      <div className='center'>
        <Button size='large' sx={{ bgcolor: 'button.main', color: 'button.text' }} variant='contained' component={Link} to={'/Login'}>Log in</Button>
        <div className='filler'></div>
        <Button size='large' sx={{ bgcolor: 'button.main', color: 'button.text' }} variant='contained' component={Link} to={'/SignUp'}>Sign up</Button>
      </div>
      <br /><br />
      <div className='center'>
        <span className='textbox'>
          In this application, TU/e students can improve their academic writing.
          This is done by uploading documents which have been written during their studies.
          After the document has been uploaded, feedback will be generated.
          The student can view the feedback, which includes the feedback scores.
          After uploading multiple documents, the students can view their progress over time.
          Lorem ipsum, lorem ipsum.
        </span>
      </div>
    </Box>
  );
}

export default LandingPage;