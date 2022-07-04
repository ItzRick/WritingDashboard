import './../css/App.css';

// materials 
import {
  Typography
} from "@mui/material";
import BlueButton from "./../components/BlueButton";

// routing
import { Link, useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';
import ProgressVisualization from "../components/ProgressVisualization";

// tracking
import { useContext } from 'react';
import { TrackingContext } from '@vrbo/react-event-tracking';

/**
 * 
 * @returns homepage
 */
const Main = () => {

  //set title in parent 'base' 
  const { setTitle } = useOutletContext();
  useEffect(() => {
    setTitle('Homepage');
  });

  // context as given by the Tracking Provider
  const tc = useContext(TrackingContext);

  return (
    <div className='home_grid'>
      <div className='home1'>
      </div>
      <div className='home2'>
        <div className='vertCenter'>
          <BlueButton idStr='UploadDocument' className='uploadButton' pathName='/Upload' addStyle={{ width: '20vw', height: '7vw', fontSize: '2vw', textTransform: 'none' }}>Upload a document</BlueButton>
        </div>
      </div>
      <div className='home3'>
        <div className='vertCenter'>
          <BlueButton idStr='ViewDocuments' className='documentsButton' pathName='/Documents' addStyle={{ width: '20vw', height: '7vw', fontSize: '2vw', textTransform: 'none' }}>View documents</BlueButton>
        </div>
      </div>
      <div className='home4'>
        <div className='subTitle'>
          <br />
          <Typography id='progressLink' className='progressLink' style={{ fontSize: 'calc(1vw + 12px)', color: '#44749D' }}
            component={Link} to='/Progress' onClick={() => {
              if (tc.hasProvider) {
                tc.trigger({
                  eventType: 'click.link',
                  buttonId: '/Progress',
                })
              }
            }}>
            <u>Progress</u>
          </Typography>
        </div>
        <div className='plotContainer'>
          <ProgressVisualization />
        </div>
      </div>
    </div>
  );
}

export default Main;