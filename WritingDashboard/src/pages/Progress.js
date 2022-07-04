// materials
import {
    Typography
} from "@mui/material";
import Plot from 'react-plotly.js';

// css
import "./../css/Progress.css";

// routing
import {useOutletContext} from 'react-router-dom';
import {useState, useEffect} from 'react';
import ProgressVisualization from "../components/ProgressVisualization";
import axios from "axios";
// Authentication service:
import { AuthenticationService } from "../services/authenticationService";
import { authHeader } from "../helpers/auth-header";


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

    /*
     * This function fetches the 5 most recent scores of each type from the database,
     * then calculates the averages and sets the variables.
     */
    const fetchScores = () => {
        // The userId of the current user:
        const userId = AuthenticationService.getCurrentUserId();
        // Url of the server:
        const url = '/api/scoreapi/getAvgScores';

        // Make the call to the backend:
        axios.get(url, {params: {userId: userId}, headers: authHeader() })
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
                <Typography variant='h5'>Average scores of the last 5 documents</Typography>
                <div className="plotContainerAverage">
                    <Plot
                        data={[
                            {
                                // Order of the bars is as follows: first source integration, then cohesion, then structure, then language & style:
                                x: ['Language & Style', 'Cohesion', 'Structure', 'Source Integration & <br> Content'],
                                y: [scoreStyle, scoreCohesion, scoreStructure, scoreIntegration],
                                marker: {color: ['#785EF0', '#FE6100', '#FFB000', '#DC267F']},
                                type: 'bar',
                            },
                        ]}
                        // The title of the char is 'scores':
                        layout={{
                            margin: {l: 80, r: 70, b: 35, t: 20, pad: 4},
                            // Scores can be between 0 and 10, so the y-axis range is set accordingly:
                            yaxis: {
                                range: [0, 10],
                                fixedrange: true,
                                type: 'linear'
                            },
                            xaxis: {
                                fixedrange: true,
                            }
                        }}
                        // Do not display the plotly modebar:
                        config={{
                            displayModeBar: false, // this is the line that hides the bar.
                        }}
                        // So the chart can resize:
                        useResizeHandler={true}
                        style={{width: '100%', height: '100%'}}
                        onHover={e => {
                            e.event.target.style.cursor = 'pointer' // Changes cursor on hover to pointer
                        }}
                        onUnhover={e => {
                            e.event.target.style.cursor = 'default' // Change cursor back on unhover
                        }}
                    />
                </div>
                <Typography variant='h5'>Progress over time</Typography>
                <div className="plotContainerLine">
                    <ProgressVisualization/>
                </div>
            </div>
        </>
    );
}

export default Progress;