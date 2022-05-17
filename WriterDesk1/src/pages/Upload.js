import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';



/**
 * 
 * @returns Upload Page
 */
const Upload = () => {
    //set title in parent 'base' 
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('Upload');
    });
    return (
        <>
            Upload
        </>
    );
}

export default Upload;