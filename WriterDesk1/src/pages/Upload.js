// materials
import { 
    Typography,
    Button
} from "@mui/material";
import UploadSingleFile from "./../components/UploadSingleFile";
import useDynamicRefs from 'use-dynamic-refs';


// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect, useState, useRef, createRef } from 'react';

/**
 * 
 * @returns File Upload page
 */
const Upload = () => {
    const [getRef, setRef] = useDynamicRefs();

    const refs = useRef([]);

    //set title in parent 'base'
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('Upload');
    });


    // list of UploadSingleFile objects
    const [uploadSingleFiles, setUploadSingleFiles] = useState([<UploadSingleFile ref={(el) => (refs.current[0] = el)} key={0}/>]);

    // add UploadSingleFile object to rowList
    const addRow = e => {
        setUploadSingleFiles(uploadSingleFiles.concat(<UploadSingleFile ref={(el) => (refs.current[uploadSingleFiles.length] = el)} key={uploadSingleFiles.length} />));
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
                <Button variant='contained' sx={{bgcolor:'button.main', color: 'button.text'}} className='uploadButton' onClick={() => {
                    uploadSingleFiles.forEach((_uploadSingleFile, index) => {
                        refs.current[index].uploadFile();
                    })
                }}
                 style={{fontSize: '2vw', textTransform: 'none'}}>
                    Upload your document(s)
                </Button>
            </div>
        </>
    );
}

export default Upload;