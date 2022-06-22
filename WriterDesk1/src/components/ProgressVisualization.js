// materials
import {
    Typography
} from "@mui/material";
import graphPlaceholder from '../images/chartImage.png';
import Plot from 'react-plotly.js';
import './../css/main.css';

// routing
import { useNavigate } from 'react-router-dom';

/**
 * Line chart of progress
 * @returns ProgressVisualization Component
 */
const ProgressVisualization = () => {
  const navigate = useNavigate();

  const documents = [
    {id: 21, date: new Date('6/7/22'), Title: 'Title1', scoreLanguage: 6.5, scoreStructure: 5, scoreCohesion: 7, scoreSourceIntegration: 5.5},
    {id: 22, date: new Date('6/8/22'), Title: 'Title2', scoreLanguage: 7, scoreStructure: 5, scoreCohesion: 7.5, scoreSourceIntegration: 8},
    {id: 23, date: new Date('6/8/22'), Title: 'Title3', scoreLanguage: 7.5, scoreStructure: 6, scoreCohesion: 6, scoreSourceIntegration: 9},
    {id: 24, date: new Date('6/10/22'), Title: 'Title4', scoreLanguage: 8, scoreStructure: 5.5, scoreCohesion: 5.5, scoreSourceIntegration: 8},
    {id: 25, date: new Date('6/11/22'), Title: 'Title5', scoreLanguage: 9, scoreStructure: 6, scoreCohesion: 5, scoreSourceIntegration: 8.5},
    {id: 26, date: new Date('6/12/22'), Title: 'Title6', scoreLanguage: 9.5, scoreStructure: 7.4, scoreCohesion: 5.5, scoreSourceIntegration: 8}
  ]; //TODO: Retrieve document data. Has to be in order of date.


  /**
   * Function to navigate to the correct document when clicked on.
   * @param {Object} data - Object of data of the point that is clicked.
   */
  const handlePointClick = (data) => {
    navigate('/Document', {state: {fileId: documents[data.pointNumber].id}});
  }


  /**
   * Function to concat titles that are on the same date.
   * This is used to show multiple titles when hovering over a
   * point in the graph that corresponds with multiple documents.
   * @param {Array} dates - Array of sorted dates.
   * @param {Array} titles - Array of titles that corresponds to the dates. Must be of same length as array of dates
   * @returns {Array} Modified array of titles where title of the first document in a row of documents with the same date
   * contains all titles of those documents. Example: ['Title1', 'Title2, Title3', 'Title3']
   */
  const concatTitlesSameDate = (dates, titles) => {
    for (let i = 0; i < dates.length-1; i++) { // Loop over all documents
      if (dates[i] === dates[i+1]) {

        // If there are 2 documents with the same date, check if there are more with that date
        for (let n = i+1; n < dates.length-1; n++) {
          if (dates[n] === dates[i]) {
            titles[i] = titles[i] + ', ' + titles[n]; // For all the documents with the same date, concat titles
          } else {
            break;
          }
        }
      }
    }
    return(titles);
  }

  // Titles of documents for the hover text
  const mergedTitles = (concatTitlesSameDate(documents.map(row => row.date), documents.map(row => row.Title)));

  return (
    <Plot style={{ height: '100%', width: '80%', marginLeft: '14vw', minWidth: '500px' }}
    data={[
      {
        x: documents.map(row => row.date),
        y: documents.map(row => row.scoreLanguage),
        mode: 'lines+markers',
        line: {color: '#648FFF'},
        marker: {color: '#B3C8FF', symbol: 'circle', size: 10, line:{color:'#648FFF', width: 2}},
        name: 'Language and Style',
        hovertemplate: '<b>%{text}</b><br>Score: %{y}<br>%{x}',
        text: mergedTitles,
        transforms: [{
          type: 'aggregate',
          groups: documents.map(row => row.date),
          aggregations: [{target: 'y', func: 'avg', enabled: true}]
        }]
      },
      {
        x: documents.map(row => row.date),
        y: documents.map(row => row.scoreCohesion),
        mode: 'lines+markers',
        line: {color: '#FE6100'},
        marker: {color: '#FFA166', symbol: 'circle', size: 10, line:{color:'#FE6100', width: 2}},
        name: 'Cohesion',
        hovertemplate: '<b>%{text}</b><br>Score: %{y}<br>%{x}',
        text: mergedTitles,
        transforms: [{
          type: 'aggregate',
          groups: documents.map(row => row.date),
          aggregations: [{target: 'y', func: 'avg', enabled: true}]
        }]
      },
      {
        x: documents.map(row => row.date),
        y: documents.map(row => row.scoreSourceIntegration),
        mode: 'lines+markers',
        line: {color: '#DC267F'},
        marker: {color: '#ED91BE', symbol: 'circle', size: 10, line: {color:'#DC267F', width: 2}},
        name: 'Source integration<br>and Content',
        hovertemplate: '<b>%{text}</b><br>Score: %{y}<br>%{x}',
        text: mergedTitles,
        transforms: [{
          type: 'aggregate',
          groups: documents.map(row => row.date),
          aggregations: [{target: 'y', func: 'avg', enabled: true}]
        }]
      },
      {
        x: documents.map(row => row.date),
        y: documents.map(row => row.scoreStructure),
        mode: 'lines+markers',
        line: {color: '#FFB000'},
        marker: {color: '#FFD780', symbol: 'circle', size: 10, line:{color:'#FFB000', width: 2}},
        name: 'Structure',
        hovertemplate: '<b>%{text}</b><br>Score: %{y}<br>%{x}',
        text: mergedTitles,
        transforms: [{
          type: 'aggregate',
          groups: documents.map(row => row.date),
          aggregations: [{target: 'y', func: 'avg', enabled: true}]
        }]
      }
    ]}
    layout={ { hovermode:'closest', margin: {l: 30, r: 0, b: 30, t: 20, pad: 4}, legend:{font: {size: 12}, bgcolor: 'rgba(0, 0, 0, 0)',
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
        showspikes: false, //true
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