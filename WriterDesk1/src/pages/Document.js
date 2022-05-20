// materials
import {Typography} from "@mui/material";

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';


import React from 'react';
import AllPagesPDFViewer from "../components/all-pages";
import samplePDF from "../example2.pdf";
import sampleDOCX from "../example3.pdf";
import sampleTXT from "../example4.pdf";
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
  return (
      <>
          <div className="all-page-container">
            <AllPagesPDFViewer pdf={sampleTXT} />
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