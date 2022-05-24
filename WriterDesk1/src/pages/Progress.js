// materials
import { 
    Typography 
} from "@mui/material";
import graphPlaceholder from '../images/chartImage.png';
import Plot from 'react-plotly.js';

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';



/**
 * 
 * @returns Progress Page
 */
function Progress() {
    //set title in parent 'base' 
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('Progress');
    });
    return (
        <>
            <div className='subTitle'>
                <Typography variant='h5'>Average score per skill category</Typography>
                <img src={graphPlaceholder} className='graph2' />
                <br /><br />
                <Typography variant='h5'>Progress over time</Typography>


                <Plot
                data={[
                  {
                    x: ['2020-10-04', '2021-11-04', '2023-12-04', '2023-12-04'],
                    y: [2, 6, 1.4],
                    mode: 'lines+markers',
                    line: {color: '#F5793A'},
                    marker: {color: '#f79c6e', symbol: 'circle', size: 10, line:{color:'#F5793A', width: 2}},
                    name: 'Language and Style',
                    hovertemplate: '<b>%{text}</b><br>Score: %{y}<br>%{x}',
                    text: ['Title1', 'Title2', ['Title3', 'Title4']]
                  },
                  {
                    x: ['2020-10-04', '2021-11-04', '2023-12-04', '2023-12-04'],
                    y: [3, 4, 2.5],
                    mode: 'lines+markers',
                    line: {color: '#A95AA1'},
                    marker: {color: '#c18abc', symbol: 'circle', size: 10, line:{color:'#A95AA1', width: 2}},
                    name: 'Cohesion',
                    hovertemplate: '<b>%{text}</b><br>Score: %{y}<br>%{x}',
                    text: ['Title1', 'Title2', ['Title3', 'Title4']]
                  },
                  {
                    x: ['2020-10-04', '2021-11-04', '2023-12-04', '2023-12-04'],
                    y: [2, 7, 8.1],
                    mode: 'lines+markers',
                    line: {color: '#85C0F9'},
                    marker: {color: '#cee6fd', symbol: 'circle', size: 10, line:{color:'#85C0F9', width: 2}},
                    name: 'Source integration and Content',
                    hovertemplate: '<b>%{text}</b><br>Score: %{y}<br>%{x}',
                    text: ['Title1', 'Title2', ['Title3', 'Title4']]
                  },
                  {
                    x: ['2020-10-04', '2021-11-04', '2023-12-04', '2023-12-04'],
                    y: [3, 10, 9.5],
                    mode: 'lines+markers',
                    line: {color: '#0F2080'},
                    marker: {color: '#324de7', symbol: 'circle', size: 10, line:{color:'#0F2080', width: 2}},
                    name: 'Structure',
                    hovertemplate: '<b>%{text}</b><br>Score: %{y}<br>%{x}',
                    text: ['Title1', 'Title2', ['Title3', 'Title4']]
                  }
                ]}
                layout={ {width: 1220, height: 400, hovermode:'closest',
                  yaxis: {
                    rangemode: 'tozero',
                    autotick: false,
                    range: [0, 10.5],
                    //tick0: 0,
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
                    //range: [0, 10],
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
                />



            </div>
        </>
    );
}

export default Progress;