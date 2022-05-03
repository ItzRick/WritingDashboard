import React, {useState} from 'react';
import axios from 'axios';


import '../App.css';


const Upload = () => {
    const onFileChange = event => {
        setFile(event.target.files[0]);
        console.log(event.target.files[0]);
    };

    const onButtonClick = event => {
        console.log("this button has been clicked");
        event.preventDefault();
        const url = 'http://localhost:5000/fileUpload';
        const formData = new FormData();
        formData.append('file', file);
        formData.append('fileName', file.name);
        console.log(formData);
        console.log(file);
        const headers = {
            Accept: 'application/json',
            'Content-Type': 'multipart/form-data',
        }
        axios.post(url, formData, headers).then((response) => {
            console.log(response.data);
        });
      
        
    };

    const [file, setFile] = useState(null);



    return (
        <div className='FileUpload'>
            <form>
                <h1>File Upload!</h1>
                <input type = "file" onChange={onFileChange}/>
                <button type= "submit" onClick={onButtonClick}>Upload </button>
            </form>
        </div>
    );
}

export default Upload;