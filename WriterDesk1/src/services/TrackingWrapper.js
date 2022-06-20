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


    const defaultFields = {location: 'top-right'};
    const defaultOptions = {asynchronous: true};
    const customTrigger = (event, fields, options) => {
        // When an event is triggered, it can be handled here
        console.log('TRIGGERED')
        console.log('ev',event)
        console.log('f',fields)
        console.log('op',options)
        sendClick({
            url:window.location.href,
            
        })
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
                {children}
            </TrackingProvider>
        </>
    );
}


export default TrackingWrapper;