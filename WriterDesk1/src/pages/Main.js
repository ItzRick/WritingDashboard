import './../css/App.css';

// materials 
import { 
  Button, 
  Typography 
} from "@mui/material";
import chartImg from '../images/chartImage.png';

// routing
import { Link, useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';
import ProgressVisualization from "../components/ProgressVisualization";


/**
 * 
 * @returns homepage
 */
const Main = () => {
  
  //set title in parent 'base' 
  const {setTitle} = useOutletContext();
  useEffect(() => {
    setTitle('Homepage');
  });
  
  return (
    <div className='home_grid'>
      <div className='home1'>
        <Typography variant='h3'>Homepage</Typography>
      </div>
      <div className='home2'>
        <div className='vertCenter'>
          <Button variant='contained' className='uploadButton' sx={{
            fontSize: '2vw', textTransform: 'none', bgcolor: 'button.main', color: 'button.text'
          }} component={Link} to='/Upload'>Upload a document</Button>
        </div>
      </div>
      <div className='home3'>
        <div className='vertCenter'>
          <Typography className='recent'><u style={{ color: 'blue' }}>Recent files</u>
            <br />TheFirstFile.docx
            <br />TheSecondFile.txt
            <br />TheThirdFile.pdf</Typography>
        </div>
      </div>
      <div className='home4'>
        <div className='subTitle'>
            <br />
            <Typography style={{ fontSize: '2vw' }}><u>Progress</u></Typography>
        </div>
        <div className='plotContainer'>
          <ProgressVisualization />
        </div>
      </div>
    </div>
  );
}

export default Main;