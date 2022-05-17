import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';


/**
 * 
 * @returns Upload Page
 */
import Typography from "@mui/material/Typography";
import {Button, TextField} from "@mui/material";
import {useState} from "react";

const FileUpload = () => {
    return(
        <div className='vertCenter'>
            <div className='upload'>
                <button className='innerUploadButton'>Choose a file</button>
                or drag it here.
            </div>
            <TextField label='dd/mm/yy' variant='outlined'/>
            <TextField label='course' variant='outlined'/>
        </div>
)};

const Upload = () => {
    //set title in parent 'base'
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('Upload');
    });

    const [rowList, setRowList] = useState([]);

    const addRow = e => {
        setRowList(rowList.concat(<FileUpload key={rowList.length} />));
    };

    return (
        <>
            <div className='title'>
                <Typography variant='h3'>Upload</Typography>
            </div>
            {FileUpload()}
            <div id='uploadRows'></div>
            {rowList}
            <Button onClick={addRow}>add</Button>
        </>
    );
}

export default Upload;