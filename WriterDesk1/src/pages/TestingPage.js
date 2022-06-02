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
        formData.append('scoreStyle', 0.1);
        formData.append('scoreCohesion', 0.2);
        formData.append('scoreStructure', 0.3);
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


    return (
        <>
            <Button onClick={uploadScore}>
                Send Some Scores
            </Button>

            <Button onClick={getScore}>
                Get Scores
            </Button>

            {Object.entries(data)
                .map(([key, value]) => <p key={key}>{key}: {value}</p>)
            }

        </>
    );
}




export default TestingPage;