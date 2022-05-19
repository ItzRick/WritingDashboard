// materials
import { } from "@mui/material";

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';


import React from 'react';
import AllPagesPDFViewer from "../components/all-pages";
import samplePDF from "../example2.pdf";
import "../css/styles.css";


// /**
//  * 
//  * @returns Documents Page
//  */
// function Documents() {
//   //set title in parent 'base' 
//   const { setTitle } = useOutletContext();
//   useEffect(() => {
//     setTitle('Documents');
//   });
export default function Documents() {  
  return (
    <div className="App">
      <div className="all-page-container">
        <AllPagesPDFViewer pdf={samplePDF} />
      </div>
    </div>
  );
}

//export default Documents;