// materials
import { } from "@mui/material";

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';
import axios from 'axios';


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

  const getDocuments = () => {
      const url = 'https://127.0.0.1:5000/fileapi/fileretrieve';
      const params = { 
          userId: 123,
          sortingAttribute: '',
      }
      axios.get(url, { params }).then((response) => {
        console.log(response.data);
        response.data.forEach(element => {console.log(element)})
      });
  };
  
  return (
    <>
      Documents
      {getDocuments()}
    </>
  );
}

export default Documents;