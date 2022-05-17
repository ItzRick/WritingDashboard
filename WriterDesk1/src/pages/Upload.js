import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';



/**
 * 
 * @returns Upload Page
 */
import Typography from "@mui/material/Typography";
import {Button, TextField} from "@mui/material";
import {useState} from "react";


const Upload = () => {
    //set title in parent 'base'
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('Upload');
    });

    const [rowList, setRowList] = useState([]);

    const addRow = event => {
        setRowList(rowList.concat(<fileUpload key={rowList.length}/>));
    };

    return (
        <>
            <div className='title'>
                <Typography variant='h3'>Upload</Typography>
            </div>
            {fileUpload()}
            <div id='uploadRows'></div>
            {rowList}
            <Button onClick={addRow}>add</Button>
        </>
    );
}

const fileUpload = () => {
    return <div>
        <div className='vertCenter'>
            <div className='upload'>
                <button className='innerUploadButton'>Choose a file</button>
                or drag it here.
            </div>
            <TextField label='dd/mm/yy' variant='outlined'/>
            <TextField label='course' variant='outlined'/>
        </div>
    </div>
};

export default Upload;