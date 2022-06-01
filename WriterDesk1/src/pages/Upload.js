// materials
import { 
    Typography,
    Button
} from "@mui/material";
import UploadSingleFile from "./../components/UploadSingleFile";

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
    const [uploadSingleFiles, setUploadSingleFiles] = useState([
        <UploadSingleFile 
            thisIndex={0}
            key={0}
            ref={(el) => (refs.current[0] = el)}
        />
    ]);

    // add UploadSingleFile object to rowList
    const addRow = e => {
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

    return (
        <>
            <br />
            <div className='center'>
                {uploadSingleFiles}
                <Button variant='contained' sx={{bgcolor:'button.main', color: 'button.text'}} onClick={addRow}>Add</Button>
            </div>
            <br />
            <div className='title'>
                <Button variant='contained' sx={{bgcolor:'button.main', color: 'button.text'}} className='uploadButton' onClick={() => {
                    uploadSingleFiles.forEach(item => {
                        refs.current[item.props.thisIndex].uploadFile();
                    })
                    //remove all files except index = 0
                    setUploadSingleFiles((list) => list.filter(item => item.props.thisIndex == 0));
                    setId(1);
                }}
                 style={{fontSize: '2vw', textTransform: 'none'}}>
                    Upload your document(s)
                </Button>
            </div>
        </>
    );
}

export default Upload;