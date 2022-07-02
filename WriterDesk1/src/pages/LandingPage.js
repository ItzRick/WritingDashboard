import './../css/LoginSignUp.css';

// materials
import {
  Typography,
  Box,
} from "@mui/material";
import logo from '../images/logo.png'
import BlueButton from "./../components/BlueButton";
import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';

/**
 * 
 * @returns landing page, main page when not logged in
 */
const LandingPage = () => {
  //set title in parent 'base' 
  const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('');
    });

  return (
    <Box classname='center'>
      <Box className='center'>
        <Box sx={{
          display: 'inline-flex',
        }}>
          <Typography className='titleChild' variant='h2'> Writing </Typography>
          <img className='logo titleChild' src={logo} alt='' />
          <Typography variant='h2' className='titleChild'> Dashboard </Typography>
        </Box>
      </Box>
      <br />
      <Typography variant='h5'>Improve your academic writing.</Typography>
      <br />
      <div className='center'>
        <BlueButton idStr='loginButton' pathName='/Login'>Log in</BlueButton>
        <div className='filler'></div>
        <BlueButton idStr='signupButton' pathName='/SignUp'>Sign up</BlueButton>
      </div>
      <br /><br />
      <div className='center'>
        <span className='textbox'>
          In this application, TU/e students can improve their academic writing.
          This is done by uploading documents which have been written during their studies.
          After the document has been uploaded, feedback will be generated.
          The student can view the feedback, which includes the feedback scores.
          After uploading multiple documents, the students can view their progress over time.
        </span>
      </div>
    </Box>
  );
}

export default LandingPage;