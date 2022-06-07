import {
    Button
} from "@mui/material";
import TestingComponent from "./../components/TestingComponent";
import axios from 'axios';

import { useState } from 'react';

/**
 * page used for testing, to be removed later
 * 
 * @returns Testing Page
 */
const TestingPage = () => {

    const uploadScore = () => {
        // url of the file api's upload function
        const url = 'https://localhost:5000/scoreapi/setScore';

        // create form with all the file information
        const formData = new FormData();
        formData.append('fileId', 3);
        formData.append('scoreStyle', 10);
        formData.append('scoreCohesion', 1);
        formData.append('scoreStructure', 0.1);
        formData.append('scoreIntegration', 0.4);
        //add header
        const headers = {
            Accept: 'application/json',
            'Content-Type': 'multipart/form-data',
        }

        //post the file
        axios.post(url, formData, headers).catch((error) => {
            console.log(error.response.data);
        });
    }

    const [data, setData] = useState([]);
    const [dataEx, setDataEx] = useState([]);
    const [dataEx2, setDataEx2] = useState([]);

    const getScore = () => {
        // url of the file api's upload function
        const url = 'https://localhost:5000/scoreapi/getScores';

        const params = {
            fileId: 3,
        }
        axios.get(url, { params })
            .then((response) => {
                setData(response.data)
            })
    }

    const uploadExplanation = () => {
        // url of the file api's upload function
        const url = 'https://localhost:5000/scoreapi/setExplanation';

        // create form with all the file information
        const formData = new FormData();
        formData.append('fileId', 3);
        formData.append('explId', 1);
        formData.append('type', 0);
        formData.append('explanation', 'When will you learn');
        formData.append('mistakeText', 'wooo');
        formData.append('X1', 0);
        formData.append('X2', 0);
        formData.append('Y1', 0);
        formData.append('Y2', 0);
        formData.append('replacement1', 0);
        formData.append('replacement2', 0);
        formData.append('replacement3', 0);
        //add header
        const headers = {
            Accept: 'application/json',
            'Content-Type': 'multipart/form-data',
        }

        //post the file
        axios.post(url, formData, headers).catch((error) => {
            console.log(error.response.data);
        });
    }

    const getExplanation = () => {
        // url of the file api's upload function
        const url = 'https://localhost:5000/scoreapi/getExplanation';

        const params = {
            fileId: 3,
            explId: 0,
        }
        axios.get(url, { params })
            .then((response) => {
                setDataEx(response.data)
            })
    }

    const getExplanations = () => {
        // url of the file api's upload function
        const url = 'https://localhost:5000/scoreapi/getExplanationForFile';

        const params = {
            fileId: 3,
        }
        axios.get(url, { params })
            .then((response) => {
                console.log(response.data)
                setDataEx2(response.data)
            })
    }




    return (
        <>
            <div>
                <Button onClick={uploadScore}>
                    Send Some Scores
                </Button>

                <Button onClick={getScore}>
                    Get Scores
                </Button>

                {Object.entries(data)
                    .map(([key, value]) => <p key={key}>{key}: {value}</p>)
                }
            </div>
            <div>
                <Button onClick={uploadExplanation}>
                    Murica Explain
                </Button>

                <Button onClick={getExplanation}>
                    Get Explain
                </Button>
                {Object.entries(dataEx)
                    .map(([key, value]) => <p key={key}>{key}: {value}</p>)
                }
            </div>
            <div>
                <Button onClick={getExplanations}>
                    Get All Expls
                </Button>
                 See console for result of this button
            </div>

        </>
    );
}




export default TestingPage;