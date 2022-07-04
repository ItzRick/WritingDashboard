// materials
import {Link} from "@mui/material";
import axios from 'axios';

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect, useState } from 'react';



/**
 * 
 * @returns FeedbackModels Page
 */
function FeedbackModels() {
  //set title in parent 'base' 
  const { setTitle } = useOutletContext();

  const [feedbackModelVersion, setFeedbackModelVersion] = useState('');

  useEffect(() => {
    const url = 'https://api.writingdashboard.xyz/feedback/getCurrentVersion';
    axios.get(url)
      .then((response) => {
        setFeedbackModelVersion(response.data)
      })
  }, []);

  useEffect(() => {
      setTitle('Feedback Models');
  });
  return (
    <>
      <div className='vertCenter' style={{textAlign: 'center', display:'inline-block'}}>
          To change the feedback model, go to <Link id='link' href='https://github.com/ItzRick/WritingDashboard'>https://github.com/ItzRick/WritingDashboard</Link>,
          create a new branch and change the code there. To change the feedback model, go to the WriterDesk1/backend/app/feedback/generateFeedback folder
          and change any of the feedbackmodels. These models are located inside the CohesionFeedback, IntegrationContentFeedback, LanguageStyleFeedback
          and StructureFeedback folders. It may also be necessary to make changes to the BaseFeedback class. Do not forget to change the feedbackversion 
          to a higher number in the FEEDBACKVERSION variable in WriterDesk1/backend/config.py file. When you are done create test cases inside the 
          WriterDesk1/backend/tests/feedbackModels folder. Then create a pull request and apply all feeedback of the reviewer.
          <br/>
          <br/>
          The current feedback model version is: {feedbackModelVersion}.
      </div>
    </>
  );
}

export default FeedbackModels;