import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';



/**
 * 
 * @returns Documents Page
 */
function Documents() {
  //set title in parent 'base' 
  const { setTitle } = useOutletContext();
  useEffect(() => {
    setTitle('Documents');
  });
  return (
    <>
      Documents
    </>
  );
}

export default Documents;