import {
    Button
} from "@mui/material";
import TestingComponent from "./../components/TestingComponent";



// routing
import { useContext, useState } from 'react';

//page used for testing, to be removed later

/**
 * page used for testing, to be removed later
 * 
 * @returns Testing Page
 */
const TestingPage = () => {
    // id provider
    const [id, setId] = useState(1);

    const getHenk = () => {
        console.log(id);
    }

    // list of UploadSingleFile instances
    const [instanceList, setInstanceList] = useState([<TestingComponent key={0} thisIndex={0}/>]);
    
    // add UploadSingleFile object to rowList
    const addRow = (e) => {
        setInstanceList((instanceList) => instanceList.concat([
            <TestingComponent key={id} thisIndex={id} setInstanceList={setInstanceList}/>
        ]));
        // update so we have a new, fresh id
        setId((i) => i + 1);
    };

    return (
        <>
            <br />
            <div className='center'>

                {instanceList}
                
                <Button variant='contained' sx={{bgcolor:'button.main', color: 'button.text'}} onClick={addRow}>Add</Button>
            </div>
            <Button variant='contained' sx={{bgcolor: 'red', color: 'button.text'}} onClick={getHenk}>getId</Button>
        </>
    );
}




export default TestingPage;