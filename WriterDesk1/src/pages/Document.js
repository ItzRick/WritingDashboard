// materials
import {Typography} from "@mui/material";

// routing
import { useOutletContext, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';

// show pdf
import React from 'react';
import AllPagesPDFViewer from "../components/ShowPDF";
import "../css/styles.css";
import "../css/Document.css";
import placeholder from '../images/chartImage.png';


/**
 *
 * @returns Documents Page
 */
function Document() {
  const location = useLocation();


  //set title in parent 'base'
  const { setTitle } = useOutletContext();

  const [showTextbox, setShowTextbox] = useState([]);

  const [path, setPath] = useState([]);
  const [type, setType] = useState([]);

  const [scoreLanguage, setScoreLanguage] = useState([]);
  const [scoreStructure, setScoreStructure] = useState([]);
  const [scoreCohesion, setScoreCohesion] = useState([]);
  const [scoreSourceIntegration, setScoreSourceIntegration] = useState([]);



  useEffect(() => {
    setTitle('Document');
  });

  useEffect(() => {
    const fileId = location.state.fileId; // Get file id from previous page.
    fetchFilePath(fileId); // Set file path and type
    fetchScores(fileId); // Set scores of current file
    fetchMistakes(fileId); //Set mistakes of current file
  }, [location.state.fileId]);


  /**
   * Make the backend call to retrieve the correct file and
   * set the correct path and file type for the given file id.
   * @param {number} fileId: id of the file that needs to be shown.
   */
  const fetchFilePath = (fileId) => {
    // Url of the server:
    const url = 'https://127.0.0.1:5000/fileapi/getFileById';

    // Make the call to the backend:
    axios.get(url, {params: {fileId: fileId}})
      .then((response) => {
        setPath(response.data.path); // Set path of file given by file id
        setType(response.data.filetype.substring(1)); // Set file type without '.'
      })
  }

//TODO: Retrieve scores from database.
  const fetchScores = (fileId) => {
    // // Url of the server:
    //const url = 'https://127.0.0.1:5000/scoreapi/getScores';

    // // Make the call to the backend:
    // axios.get(url, {params: {fileId: fileId}})
    //   .then((response) => {
    //     setScoreLanguage(response.data.scoreLanguage);
    //     setScoreStructure(response.data.scoreStructure);
    //     setScoreCohesion(response.data.scoreCohesion);
    //     setScoreSourceIntegration(response.data.scoreSourceIntegration);
    //   })
  }

//TODO: Retrieve mistakes from database.
  const fetchMistakes = (fileId) => {
    // Url of the server:
    //const url = 'https://127.0.0.1:5000/mistakeapi/getMistakes';

    // Make the call to the backend:
    // axios.get(url, {params: {fileId: fileId}})
    //   .then((response) => {
    //
    //   })
  }

  const mistakes = [
    {text: 'decade', explanation: 'expl1', type: 0, coords: [156.9016876220703, 157.89927673339844, 183.29876708984375, 169.56455993652344], replacements: ['ab', 'b', 'ba']},
    {text: 'Furthermore', explanation: 'expl2', type: 1, coords: [464.495361328125, 468.1363525390625, 514.29833984375, 480.14129638671875], replacements: ['as']},
    {text: 'past decade, a new ', explanation: 'expl3', type: 2, coords: [126.9016876220703, 157.89927673339844, 213.29876708984375, 169.56455993652344], replacements: ['a', 'b', 'c']},
    {text: 'semantics', explanation: 'expl4', type: 3, coords: [390.88116455078125, 858.056518555, 430.1736755371094, 870.061454773], replacements: []},
  ];


  /**
   * Function to show all the explanation boxes that are being clicked.
   * @param {Object} e - Click event
   * @param {Object} coords - Array of the coordinates of the mistake being clicked
   */
  const handleHighlightClick = (e, coords) => {
    let rect = e.target.getBoundingClientRect();
    let x = coords[0] + e.clientX - rect.left; // x-coordinate of click in document
    let y = coords[1] + e.clientY - rect.top; // y-coordinate of click in document

    let newArrShowTextbox = []; // Create new array to overwrite showTextbox

    for (let i = 0; i < mistakes.length; i++) {
      // Loop over all mistakes to check if there is clicked on that mistake.
      let left = mistakes[i].coords[0] - 2; // x1 of mistake[i] coordinates
      let right = mistakes[i].coords[2] + 2; // x2 of mistake[i] coordinates
      let top = mistakes[i].coords[1]; // y1 of mistake[i] coordinates
      let bottom = mistakes[i].coords[3]; // y2 of mistake[i] coordinates

      //Set showTextbox true for every mistake that is clicked
      newArrShowTextbox[i] = (left <= x) && (x <= right) && (top <= y) && (y <= bottom);
    }
    setShowTextbox(newArrShowTextbox); // Overwrite showTextbox
  }

  /**
   * Function to show or hide all the explanations of one type. Call this function when clicking on the bar chart.
   * @param {number} type - Number for type of mistake
   */
  const showAllExplanationsOfType = (type) => {
    let allOpenOfType = true; // Boolean that indicate if all explanations of given type are shown

    for (let i = 0; i < mistakes.length; i++) {
      // Check if explanation of mistake is shown
      if (mistakes[i].type === type && !showTextbox[i]) {
        allOpenOfType = false; // Not all explanations of the given type are shown
      }
    }

    let newArrShowTextbox = []; // Create new array to overwrite showTextbox

    for (let i = 0; i < mistakes.length; i++) {
      if (mistakes[i].type === type) {
        // Show all explanations of the given type
        // If this is already the case, hide them all
        newArrShowTextbox[i] = !allOpenOfType;
      }
    }
    setShowTextbox(newArrShowTextbox); // Overwrite showTextbox
  }



  /**
   * Div that shows the explanation of a mistake being clicked
   * @property {number} number - Number of mistake
   * @property {number} type - Number for type of mistake
   * @property {String} expl - Explanation of the mistake
   * @property {Object} replacements - Array of max 3 replacements for the mistake
   * @returns TextBoxExplanation component
   */
  const TextBoxExplanation = (props) => {
    return(
      <div className={showTextbox[props.number] ? 'textBoxExpl' : 'hidden'} id={'textBoxExpl' + props.number}
           style={{backgroundColor: typeToColor(props.type), borderColor: typeToColor(props.type)}}>
        <Typography className='textBoxType' style={{color: typeToColor(props.type), fontSize: 'calc(8px + 0.5vw)'}}>
          <b>{typeToName(props.type)}</b>
        </Typography>
        <Typography variant='body1' className='textBoxWord' style={{fontSize: 'calc(12px + 0.3vw)'}}>
          <b>{props.text}</b>
        </Typography>
        <Typography variant='body2' sx={{marginTop: '5px', marginBottom:'10px', fontSize: 'calc(12px + 0.2vw)'}}>
          {props.expl}
        </Typography>
        <Typography className={props.replacements.length > 0 ? 'replacementsText' : 'hidden'}
                    style={{fontSize: 'calc(11px + 0.2vw)'}} variant='body2'>
          Possible replacements:
        </Typography>
        <Typography className={props.replacements.length > 0 ? 'textBoxReplacements' : 'hidden'}
                    variant='body1'
                    style={{borderColor: typeToColor(props.type), fontSize: 'calc(11px + 0.2vw)',
                      marginLeft: 'calc(2px + 0.2vw)', marginRight: 'calc(2px + 0.2vw)'}}>
          {props.replacements[0]}
        </Typography>
        <Typography className={props.replacements.length > 1 ? 'textBoxReplacements' : 'hidden'}
                    variant='body1'
                    style={{borderColor: typeToColor(props.type), fontSize: 'calc(11px + 0.2vw)',
                      marginLeft: 'calc(2px + 0.2vw)', marginRight: 'calc(2px + 0.2vw)'}}>
          {props.replacements[1]}
        </Typography>
        <Typography className={props.replacements.length > 2 ? 'textBoxReplacements' : 'hidden'}
                    variant='body1'
                    style={{borderColor: typeToColor(props.type), fontSize: 'calc(11px + 0.2vw)',
                      marginLeft: 'calc(2px + 0.2vw)', marginRight: 'calc(2px + 0.2vw)'}}>
          {props.replacements[2]}
        </Typography>
      </div>
    );
  };


  /**
   * Transparent div that handles onClick events on highlighted text
   * @property {Object} coords - Array of the coordinates on the page where the mistake is
   * @property {number} type - Number for type of mistake
   * @returns ClickableTextDiv component
   */
  const ClickableTextDiv = (props) => {
    return(
     <div onClick={e=>handleHighlightClick(e, props.coords)} className='clickableTextDiv'
          style={{ backgroundColor: typeToColor(props.type), left: props.coords[0] - 2, top: props.coords[1],
            width: props.coords[2] - props.coords[0] + 4,
            height: props.coords[3] - props.coords[1], borderRadius:'4px'}}>
     </div>
    );
  };


  /**
   * Function to get the correct color for a mistake type
   * @param {number} type - Number for type of mistake
   * @returns {String} Color matched to the input type
   */
  const typeToColor = (type) => {
    if (type === 0) { // Language and Style
      return '#648FFF80'
    } else if (type === 1) { // Cohesion
      return '#FE610080'
    } else if (type === 2) { // Structure
      return '#FFB00080'
    } else { // Source Integration and Content
      return '#DC267F80'
    }
  };


  /**
   * Function to get the correct name for a mistake type
   * @param {number} type - Number for type of mistake
   * @returns {String} Name matched to the input type
   */
  const typeToName = (type) => {
    if (type === 0) {
      return 'Language and Style'
    } else if (type === 1) {
      return 'Cohesion'
    } else if (type === 2) {
      return 'Structure'
    } else {
      return 'Source Integration and Content'
    }
  };


  return (
    <>
      <div className="all-page-container" id="all-page-container">
        {/** potentially convert document to pdf and show document on page */}
        <AllPagesPDFViewer pdf={`https://127.0.0.1:5000/converttopdf/convert?filepath=${path}&filetype=${type}`} />
        {mistakes.map((mistake, i) =>
          <ClickableTextDiv key={i} number={i} coords={mistake.coords} type={mistake.type}/>
        )}
      </div>
      <div className='rightFloat'>
        <img className='smallGraph' src={placeholder} />
        <br />
        {mistakes.map((mistake, i) =>
          <TextBoxExplanation
          key={i} number={i} text={mistake.text} type={mistake.type} expl={mistake.explanation}
          replacements={mistake.replacements}
          />
        )}
      </div>
    </>
  );
}

export default Document;