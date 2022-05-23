// materials
import {Typography} from "@mui/material";

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect, useState } from 'react';

import React from 'react';
import AllPagesPDFViewer from "../components/all-pages";
import "../css/styles.css";
import "../css/main.css";
import placeholder from '../images/chartImage.png';
import Plot from 'react-plotly.js';


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

    // State to save the data to display in the barchart in: 
    const [currentData, setCurrentData] = useState([2, 6, 3, 4])

  const path = 'C:\\Users\\20192435\\Downloads\\SEP2021\\WriterDesk1\\src\\example3.docx'
  const type = 'docx'
  return (
      <>
          <div className="allPageContainer" >
            <AllPagesPDFViewer pdf={`http://127.0.0.1:5000/converttopdf/convert?filepath=${path}&filetype=${type}`} />
          </div>
          <div className='sideBar'>
            <Plot
                data={[
                    {
                    x: ['Source integration & <br> content', 'Cohesion', 'Structure', "Language & style"],
                    y: currentData,
                    marker: {color: ['#F5793A', '#A95AA1', '#85C0F9', '#0F2080']},
                    type: 'bar',
                    },
                ]}
                layout={ {title: 'Scores', 
                yaxis: {
                    range: [0, 10],
                    type: 'linear'
                }} }
                config= {{
                    displayModeBar: false, // this is the line that hides the bar.
                }}
                onClick={(data) => {
                    console.log("data", data.points[0].pointNumber)
                }}
                useResizeHandler={true}
                style={{width: '40vw', height: '50vh'}}
                />
              {/* <img className='smallGraph' src={placeholder} /> */}
              <br />
              <div className='textBoxExpl'>
                  <Typography>Sample text</Typography>
              </div>
          </div>
    </>
  );
}

export default Document;