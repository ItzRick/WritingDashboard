// materials
import Plot from 'react-plotly.js';
import './../css/main.css';

// routing
import { useNavigate } from 'react-router-dom';
import {useEffect, useState} from "react";
import axios from "axios";
import {authHeader} from "../helpers/auth-header";

/**
 * Line chart of progress
 * @returns ProgressVisualization Component
 */
const ProgressVisualization = () => {
  const navigate = useNavigate();

  const [dateCorrectFormat, setDateCorrectFormat] = useState();  // List of dates in correct format
  const [mergedTitles, setMergedTitles] = useState();  // Titles of documents for the hover text

  // Dictionary of all documents and scores that are shown in the line chart
  const [documents, setDocuments] = useState({'id': [], 'filename': [], 'date': [], 'scoreStyle': [],
                                              'scoreCohesion': [], 'scoreStructure': [], 'scoreIntegration': []});


  /**
   * Function to retrieve all documents and corresponding scores for the current user from the database.
   */
  const fetchFilesAndScores = () => {
    // Url of the server:
    const url = 'https://127.0.0.1:5000/scoreapi/getFilesAndScoresByUser';

    // Make the backend call and set the documents variable:
    axios.get(url, {headers: authHeader()}).then((response) => {
      setDocuments(response.data)
    })

  }

  useEffect(() => {
    fetchFilesAndScores()  // Retrieve documents and scores
  }, []);

  useEffect(() => {
    const newDateList = []  // Create new array for dates in correct format
    documents['date'].forEach((date, i) => {
      newDateList[i] = new Date(date)  // Set array in date format
    })
    setDateCorrectFormat(newDateList)  // Set dates as date object instead of string
  }, [documents]);

  useEffect(() => {
    // Run concatTitlesSameDate function to show correct information on hover
    setMergedTitles(concatTitlesSameDate(dateCorrectFormat, documents['filename']))
  }, [dateCorrectFormat, documents]);


  /**
   * Function to navigate to the correct document when clicked on.
   * @param {Object} data - Object of data of the point that is clicked.
   */
  const handlePointClick = (data) => {
    navigate('/Document', {state: {fileId: documents['id'][data.pointNumber]}});
  }


  /**
   * Function to concat titles that are on the same date.
   * This is used to show multiple titles when hovering over a
   * point in the graph that corresponds with multiple documents.
   * @param {Array} dates - Array of sorted dates.
   * @param {Array} titles - Array of titles that corresponds to the dates. Must be of same length as array of dates
   * @returns {Array} Array of titles where title of the first document in a row of documents with the same date
   * contains all titles of those documents. Example: ['Title1', 'Title2, Title3', 'Title3']
   */
  const concatTitlesSameDate = (dates, titles) => {
    // Check if titles or dates variable is undefined.
    if (titles === undefined || dates === undefined) {
      return titles;
    }

    let newTitles = [...titles]
      for (let i = 0; i < dates.length-1; i++) { // Loop over all documents
        if (dates[i].getTime() === dates[i+1].getTime()) {
          // If there are 2 documents with the same date, check if there are more with that date
          for (let n = i+1; n <= dates.length-1; n++) {
            if (dates[i].getTime() === dates[n].getTime()) {
              newTitles[i] = titles[i] + ', ' + titles[n]; // For all the documents with the same date, concat titles
            } else {
              break;
            }
          }
        }
     }
    return(newTitles);
  }


  return (
    <Plot style={{ height: '100%', width: '80%', marginLeft: '14vw', minWidth: '500px' }}
    data={[
      {
        x: dateCorrectFormat,
        y: documents['scoreStyle'],
        mode: 'lines+markers',
        line: {color: '#785EF0'},
        marker: {color: '#B1A2F6', symbol: 'circle', size: 10, line:{color:'#785EF0', width: 2}},
        name: 'Language & Style',
        hovertemplate: '<b>%{text}</b><br>Score: %{y}<br>%{x}',
        text: mergedTitles,
        transforms: [{
          type: 'aggregate',
          groups: dateCorrectFormat,
          aggregations: [{target: 'y', func: 'avg', enabled: true}]
        }]
      },
      {
        x: dateCorrectFormat,
        y: documents['scoreCohesion'],
        mode: 'lines+markers',
        line: {color: '#FE6100'},
        marker: {color: '#FFA166', symbol: 'circle', size: 10, line:{color:'#FE6100', width: 2}},
        name: 'Cohesion',
        hovertemplate: '<b>%{text}</b><br>Score: %{y}<br>%{x}',
        text: mergedTitles,
        transforms: [{
          type: 'aggregate',
          groups: dateCorrectFormat,
          aggregations: [{target: 'y', func: 'avg', enabled: true}]
        }]
      },
      {
        x: dateCorrectFormat,
        y: documents['scoreIntegration'],
        mode: 'lines+markers',
        line: {color: '#DC267F'},
        marker: {color: '#ED91BE', symbol: 'circle', size: 10, line: {color:'#DC267F', width: 2}},
        name: 'Source Integration<br>& Content',
        hovertemplate: '<b>%{text}</b><br>Score: %{y}<br>%{x}',
        text: mergedTitles,
        transforms: [{
          type: 'aggregate',
          groups: dateCorrectFormat,
          aggregations: [{target: 'y', func: 'avg', enabled: true}]
        }]
      },
      {
        x: dateCorrectFormat,
        y: documents['scoreStructure'],
        mode: 'lines+markers',
        line: {color: '#FFB000'},
        marker: {color: '#FFD780', symbol: 'circle', size: 10, line:{color:'#FFB000', width: 2}},
        name: 'Structure',
        hovertemplate: '<b>%{text}</b><br>Score: %{y}<br>%{x}',
        text: mergedTitles,
        transforms: [{
          type: 'aggregate',
          groups: dateCorrectFormat,
          aggregations: [{target: 'y', func: 'avg', enabled: true}]
        }]
      }
    ]}
    layout={ { hovermode:'closest', margin: {l: 30, r: 0, b: 35, t: 20, pad: 4}, legend:{font: {size: 12}, bgcolor: 'rgba(0, 0, 0, 0)',
		xanchor: "left",
		yanchor: "center"},
      yaxis: {
        rangemode: 'tozero',
        autotick: false,
        range: [0, 10.5],
        dtick: 1,
        tickwidth: 1,
        ticklen: 6,
        showgrid: true,
        fixedrange: true,

      },
      xaxis: {
        rangemode: 'tozero',
        autotick: true,
        type: 'date',
        showgrid: true,
        hoverformat: '%d-%m-%Y',
        showspikes: false,
        spikecolor: 'black',
        spikemode: 'toaxis+across',
        spikethickness: 1
      }
    } }
    config={{ modeBarButtonsToRemove: ['toImage', 'lasso2d', 'select2d', 'resetScale2d'], displaylogo: false, responsive: true}}
    onClick={
      (data) => handlePointClick(data.points[0]) // Call function to handle point click
    }
    onHover={e => {
      e.event.target.style.cursor = 'pointer' // Changes cursor on hover to pointer
    }}
    onUnhover={e => {
      e.event.target.style.cursor = 'ew-resize' // Change cursor back on unhover
    }}
    />
  );
}


export default ProgressVisualization;