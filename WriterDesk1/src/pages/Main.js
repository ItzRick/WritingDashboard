//import {Component, useEffect, useState} from 'react'
//import axios from "axios";
import './../css/App.css';

import Typography from '@mui/material/Typography';
import { Button } from "@mui/material";
import chartImg from '../images/chartImage.png';

import { Link } from 'react-router-dom';


const Main = () => {
  return (
    <div className='home_grid'>
      <div className='home1'>
        <Typography variant='h3'>Homepage</Typography>
      </div>
      <div className='home2'>
        <div className='vertCenter'>
          <Button variant='contained' className='uploadButton' style={{
            fontSize: '2vw', textTransform: 'none'
          }} component={Link} to='/Upload'>Upload a document</Button>
        </div>
      </div>
      <div className='home3'>
        <div className='vertCenter'>
          <Typography className='recent'><u style={{ color: 'blue' }}>Recent files</u>
            <br />TheFirstFile.docx
            <br />TheSecondFile.txt
            <br />TheThirdFile.pdf</Typography>
        </div>
      </div>
      <div className='home4'>
        <div className='subTitle'>
            <br />
            <Typography style={{ fontSize: '2vw' }}><u>Progress</u></Typography>
        </div>
        <div className='vertCenter'>
          <img className='graph' src={chartImg} />
        </div>
      </div>
    </div>
  );
}

export default Main;