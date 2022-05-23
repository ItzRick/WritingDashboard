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

  const path = 'C:\\Users\\20192543\\Documents\\GitHub\\SEP2021\\WriterDesk1\\src\\example3.docx'
  const type = 'docx'
  return (
      <>
        {/* Div for the pdf file: */}
      <div sx={{
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'space-between',
      }}>
          <div className="allPageContainer" >
            <AllPagesPDFViewer pdf={`http://127.0.0.1:5000/converttopdf/convert?filepath=${path}&filetype=${type}`} />
          </div>
          {/* Div for the sidebar: */}
          <div className='sideBar'>
              {/* The actual barchart, with the colors as required by the design and score as set in the currentData state: */}
            <Plot
                data={[
                    {
                        // Order of the bars is as follows: first source integration, then cohesion, then structure, then language & style:
                    x: ['Source integration & <br> content', 'Cohesion', 'Structure', "Language & style"],
                    y: currentData,
                    marker: {color: ['#F5793A', '#A95AA1', '#85C0F9', '#0F2080']},
                    type: 'bar',
                    },
                ]}
                // The title of the char is 'scores':
                layout={ {title: 'Scores',
                // Scores can be between 0 and 10, so the y-axis range is set accordingly: 
                yaxis: {
                    range: [0, 10],
                    type: 'linear'
                }} }
                // Do not display the plotly modebar:
                config= {{
                    displayModeBar: false, // this is the line that hides the bar.
                }}
                // So that you can do stuff if you click on a bar (TODO: remove):
                onClick={(data) => {
                    console.log("data", data.points[0].pointNumber)
                }}
                // So the chart can resize:
                useResizeHandler={true}
                style={{width: '100%', height: '50%'}}
                />
              {/* <img className='smallGraph' src={placeholder} /> */}
              <br />
              <Typography className='textBoxExpl'>Sample text</Typography>
          </div>
    </div>
  );
}

export default Document;