// materials
import {Typography} from "@mui/material";

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';


import React from 'react';
import AllPagesPDFViewer from "../components/all-pages";
import samplePDF from "../example2.pdf";
import "../css/styles.css";
import "../css/main.css";
import placeholder from '../images/chartImage.png';


/**
 * 
 * @returns Documents Page
 */
function Documents() {
  //set title in parent 'base' 
  const { setTitle } = useOutletContext();
  useEffect(() => {
    setTitle('Documents');
  });
  return (
      <>
          <div className="pdfContainer">
            <AllPagesPDFViewer pdf={samplePDF} />
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

export default Documents;