import React, {useState, useRef} from 'react';
import axios from 'axios';

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
        const url = 'http://localhost:5000/fileUpload';
        const formData = new FormData();
        // formData.append('files', files[0])
        files.forEach(file => formData.append('files',file));
        // formData.append('files', files);
        console.log(formData);
        // formData.append('fileName', files.name);
        const headers = {
            Accept: 'application/json',
            'Content-Type': 'multipart/form-data',
        }
        axios.post(url, formData, headers).then((response) => {
            if (response.data === 'success') {
                // Reset the upload selectors to not have a file displayed:
                setFiles(['']);
                reset();
            } 
        });
      
        
    };

    const [receivedFileType, setReceivedFileType] = useState('');
    const [hasError, setError] = useState(-1);

    // To be able to reset the things at the end:
    const ref = useRef();

    const reset = () => {
        ref.current.value = "";
    };

    const [files, setFiles] = useState(['']);

    return (
        <div className='FileUploadButtons'>
            <h1>File Upload!</h1>
            <form>
                {console.log(files)}
                {files.map((_file, index) => {
                    return (<div key={index}>
                        <input type = "file" onChange={event => onFileChange(index, event)} ref = {ref} 
                        accept="application/pdf, application/msword, 
                        application/vnd.openxmlformats-officedocument.wordprocessingml.document, text/plain"/>
                        <button type = "button" onClick={() => removeFileSelector(index)}>Remove</button>
                        {index === hasError && <p style={{ color: 'red' }}>{`${receivedFileType} is not a supported filetype, please use a supported file.`}</p>}
                    </div>
                    
                    )
                })}
                <button type= "submit" onClick={submitFiles}>Upload </button>
                <button type= "button" onClick={addFileSelector}>add another file </button>
            </form>
        </div>
    );
}


export default Upload;