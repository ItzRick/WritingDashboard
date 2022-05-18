import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';



/**
 * 
 * @returns FeedbackModels Page
 */
function FeedbackModels() {
  //set title in parent 'base' 
  const { setTitle } = useOutletContext();
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