// trackers
import {TrackingProvider} from '@vrbo/react-event-tracking';



/**
 * page used for testing, to be removed later
 * 
 * @returns Testing Page
 */
const TrackingWrapper = ({children}) => {
    
    const defaultFields = {location: 'top-right'};
    const defaultOptions = {asynchronous: true};
    const customTrigger = (event, fields, options) => {
        // When an event is triggered, it can be handled here
        console.log('TRIGGERED')
        console.log('ev',event)
        console.log('f',fields)
        console.log('op',options)
        
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