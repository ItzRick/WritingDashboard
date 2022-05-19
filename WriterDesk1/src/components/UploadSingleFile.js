
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DatePicker } from '@mui/x-date-pickers';
import LocalizationProvider from '@mui/lab/LocalizationProvider';
import { useEffect, useState, useRef, forwardRef, useImperativeHandle } from 'react';
// materials
import {
    Button,
    TextField
} from "@mui/material";



/**
 * 
 * @returns Single File Upload Object
 */
const UploadSingleFile = forwardRef(({ props, setUploadSingleFiles, thisIndex }, ref) => {

    /**
     * Update uploadSingleFiles in parent Upload.js
     */
    const removeInstance = () => {
        setUploadSingleFiles((list) => list.filter(item => item.props.thisIndex !== thisIndex));
    }

    useImperativeHandle(ref, () => ({
        uploadFile() {
            console.log("Hello from Child Component")
            console.log(file.name);
            console.log(date);
            console.log(course);
            setFile('or drag it here.');
            setDate('');
            setCourse('');
        },
    }))

    const [file, setFile] = useState('or drag it here.');

    const [date, setDate] = useState('');

    const [course, setCourse] = useState('');


    const onFileChange = (event) => {
        if (event.target.files[0] === undefined) {
            setFile('or drag it here.')
        } else {
            setFile(event.target.files[0]);
        }
    }

    const onFileDrop = (event) => {
        event.stopPropagation();
        event.preventDefault();
        let dt = event.dataTransfer;
        let files = dt.files;
        console.log(files[0]);
        setFile(files[0]);
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
                        onChange={onFileChange}
                    />
                    {file.name !== undefined ? file.name : 'or drag it here.'}
                </div>

                <TextField label='dd/mm/yy' variant='outlined' value={date} style={{ marginRight: '1vw' }} onChange={event => setDate(event.target.value)} />
                <TextField label='course' variant='outlined' value={course} onChange={event => setCourse(event.target.value)} />
                <Button variant='contained' sx={{ bgcolor: 'red', color: 'button.text' }} value={thisIndex} onClick={removeInstance}>Remove</Button>
            </div>
        </div>
    )
});

export default UploadSingleFile;