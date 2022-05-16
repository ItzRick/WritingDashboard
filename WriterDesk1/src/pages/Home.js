//import {Component, useEffect, useState} from 'react'
//import axios from "axios";
import './../css/App.css';
import Base from './../components/Base.js'

import Typography from '@mui/material/Typography';
import {Button} from "@mui/material";
import chartImg from '../images/chartImage.png';

function App() {

  return (
    <Base pageName='' enableNav={true} researcher={true} admin={true}>
        <div className='home_grid'>
            <div className='home1'>
                <Typography variant='h3'>Homepage</Typography>
            </div>
            <div className='home2'>
                <div className='vertCenter'>
                    <Button variant='contained' className='uploadButton' style={{
                        fontSize: '2vw', textTransform: 'none'}}>Upload a document</Button>
                </div>
            </div>
            <div className='home3'>
                <div className='vertCenter'>
                    <Typography class='recent'><u style={{color: 'blue'}}>Recent files</u>
                    <br />TheFirstFile.docx
                    <br />TheSecondFile.txt
                    <br />TheThirdFile.pdf</Typography>
                </div>
            </div>
            <div className='home4'>
                <div className='subTitle'>
                    <Typography style={{fontSize: '2vw'}}><u>Progress</u></Typography>
                </div>
                <div className='vertCenter'>
                    <img class='graph' src={chartImg} />
                </div>
            </div>
        </div>
    </Base>
  );
 }

 export default App;