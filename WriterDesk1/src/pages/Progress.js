// materials
import {
    Typography
} from "@mui/material";
import Plot from 'react-plotly.js';

// routing
import {useOutletContext} from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import ProgressVisualization from "../components/ProgressVisualization";
import axios from "axios";


/**
 *
 * @returns Progress Page
 */
function Progress() {
    //set title in parent 'base' 
    const {setTitle} = useOutletContext();
    useEffect(() => {
        setTitle('Progress');
        fetchScores();
    });

    const [scoreStyle, setScoreStyle] = useState();
    const [scoreStructure, setScoreStructure] = useState();
    const [scoreCohesion, setScoreCohesion] = useState();
    const [scoreIntegration, setScoreIntegration] = useState();

    const fetchScores = () => {
        // // Url of the server:
        const url = 'https://127.0.0.1:5000/scoreapi//getAvgScores';

        // Make the call to the backend:
        axios.get(url, {params: {userId: 123}})
            .then((response) => {
                setScoreStyle(response.data.scoreStyle);
                setScoreStructure(response.data.scoreStructure);
                setScoreCohesion(response.data.scoreCohesion);
                setScoreIntegration(response.data.scoreIntegration);
            })
    }

    return (
        <>
            <div className='subTitle'>
                <Typography variant='h5'>Average score per skill category</Typography>
                <Plot
                    data={[
                        {
                            // Order of the bars is as follows: first source integration, then cohesion, then structure, then language & style:
                            x: ['Language & style', 'Cohesion', 'Structure', 'Source integration & <br> content'],
                            y: [scoreStyle, scoreCohesion, scoreStructure, scoreIntegration],
                            marker: {color: ['#785EF0', '#FE6100', '#FFB000', '#DC267F']},
                            type: 'bar',
                        },
                    ]}
                    // The title of the char is 'scores':
                    layout={{
                        title: 'Average scores',
                        // Scores can be between 0 and 10, so the y-axis range is set accordingly:
                        yaxis: {
                            range: [0, 10],
                            type: 'linear'
                        }
                    }}
                    // Do not display the plotly modebar:
                    config={{
                        displayModeBar: false, // this is the line that hides the bar.
                    }}
                    // So the chart can resize:
                    useResizeHandler={true}
                    style={{width: '100%', height: '50%'}}
                />
                <br/><br/>
                <Typography variant='h5'>Progress over time</Typography>
                <div className="plotContainer">
                    <ProgressVisualization/>
                </div>
            </div>
        </>
    );
}

export default Progress;