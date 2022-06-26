// materials
import { } from "@mui/material";

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';



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
      <div className='vertCenter' style={{textAlign: 'center'}}>
          To change the feedback model, go to github.com/XXXX and
          commit your changes there.
      </div>
    </>
  );
}

export default FeedbackModels;