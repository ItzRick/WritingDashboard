import React, {useState, useRef} from 'react';
import axios from 'axios';
import useDynamicRefs from 'use-dynamic-refs';

import '../App.css';


const Upload = () => {
    const onFileChange = (index, event) => {
        console.log(event.target.files[0].type);
        const fileType = event.target.files[0].type
        const isPDF = fileType === 'application/pdf';
        const isWord1 = fileType === ('application/vnd.openxmlformats-officedocument.wordprocessingml.document');
        const isWord2 = fileType === 'application/msword';
        const isTXT = fileType === 'text/plain';
        let data = [...files];
        if (!(isPDF || isWord1 || isWord2 || isTXT)) {
            // console.log();
            data[index] = '';
            reset();
            console.log(files);
            setError(index);
            setReceivedFileType(fileType);
        } else {
            data[index] = event.target.files[0];
            setError(-1);
        }
        setFiles(data);
    };

    const addFileSelector = () => {
        setFiles([...files, ''])
        // console.log(files)
    }

    const removeFileSelector = (index) => {
        let currentFiles = [...files]
        currentFiles.splice(index, 1)
        setFiles(currentFiles)
        // console.log(files)
    }

    const submitFiles = event => {
        event.preventDefault();
        console.log(files[0]);
        // Connnection to the backend, URL to be changed later:
        const url = 'https://localhost:5000/fileapi/upload';
        const formData = new FormData();
        // formData.append('files', files[0])
        files.forEach(file => formData.append('files',file));
        // formData.append('files', files);
        console.log(formData);
        files.forEach(file => formData.append('fileName', file.name));
        files.forEach(file => formData.append('userId', 123));
        const headers = {
            Accept: 'application/json',
            'Content-Type': 'multipart/form-data',
        }
        axios.post(url, formData, headers).then((response) => {
            console.log(response.data)
            if (response.data === 'success') {
                let oldLength = files.length;
                // Reset the upload selectors to not have a file displayed:
                setFiles(['']);
                files.forEach((_file, index) => {
                    reset(index);
                }
                )
            } 
        });
      
        
    };

    const [receivedFileType, setReceivedFileType] = useState('');
    const [hasError, setError] = useState(-1);

    // To be able to reset the things at the end:
    const [getRef, setRef] =  useDynamicRefs();

    const reset = (index) => {
        getRef(index.toString()).current.value = "";
    };

    const [files, setFiles] = useState(['']);

    return (
        <>
            <div className='title'>
                <Typography variant='h3'>Upload</Typography>
            </div>
            <br />
            <div className='center'>
                {UploadSingleFile()}
                {rowList}
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