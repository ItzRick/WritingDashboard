import React, { useState, useEffect } from 'react';
import axios from 'axios';
// import '../App.css';

const ListFiles = () => {
    // Initialize file list
    const [files, setFiles] = useState([
        { id: 1, fileName: 'Frank', course: '2IPE0', date: '20-02-2002' },
        { id: 2, fileName: 'Bertus', course: '2IPE0', date: '08-12-2180' },
    ]);

    const sortingAttributes = ["filename.asc", "filename.desc", "course.asc", "course.desc", "date.asc", "date.desc"]
    const [sortingAttribute, setSorting] = useState(sortingAttributes[0]);

    const changeSortingAttribute = (event) => {
        setSorting(event.target.value);
    };

    // Call getFiles() on refresh page 
    useEffect(() => {getFiles()});

    // Perform GET request to retrieve files of current user from backend
    // Puts response in variable 'files'
    const getFiles = () => {
        const url = 'https://localhost:5000/fileapi/fileretrieve';
        const data = {
            params: {sortingAttribute: sortingAttribute}
        }
        const headers = {
            Accept: 'application/json',
            'Content-Type': 'application/json',
        }

        //Perform GET request
        axios.get(url, data, headers).then((response) => {
            setFiles(response.data);
        }).catch(err => {
            console.log(err.response.data);
        });
    }

    return (
    <div className='ListFiles'>
        <h1>List Files</h1>
        <button type="button" onClick={getFiles}>Get Files</button>
        <div>
            <label>
                Sort by: 
                <select value={sortingAttribute} onChange={changeSortingAttribute}>
                    {sortingAttributes && sortingAttributes.map(sortingAttribute =>
                        <option key={sortingAttribute} value={sortingAttribute}>{sortingAttribute}</option>
                    )}
                </select>
            </label>
        </div>
        <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Course</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {files && files.map(file =>
                        <tr key={file.id}>
                            <td><a href='https://localhost:3000/'>{file.fileName}</a></td>
                            <td>{file.course}</td>
                            <td>{file.date}</td>
                        </tr>
                    )}
                </tbody>
            </table>
    </div> );
}

export default ListFiles;