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
    

    /**
     * 
     * @param {String} url url of the page where the click happened
     * @param {String} eventType type of event, can be one of [click.button, click.link, view.document]
     * @param {String} buttonId id of the button, usually similair to the text displayed on the button, not available for view.document events
     * @param {int} documentId id of the document being viewed, only availabel for view.document events
     * @param {String} documentName name of the document being viewed, only availabel for view.document events
     */
    const sendClick = ({
        url,
        eventType,
        buttonId,
        documentId,
        documentName,
    }) => {
        //url for request
        const requestUrl = 'https://api.writingdashboard.xyz/clickapi/addClick';

        // create form with all the file information
        const formData = new FormData();
        formData.append('url', url);
        formData.append('eventType', eventType);
        // add only data that is not null
        if (buttonId != null) {
            formData.append('actionId', buttonId)
        } else {
            formData.append('actionId', 'name: '+ documentName + ', id: '+ documentId.toString());
        }
        
        //post the file
        axios.post(requestUrl, formData, {
            headers: authHeader(), // Autheader needed for request
        }).catch((error) => {
            console.log(error.response.data);
        });
    }

    const customTrigger = (event) => {
        // When an event is triggered, it can be handled here
        sendClick({
            url: window.location.href,
            eventType: event.eventType,
            buttonId: event.buttonId,
            documentId: event.documentId,
            documentName: event.documentName,
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