import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';



/**
 * 
 * @returns FileDownload Page
 */
function FileDownload() {
    //set title in parent 'base' 
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('File Download');
    });
    return (
        <>
            FileDownload
        </>
    );
}

export default FileDownload;