// materials
import {Typography} from "@mui/material";

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect, useState } from 'react';

// show pdf
import React from 'react';
import AllPagesPDFViewer from "../components/ShowPDF";
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

  useEffect(() => {
    setTitle('Document');    
  });

  // TODO take file path and file type from database 
  const path = 'C:\\Users\\20174066\\Documents\\School\\2IPE0_SEP\\SEP2021\\WriterDesk1\\src\\example6.txt'
  const type = 'txt'

  return (
      <>
          <div className="all-page-container">
            {/** potentially convert document to pdf and show document on page */}
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