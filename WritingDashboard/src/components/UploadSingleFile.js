
import { useState, useRef, forwardRef, useImperativeHandle } from 'react';
import axios from 'axios';

// materials
import {
    Alert,
    Button,
    TextField
} from "@mui/material";
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import BlueButton from "./BlueButton"; 

import { AuthenticationService } from "../services/authenticationService";

// tracking
import { useContext } from 'react';
import { TrackingContext } from '@vrbo/react-event-tracking';
import { authHeader } from '../helpers/auth-header';

/**
 * 
 * @param {*} ref reference to the parent Upload.js
 * @param {int} thisIndex Index of the UploadSingleFile objects in the list in parent
 * @param {function} setUploadSingleFiles function in parent to change the list of UploadSingleFile objects
 * @returns Single File Upload Object
 */
const UploadSingleFile = forwardRef(({ setFailedFiles, setSucc, setFail, setUploadSingleFiles, thisIndex }, ref) => {

    // context as given by the Tracking Provider
    const tc = useContext(TrackingContext);

    /**
     * Update uploadSingleFiles in parent Upload.js by removing self
     */
    const removeInstance = () => {
        setUploadSingleFiles((list) => list.filter(item => item.props.thisIndex !== thisIndex));
        // use Tracking when remove file row has been clicked
        if (tc.hasProvider) {
            tc.trigger({
                eventType: 'click.button', //send eventType
                buttonId: 'removeFileRow', //send buttonId
            })
        }
    }

    /**
     * File upload function
     * @param {*} ref reference to parent
     */
    useImperativeHandle(ref, () => ({
        uploadFile() {
            if (file !== 'or drag it here.') {            
                // url of the file api's upload function
                const url = '/api/fileapi/upload';
                // id of current user
                const userId = AuthenticationService.getCurrentUserId();

                // create form with all the file information
                const formData = new FormData();
                formData.append('files', file);
                formData.append('fileName', file.name);
                formData.append('userId', userId);
                formData.append('date', date.toISOString().substring(0, 10));
                formData.append('courseCode', course);
                //add header
                const authheader = authHeader();
                const fileheader = {
                    Accept: 'application/json',
                    'Content-Type': 'multipart/form-data',
                }
                const headers = {headers: Object.assign(fileheader, authheader)};
                //post the file
            axios.post(url, formData, headers)
            .then((response) => {
                setSucc((v) => (v+1))
                // Make the backend call to generate feedback:
                // Get the ids of the uploaded files from the backend:
                let message = response.data
                let ids = /\[(.*?)\]/.exec(message)[0];
                ids = ids.replace(/[[\]']+/g,'')
                ids = ids.split(', ')
                // Make a post request with the correct parameters:
                let params = new URLSearchParams();
                ids.forEach(element => params.append("fileId", element));
                let generateUrl = '/api/feedback/generate';
                const config = {
                    params: params,
                    headers: {
                      'Content-Type': 'application/x-www-form-urlencoded'
                    }
                  }
                axios.post(generateUrl, {}, config)
                .catch((error) => {
                    console.log(error.response.data);
                });
              })
            .catch((error) => {
                // If the backend call has a failure, pass this to the popup:
                setFail((v) => (v+1))
                setFailedFiles((l) => l.concat([{'content':error.response.data,'id':thisIndex}]))
                console.log(error.response.data);
            });
            } else {
                // there is no file selected
                setFail((v) => (v+1))
                setFailedFiles((l) => l.concat([{'content':'Missing File','id':thisIndex}]))
            }
            //post-update
            //empty file, date and course
            setFile('or drag it here.');
            setDate(new Date());
            setCourse('');
            //remove warnings
            setDisplayAlertSize(false);
            setDisplayAlertType(false);
        },
    }))

    // state of the file drag and drop box. Either 'or drag it here.' or 'FILENAME.TYPE'
    const [file, setFile] = useState('or drag it here.');
    // state of the course box. String
    const [course, setCourse] = useState('');
    // state of the course box. String
    const [date, setDate] = useState(new Date());

    // Alerts
    const [displayAlertType, setDisplayAlertType] = useState(false);
    const [displayAlertSize, setDisplayAlertSize] = useState(false);

    /**
     * Checks if the file is of the correct type, and correct size
     * @param {file} file Some file
     */
    const checkCorrectFile = (file) => {
        const fileType = file.type
        //file type checkers
        const isPDF = fileType === 'application/pdf';
        const isWord = fileType === ('application/vnd.openxmlformats-officedocument.wordprocessingml.document');
        const isTXT = fileType === 'text/plain';
        //boolean for correct type and size
        let isCorrectType = true;
        let isCorrectSize = true;

        //check file type: pdf, doc, docx, txt
        if (!(isPDF || isWord || isTXT)) {
            // incorrect file type
            setDisplayAlertType(true);
            isCorrectType = false;
        } else {
            // correct file type
            setDisplayAlertType(false);
            isCorrectType = true;
        }

        //check file size: <10MB
        if (file.size > 10485760) {
            // incorrect file size
            setDisplayAlertSize(true);
            isCorrectSize = false;
        } else {
            // correct file size
            setDisplayAlertSize(false);
            isCorrectSize = true;
        }

        //change the displayed file
        if (isCorrectSize && isCorrectType) {
            // all is correct, accept file
            setFile(file);
        } else {
            // some incorrect, reject file
            setFile('or drag it here.');
        }
    }


    /**
     * Handle file being added to the file-box
     * @param {FileChangeEvent} event The file in the filebox changed
     */
    const onFileChange = (event) => {
        if (event.target.files[0] === undefined) {
            // no file here
            setFile('or drag it here.')
        } else {
            // there is a file here, check if it is correct
            checkCorrectFile(event.target.files[0])
        }
    }

    /**
     * Handle a file being dragged and dropped into file field
     * @param {event} event 
     */
    const onFileDrop = (event) => {
        // make sure the file is not displayed as pdf in the browser
        event.stopPropagation();
        event.preventDefault();
        //check file correctness
        let dt = event.dataTransfer;
        let files = dt.files;
        checkCorrectFile(files[0])
    }

    // reference so the parent can ask for the file
    const fileInput = useRef();
    return (
        <div style={{ marginBottom: '1vw' }}>
            <div className='vertCenter'>
                <div className='upload'
                    onDragEnter={(event) => event.preventDefault()}
                    onDragOver={(event) => event.preventDefault()}
                    onDrop={onFileDrop}>
                    <BlueButton idStr='ChooseAFile' onClick={() => fileInput.current.click()} addStyle={{ mr: '8px', width: '8vw',
                        minWidth: '50px', whiteSpace: 'nowrap', overflow: 'hidden', fontSize: '0.8vw'}}>
                        Choose a file
                    </BlueButton>
                    <input
                        ref={fileInput}
                        type="file"
                        style={{ display: 'none' }}
                        accept="application/pdf,
                        application/vnd.openxmlformats-officedocument.wordprocessingml.document, text/plain"
                        onChange={onFileChange}
                    />
                    {file.name !== undefined ? file.name : 'or drag it here.'}
                </div>
                <LocalizationProvider dateAdapter={AdapterDayjs} width={'5px'}>
                    <DatePicker
                        disableFuture
                        label="Date"
                        openTo="day"
                        views={['year', 'month', 'day']}
                        value={date}
                        onChange={(newDate) => {
                            var tempdate = new Date(newDate);
                            // Transform date from GMT to UTC
                            var date = new Date(tempdate.getTime() - (tempdate.getTimezoneOffset() * 60 * 1000));
                            setDate(date);
                        }}
                        renderInput={(params) => <TextField {...params} sx={{minWidth: '80px'}}/>}
                    />
                </LocalizationProvider>
                <TextField id='courseId' label='Course ID' inputProps={{ maxLength: 16 }} variant='outlined' value={course} sx={{minWidth: '80px'}} onChange={event => setCourse(event.target.value)} />
                <Button id='RemoveUploadRow' variant='contained' sx={{ bgcolor: 'buttonWarning.main', color: 'buttonWarning.text', ml: '5px',}} value={thisIndex} onClick={removeInstance}>Remove</Button>
            </div>
            {displayAlertType ? <Alert severity="error">Upload a file with a .txt, .pdf or .docx filetype!</Alert> : null}
            {displayAlertSize ? <Alert severity="error">The uploaded file was too big, upload a file that is not larger than 10 MB!</Alert> : null}
        </div>
    )
});

export default UploadSingleFile;