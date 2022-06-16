import {
} from "@mui/material";
import BlueButton from "./../components/BlueButton";
import TestingComponent from "./../components/TestingComponent";


/**
 * page used for testing, to be removed later
 * 
 * @returns Testing Page
 */
const TestingPage = () => {

    return (
        <>
            <BlueButton onClick={() => {console.log("I'm Blue")}}> blueee </BlueButton>
        </>
    );
}


export default TestingPage;