//import {Component, useEffect, useState} from 'react'
//import axios from "axios";
import './../css/LoginSignUp.css';

import Typography from '@mui/material/Typography';
import {Button} from "@mui/material";

function ExamplePage() {

  return (
    <>
        <Typography variant='h2'>Writing Dashboard</Typography>
        <br />
        <Typography variant='h5'>Improve your academic writing.</Typography>
        <br />
        <div className='center'>
            <Button size='large' variant='contained'>Log in</Button>
            <div className='filler'></div>
            <Button size='large' variant='contained'>Sign up</Button>
        </div>
        <br /><br />
        <div className='center'>
            <span className='textbox'>In this application, TU/e students can improve their academic writing.
                This is done by uploading documents which have been written during their studies.
                After the document has been uploaded, feedback will be generated.
                The student can view the feedback, which includes the feedback scores.
                After uploading multiple documents, the students can view their progress over time.
                Lorem ipsum, lorem ipsum. EXAMPLE </span>
        </div>
    </>
  );
 }

 export default ExamplePage;