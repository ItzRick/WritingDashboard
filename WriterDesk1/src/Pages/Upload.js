// materials
import {
    Box,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    Typography,
} from "@mui/material";

import UploadSingleFile from "./../components/UploadSingleFile";
import BlueButton from "./../components/BlueButton";

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect, useState, useRef, Fragment } from 'react';

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
    
    // list of references
    const refs = useRef([]);

    // whether the dialog is open or not
    const [open, setOpen] = useState(false);
    // number of successes and failures during uploading of files
    const [succ, setSucc] = useState(0);
    const [fail, setFail] = useState(0);
    // filenames of the failed uploads
    const [failedFiles, setFailedFiles] = useState([]);

    /**
     * close the popup and reset to successes and failures to 0
     */
    const popUpClose = () => {
        setOpen(false)
        setSucc(0)
        setFail(0)
        setFailedFiles([])
    }

    /**
     * open popup and upload all documents
     */
    const handleClickOpen = () => {
        uploadDocuments();
        setOpen(true);
    };

    // id provider
    const [id, setId] = useState(1);

    // list of UploadSingleFile objects
    const [uploadSingleFiles, setUploadSingleFiles] = useState([]);

    /**
     * add UploadSingleFile object to uploadSingleFiles
     */
    const addRow = () => {
        setUploadSingleFiles(uploadSingleFiles.concat([
            <UploadSingleFile
                thisIndex={id}
                key={id}
                setFailedFiles={setFailedFiles}
                setSucc={setSucc}
                setFail={setFail}
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

    /**
     * upload all documents present in the UploadSingleFile objects in uploadSingleFiles
     */
    const uploadDocuments = () => {
        uploadSingleFiles.forEach(item => {
            refs.current[item.props.thisIndex].uploadFile();
        })
        //remove all files except index = 0
        setUploadSingleFiles([<UploadSingleFile
            thisIndex={0}
            key={0}
            setFailedFiles={setFailedFiles}
            setSucc={setSucc}
            setFail={setFail}
            setUploadSingleFiles={setUploadSingleFiles}
            ref={(el) => (refs.current[0] = el)}
        />]);
        setId(1);
    }

    return (
        <>
            <br />
            <Box className='center'>
                {uploadSingleFiles}
            </Box>
            <Box className='center' >
                <BlueButton idStr='AddUploadRow' onClick={addRow}>Add</BlueButton>
            </Box>
            <br />
            <Box className='title'>
            <BlueButton idStr='uploadYourDocument(s)' addStyle={{ fontSize: '2vw', textTransform: 'none' }} onClick={handleClickOpen}>Upload your document(s)</BlueButton>
            {/* Dialog after upload, displays number of documents uploaded and failed and has 2 buttons */}
            <Dialog
                open={open}
                onClose={popUpClose}
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
            >
                <DialogTitle id="alert-dialog-title">
                    {"Upload your documents?"}
                </DialogTitle>
                <DialogContent>
                    <DialogContentText id="alert-dialog-description">
                        {succ <= 0 && <>No documents were successfully uploaded. </>}
                        {succ == 1 && <>1 document was successfully uploaded. </>}
                        {succ > 1 && <>{succ} documents were successfully uploaded. </>}
                        <br/>
                        {fail <= 0 && <>No documents failed to upload</>}
                        {fail == 1 && <>1 document failed to upload</>}
                        {fail > 1 && <>{fail} documents failed to upload</>}
                        , because:<br/>
                        {failedFiles.map((item) =><Typography component={'span'} key={item.id}>{item.content}<br/></Typography>)}
                        What would you like to do next?
                    </DialogContentText>
                </DialogContent>
                <DialogActions sx={{justifyContent:'space-between'}}>
                    <BlueButton idStr='uploadMoreDocuments' onClick={popUpClose}> Upload more documents </BlueButton>
                    <BlueButton idStr='viewDocuments' pathName='/Documents'> View documents </BlueButton>
                </DialogActions>
            </Dialog>
            </Box>            
        </>
    );
}

export default Upload;