import {
    Button
} from "@mui/material";
import BlueButton from "./../components/BlueButton";
import TestingComponent from "./../components/TestingComponent";

// trackers
import {TrackingProvider, TrackingContext} from '@vrbo/react-event-tracking';
import { useContext } from "react";

const triggerFunc = () => {
    console.log('TRIGGERED')
}

// click data tracking



/**
 * page used for testing, to be removed later
 * 
 * @returns Testing Page
 */
const TestingPage = () => {
    const defaultFields = {location: 'top-right'};
    const defaultOptions = {asynchronous: true};
    const customTrigger = (event, fields, options) => {
        // Implement custom event tracking.
        console.log('ev',event)
        console.log('f',fields)
        console.log('op',options)
        triggerFunc()
    }
    
    const eventPayload = {
        'generic.click': {
            eventaction: 'toggle'
        },
        'button.click': {
            eventaction: 'button clicked'
        },
        'generic.event': {
            eventaction: 'hit test'
        }
    }

    return (
        <>
            <TrackingProvider
                fields={defaultFields}
                options={defaultOptions}
                trigger={customTrigger}
                eventPayload={eventPayload}
            >
                <BlueButton onClick={() => {console.log("I'm Blue")}}> blueee </BlueButton>
            </TrackingProvider>
        </>
    );
}


export default TestingPage;