// materials
import {
    Typography
} from "@mui/material";
import graphPlaceholder from '../images/chartImage.png';
import Plot from 'react-plotly.js';


/**
 * Line chart of progress
 * @returns ProgressVisualization Component
 */
const ProgressVisualization = () => {
  const documents = [
    {id: 1, date: '2020-10-04', Title: 'Title1', scoreLanguage: 6.5, scoreStructure: 5, scoreCohesion: 7, scoreSourceIntegration: 5.5},
    {id: 2, date: '2021-11-04', Title: 'Title2', scoreLanguage: 7, scoreStructure: 5, scoreCohesion: 7.5, scoreSourceIntegration: 8},
    {id: 3, date: '2022-12-04', Title: 'Title3', scoreLanguage: 7.5, scoreStructure: 6, scoreCohesion: 6, scoreSourceIntegration: 9},
    {id: 4, date: '2022-12-04', Title: 'Title4', scoreLanguage: 8, scoreStructure: 5.5, scoreCohesion: 5.5, scoreSourceIntegration: 8},
    {id: 4, date: '2023-01-04', Title: 'Title5', scoreLanguage: 9, scoreStructure: 6, scoreCohesion: 5, scoreSourceIntegration: 8.5},
    {id: 4, date: '2023-03-04', Title: 'Title6', scoreLanguage: 9.5, scoreStructure: 7.4, scoreCohesion: 5.5, scoreSourceIntegration: 8}
  ];



  return (<>
    <Plot
    data={[
      {
        x: documents.map(row => row.date),
        y: documents.map(row => row.scoreLanguage),
        mode: 'lines+markers',
        line: {color: '#F5793A'},
        marker: {color: '#f79c6e', symbol: 'circle', size: 10, line:{color:'#F5793A', width: 2}},
        name: 'Language and Style',
        hovertemplate: '<b>%{text}</b><br>Score: %{y}<br>%{x}',
        text: documents.map(row => row.Title),
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
        line: {color: '#A95AA1'},
        marker: {color: '#c18abc', symbol: 'circle', size: 10, line:{color:'#A95AA1', width: 2}},
        name: 'Cohesion',
        hovertemplate: '<b>%{text}</b><br>Score: %{y}<br>%{x}',
        text: documents.map(row => row.Title),
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
        line: {color: '#85C0F9'},
        marker: {color: '#cee6fd', symbol: 'circle', size: 10, line: {color:'#85C0F9', width: 2}},
        name: 'Source integration<br>and Content',
        hovertemplate: '<b>%{text}</b><br>Score: %{y}<br>%{x}',
        text: documents.map(row => row.Title),
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
        line: {color: '#0F2080'},
        marker: {color: '#324de7', symbol: 'circle', size: 10, line:{color:'#0F2080', width: 2}},
        name: 'Structure',
        hovertemplate: '<b>%{text}</b><br>Score: %{y}<br>%{x}',
        text: documents.map(row => row.Title),
        transforms: [{
          type: 'aggregate',
          groups: documents.map(row => row.date),
          aggregations: [{target: 'y', func: 'avg', enabled: true}]
        }]
      }
    ]}
    layout={ {width: 1120, height: 400, hovermode:'closest', margin: {l: 30, r: 0, b: 30, t: 20, pad: 4},
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
        showspikes: true,
        spikecolor: 'black',
        spikemode: 'toaxis+across',
        spikethickness: 1
      }
    } }
    config={{ modeBarButtonsToRemove: ['toImage', 'lasso2d', 'select2d', 'resetScale2d'], displaylogo: false }}
    onClick={(data) => alert(data.points[0].x)}
    /></>
  );
}


export default ProgressVisualization;