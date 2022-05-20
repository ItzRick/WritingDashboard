// materials
import {Typography} from "@mui/material";

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';

import React from 'react';
import AllPagesPDFViewer from "../components/all-pages";
import "../css/styles.css";
import "../css/main.css";
import placeholder from '../images/chartImage.png';


/**
 *
 * @returns Documents Page
 */
function Document() {
  //set title in parent 'base'
  const { setTitle } = useOutletContext();

    const [file, setFile] = useState('');
  useEffect(() => {
    setTitle('Document');    
  });

  const path = 'C:\\Users\\20192435\\Downloads\\SEP2021\\WriterDesk1\\src\\example3.docx'
  const type = 'docx'
  return (
      <>
          <div className="all-page-container">
            <AllPagesPDFViewer pdf={`http://127.0.0.1:5000/converttopdf/convert?filepath=${path}&filetype=${type}`} />
          </div>
          <div className='rightFloat'>
              <img className='smallGraph' src={placeholder} />
              <br />
              <div className='textBoxExpl'>
                  <Typography>Sample text</Typography>
              </div>
          </div>
      </>

  );
}

export default Document;