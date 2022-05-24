
import { useEffect, useState, useRef, forwardRef, useImperativeHandle  } from 'react';
import axios from 'axios';

// materials
import {
    Alert,
    Button,
    TextField
} from "@mui/material";
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';


/**
 * 
 * @param {} 
 * @returns Single File Upload Object
 */
const UploadSingleFile = forwardRef(({ setUploadSingleFiles, thisIndex }, ref) => {

    /**
     * Update uploadSingleFiles in parent Upload.js
     */
    const removeInstance = () => {
        setUploadSingleFiles((list) => list.filter(item => item.props.thisIndex !== thisIndex));
    }

    /**
     * 
     */
    useImperativeHandle(ref, () => ({
        uploadFile() {
            // url of the file api
            const url = 'https://localhost:5000/fileapi/upload';
            const formData = new FormData();
            formData.append('files',file);
            formData.append('fileName', file.name);
            formData.append('userId', 123);
            formData.append('date', date.toISOString().substring(0, 10));
            formData.append('courseCode', course);
            const headers = {
                Accept: 'application/json',
                'Content-Type': 'multipart/form-data',
            }
            axios.post(url, formData, headers).catch((error) => {
                console.log(error.response.data);
            });
                
          setFile('or drag it here.');
          setDate(new Date());
          setCourse('');
          setDisplayAlertSize(false);
          setDisplayAlertType(false);
        },
    }))

    const [file, setFile] = useState('or drag it here.');

    const [course, setCourse] = useState('');

    const [displayAlertType, setDisplayAlertType] = useState(false);

    const [displayAlertSize, setDisplayAlertSize] = useState(false);

    const [date, setDate] = useState(new Date());
    

    /**
     * Checks if the file is of the correct type, and correct size
     * @param {file} file Some file
     */
    const checkCorrectFile = (file) => {
        const fileType = file.type
        const isPDF = fileType === 'application/pdf';
        const isWord1 = fileType === ('application/vnd.openxmlformats-officedocument.wordprocessingml.document');
        const isWord2 = fileType === 'application/msword';
        const isTXT = fileType === 'text/plain';
        let isCorrectType = true;
        let isCorrectSize = true;
        if (!(isPDF || isWord1 || isWord2 || isTXT)) {
            setDisplayAlertType(true);
            isCorrectType = false;
        } else {
            setDisplayAlertType(false);
            isCorrectType = true;
        }
        if (file.size > 10485760) {
            setDisplayAlertSize(true);
            isCorrectSize = false;
        } else {
            setDisplayAlertSize(false);
            isCorrectSize = true;
        }
        if (isCorrectSize && isCorrectType) {
            setFile(file);
        } else {
            setFile('or drag it here.');
        }
    }


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
        event.stopPropagation();
        event.preventDefault();
        let dt = event.dataTransfer;
        let files = dt.files;
        checkCorrectFile(files[0])
    }

    const fileInput = useRef();
    return (
        <div style={{ marginBottom: '1vw' }}>
            <div className='vertCenter'>
                <div className='upload'
                    onDragEnter={(event) => event.preventDefault()}
                    onDragOver={(event) => event.preventDefault()}
                    onDrop={onFileDrop}>
                    <Button variant='contained' sx={{ mr: '8px', bgcolor: 'button.main', color: 'button.text' }} onClick={() => fileInput.current.click()}>Choose a file</Button>
                    <input
                        ref={fileInput}
                        type="file"
                        style={{ display: 'none' }}
                        accept="application/pdf, application/msword, 
                        application/vnd.openxmlformats-officedocument.wordprocessingml.document, text/plain"
                        onChange={onFileChange} 
                    />
                    {file.name !== undefined ? file.name : 'or drag it here.'}
                </div>
                <LocalizationProvider dateAdapter={AdapterDayjs}>
                    <DatePicker
                    disableFuture
                    label="Date"
                    openTo="day"
                    views={['year', 'month', 'day']}
                    value={date}
                    onChange={(newDate) => {
                        setDate(newDate);
                    }}
                    renderInput={(params) => <TextField {...params} />}
                    />
                </LocalizationProvider>
                <TextField label='course' variant='outlined' value={course} onChange={event => setCourse(event.target.value)}/>
                <Button variant='contained' sx={{bgcolor: 'red', color: 'button.text'}} value={thisIndex} onClick={removeInstance}>Remove</Button>
            </div>
            {displayAlertType? <Alert severity="error">Upload a file with a .txt, .pdf, .docx or .doc filetype!</Alert> : null}
            {displayAlertSize? <Alert severity="error">The uploaded file was too big, upload a file that is not larger than 10 MB!</Alert> : null}
        </div>
    )
});

export default UploadSingleFile;