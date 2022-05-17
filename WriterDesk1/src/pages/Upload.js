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
        <div style={{marginBottom: '1vw'}}>
            <div className='vertCenter'>
                <div className='upload'>
                    <Button variant='contained' style={{marginRight: '8px'}}>Choose a file</Button>
                    or drag it here.
                </div>
                <TextField label='dd/mm/yy' variant='outlined' style={{marginRight: '1vw'}}/>
                <TextField label='course' variant='outlined'/>
            </div>
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
            <br />
            <div className='center'>
                {FileUpload()}
                {rowList}
                <Button variant='contained' color='secondary' onClick={addRow}>Add</Button>
            </div>
            <br />
            <div className='title'>
                <Button variant='contained' className='uploadButton' style={{fontSize: '2vw', textTransform: 'none'}}>
                    Upload your document(s)
                </Button>
            </div>
        </>
    );
}

export default Upload;