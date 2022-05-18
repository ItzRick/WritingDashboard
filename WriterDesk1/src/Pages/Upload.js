// materials
import { 
    Typography,
    Button
} from "@mui/material";
import UploadSingleFile from "./../components/UploadSingleFile";


// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect, useState } from 'react';

/**
 * 
 * @returns File Upload page
 */
const Upload = () => {
    //set title in parent 'base'
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('Upload');
    });

    // list of UploadSingleFile objects
    const [uploadSingleFiles, setUploadSingleFiles] = useState([<UploadSingleFile key={0}/>]);

    // add UploadSingleFile object to rowList
    const addRow = e => {
        setUploadSingleFiles(uploadSingleFiles.concat(<UploadSingleFile key={uploadSingleFiles.length} />));
    };

    return (
        <>
            <div className='title'>
                <Typography variant='h3'>Upload</Typography>
            </div>
            <br />
            <div className='center'>
                {uploadSingleFiles}
                <Button variant='contained' sx={{bgcolor:'button.main', color: 'button.text'}} onClick={addRow}>Add</Button>
            </div>
            <br />
            <div className='title'>
                <Button variant='contained' sx={{bgcolor:'button.main', color: 'button.text'}} className='uploadButton' style={{fontSize: '2vw', textTransform: 'none'}}>
                    Upload your document(s)
                </Button>
            </div>
        </>
    );
}

export default Upload;