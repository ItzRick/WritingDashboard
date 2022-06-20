// trackers
import {TrackingProvider} from '@vrbo/react-event-tracking';

// data sending
import axios from 'axios';
import {authHeader} from "./../helpers/auth-header";

/**
 * ContextProvider needed for tracking
 * 
 * @returns TrackingWrapper
 */
const TrackingWrapper = ({children}) => {
    
    const sendClick = ({
        url,
        
    }) => {
        console.log(url)
        //url for request
        const requestUrl = 'https://localhost:5000/clickapi/setClick';

        // create form with all the file information
        const formData = new FormData();
        formData.append('url', url);

        //post the file
        axios.post(requestUrl, formData, {
            headers: authHeader(), // Autheader needed for request
        }).catch((error) => {
            console.log(error.response.data);
        });
    }

    const customTrigger = (event) => {
        // When an event is triggered, it can be handled here
        console.log('ev',event)
        sendClick({
            url: window.location.href,
            eventType: event.eventType,
            buttonId: event.buttonId,
            linkPath: event.linkPath,
        })
    }

    return (
        <>
            <TrackingProvider
                trigger={customTrigger}
            >
                {children}
            </TrackingProvider>
        </>
    );
}


export default TrackingWrapper;