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
      FeedbackModels
    </>
  );
}

export default FeedbackModels;