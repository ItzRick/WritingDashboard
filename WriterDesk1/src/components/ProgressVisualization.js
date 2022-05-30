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
  ]; //TODO: Retrieve document data



  return (<>
    <Plot
    data={[
      {
        x: documents.map(row => row.date),
        y: documents.map(row => row.scoreLanguage),
        mode: 'lines+markers',
        line: {color: '#648FFF'},
        marker: {color: '#B3C8FF', symbol: 'circle', size: 10, line:{color:'#648FFF', width: 2}},
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
        line: {color: '#FE6100'},
        marker: {color: '#FFA166', symbol: 'circle', size: 10, line:{color:'#FE6100', width: 2}},
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
        line: {color: '#DC267F'},
        marker: {color: '#ED91BE', symbol: 'circle', size: 10, line: {color:'#DC267F', width: 2}},
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
        line: {color: '#FFB000'},
        marker: {color: '#FFD780', symbol: 'circle', size: 10, line:{color:'#FFB000', width: 2}},
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
    onClick={
      (data) => alert(data.points[0].x) //TODO: Add onclick event to go to document page
    }
    /></>
  );
}


export default ProgressVisualization;