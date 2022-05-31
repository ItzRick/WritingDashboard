// materials
import {
    Typography,
    Box,
} from "@mui/material";

import UploadSingleFile from "./../components/UploadSingleFile";
import UploadPopUp from "./../components/UploadPopUp";
import BlueButton from "./../components/BlueButton";

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect, useState, useRef } from 'react';

/**
 * 
 * @returns File Upload page
 */
const Upload = () => {
    // list of references
    const refs = useRef([]);

    //set title in parent 'base'
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('Upload');
    });

    // id provider
    const [id, setId] = useState(1);

    // list of UploadSingleFile objects
    const [uploadSingleFiles, setUploadSingleFiles] = useState([]);

    // add UploadSingleFile object to uploadSingleFiles
    const addRow = () => {
        setUploadSingleFiles(uploadSingleFiles.concat([
            <UploadSingleFile
                thisIndex={id}
                key={id}
                setUploadSingleFiles={setUploadSingleFiles}
                ref={(el) => (refs.current[id] = el)}
            />
        ]));
        // update id so we have a fresh id ready for the next instance
        setId((i) => i + 1);
    };

    // Add first row, but only upon first render (i.e. when rendering the page)
    //   Side effect: when you update the code, the page renders again, but does not remove the first row
    useEffect(() => {
        addRow();
    }, []);

    // upload all documents present in the UploadSingleFile objects in uploadSingleFiles
    const uploadDocuments = () => {
        uploadSingleFiles.forEach(item => {
            refs.current[item.props.thisIndex].uploadFile();
        })
        //remove all files except index = 0
        setUploadSingleFiles([<UploadSingleFile
            thisIndex={0}
            key={0}
            setUploadSingleFiles={setUploadSingleFiles}
            ref={(el) => (refs.current[0] = el)}
        />]);
        setId(1);
    }

    return (
        <>
            <Box className='title'>
                <Typography variant='h3'>Upload</Typography>
            </Box>
            <br />
            <Box className='center'>
                {uploadSingleFiles}
            </Box>
            <Box className='center' >
                <BlueButton onClick={addRow}>Add</BlueButton>
            </Box>
            <br />
            <Box className='title'>
                <UploadPopUp func={uploadDocuments} fileCount={1} />
            </Box>
            
        </>
    );
}

export default Upload;