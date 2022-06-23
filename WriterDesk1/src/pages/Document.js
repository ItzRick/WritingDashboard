// materials
import {
  Typography,
  Tooltip,
} from "@mui/material";

// routing
import { useOutletContext, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';

// show pdf
import React from 'react';
import AllPagesPDFViewer from "../components/ShowPDF";
import "../css/styles.css";
import "../css/Document.css";
import Plot from 'react-plotly.js';

// tracking
import { useContext } from 'react';
import { TrackingContext } from '@vrbo/react-event-tracking';

// authentication
import { authHeader } from "../helpers/auth-header";

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

  const [scoreStyle, setScoreStyle] = useState();
  const [scoreStructure, setScoreStructure] = useState();
  const [scoreCohesion, setScoreCohesion] = useState();
  const [scoreIntegration, setScoreIntegration] = useState();

  const [explanations, setExplanations] = useState([]);

  // context as given by the Tracking Provider
  const tc = useContext(TrackingContext);

  useEffect(() => {
    setTitle('Document');
  });

  useEffect(() => {
    const fileId = location.state.fileId; // Get file id from previous page.
    fetchFilePath(fileId); // Set file path and type
    fetchScores(fileId); // Set scores of current file
    fetchExplanations(fileId); //Set mistakes of current file
  }, [location.state.fileId]);


  /**
   * Make the backend call to retrieve the correct file and
   * set the correct path and file type for the given file id.
   * @param {number} fileId: id of the file that needs to be shown.
   */
  const fetchFilePath = (fileId) => {
    // Url of the server:
    const url = 'https://api.writingdashboard.xyz/fileapi/getFileById';

    // Make the call to the backend:
    axios.get(url, { params: { fileId: fileId }, headers: authHeader() })
      .then((response) => {
        setPath(response.data.path); // Set path of file given by file id
        setType(response.data.filetype.substring(1)); // Set file type without '.'
      })
  }


  /**
   * Make the backend call to retrieve and set the correct scores for the given file id.
   * @param {number} fileId: id of the file that that is shown.
   */
  const fetchScores = (fileId) => {
    // // Url of the server:
    const url = 'https://api.writingdashboard.xyz/scoreapi/getScores';

    // Make the call to the backend:
    axios.get(url, { params: { fileId: fileId } })
      .then((response) => {
        setScoreStyle(response.data.scoreStyle);
        setScoreStructure(response.data.scoreStructure);
        setScoreCohesion(response.data.scoreCohesion);
        setScoreIntegration(response.data.scoreIntegration);
      })
  }

  /**
   * Make the backend call to retrieve and set the correct explanations for the given file id.
   * @param {number} fileId: id of the file that that is shown.
   */
  const fetchExplanations = (fileId) => {
    // Url of the server:
    const url = 'https://api.writingdashboard.xyz/scoreapi/getExplanationForFile';

    // Make the call to the backend:
    axios.get(url, { params: { fileId: fileId } })
      .then((response) => {
        let explanationsArray = []  // Array of all explanations in the response from the backend call
        for (let i = 0; i < response.data.length; i++) {  // Loop over all explanations
          // Append explanation to array
          explanationsArray = [...explanationsArray, response.data[i]];
        }
        setExplanations(explanationsArray);
      })
  }


  /**
   * Function to show all the explanation boxes that are being clicked.
   * In addition, notify the tracker of a click event
   * @param {Object} e - Click event
   * @param {Object} coords - Array of the coordinates of the mistake being clicked
   */
  const handleHighlightClick = (e, coords) => {
    let rect = e.target.getBoundingClientRect();
    let x = coords[0] + e.clientX - rect.left; // x-coordinate of click in document
    let y = coords[1] + e.clientY - rect.top; // y-coordinate of click in document

    let newArrShowTextbox = []; // Create new array to overwrite showTextbox

    for (let i = 0; i < explanations.length; i++) {
      // Loop over all mistakes to check if there is clicked on that mistake.
      let left = explanations[i].X1 - 2; // x1 of mistake[i] coordinates
      let right = explanations[i].X2 + 2; // x2 of mistake[i] coordinates
      let top = explanations[i].Y1; // y1 of mistake[i] coordinates
      let bottom = explanations[i].Y2; // y2 of mistake[i] coordinates

      //Set showTextbox true for every mistake that is clicked
      const hasBeenClicked = (left <= x) && (x <= right) && (top <= y) && (y <= bottom);
      newArrShowTextbox[i] = hasBeenClicked;
      //handle tracking
      if (tc.hasProvider && hasBeenClicked) {
        // set trigger with explanations type
        tc.trigger({
          eventType: 'click.highlight',
          buttonId: explanations[i].type,
        })
      }
    }
    setShowTextbox(newArrShowTextbox); // Overwrite showTextbox
  }

  /**
   * Function to get all unique rows of an object by the given keys.
   * @param {Object} arr - Array of dictionary rows to get only unique rows.
   * @param {Object} keyProps - Array of keys to base the unique rows on.
   * @return Modified array that only has all unique rows based on the given keys.
   */
  const unique = (arr, keyProps) => {
   const kvArray = arr.map(entry => {
     const key = keyProps.map(k => entry[k]).join('|');
     return [key, entry];
   });
   const map = new Map(kvArray);
   return Array.from(map.values());
  }


  /**
   * Function to show or hide all the explanations of one type. Call this function when clicking on the bar chart.
   * @param {number} type - Number for type of mistake
   */
  const showAllExplanationsOfType = (type) => {
    // Copy explanations array to newExpl
    const newExpl = explanations.map(obj => ({...obj}));

    // Add number to new array to distinguish after removing rows
    for (let i = 0; i < newExpl.length; i++) {
      newExpl[i].number = i;
    }

    const keys = ['explanation', 'mistakeText', 'type', 'replacement1', 'replacement2', 'replacement3'];
    const uniqueExpl = unique(newExpl, keys);  // Get all unique explanations to prevent showing duplicates

    let allOpenOfType = true; // Boolean that indicate if all explanations of given type are shown

    // Loop over all unique explanations
    for (const expl of uniqueExpl) {
      // Check if explanation of mistake is shown
      if (expl.type === type && !showTextbox[expl.number]) {
        allOpenOfType = false; // Not all explanations of the given type are shown
      }
    }

    let newArrShowTextbox = []; // Create new array to overwrite showTextbox

    for (const expl of uniqueExpl) {
      if (expl.type === type) {
        // Show all explanations of the given type
        // If this is already the case, hide them all
        newArrShowTextbox[expl.number] = !allOpenOfType;
      }
    }
    setShowTextbox(newArrShowTextbox); // Overwrite showTextbox
  }

  // tracking
  const eventFields = {
    location: 'searchbar',
    name: 'SomeComponent'
  };
  const eventOptions = { asynchronous: 'true' };


  /**
   * Div that shows the explanation of a mistake being clicked
   * @property {number} number - Number of mistake
   * @property {number} type - Number for type of mistake
   * @property {String} expl - Explanation of the mistake
   * @property {Object} replacements - Array of max 3 replacements for the mistake
   * @returns TextBoxExplanation component
   */
  const TextBoxExplanation = (props) => {
    return (<>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <div className={showTextbox[props.number] ? 'textBoxExpl' : 'hidden'} id={'textBoxExpl' + props.number}
          style={{ backgroundColor: typeToColor(props.type), borderColor: typeToColor(props.type) }}>
          <Typography className='textBoxType' style={{ color: typeToColor(props.type), fontSize: 'calc(8px + 0.5vw)' }}>
            <b>{typeToName(props.type)}</b>
          </Typography>
          <Typography variant='body1' className='textBoxWord' style={{ fontSize: 'calc(12px + 0.3vw)' }}>
            <b>{props.text}</b>
          </Typography>
          <Typography variant='body2' sx={{ marginTop: '5px', marginBottom: '10px', fontSize: 'calc(12px + 0.2vw)' }}>
            {props.expl}
          </Typography>
          <Typography className={props.replacements.length > 0 && props.replacements[0] !== '' ? 'replacementsText' : 'hidden'}
            style={{ fontSize: 'calc(11px + 0.2vw)' }} variant='body2'>
            Possible replacements:
          </Typography>
          <Typography className={props.replacements.length > 0 && props.replacements[0] !== '' ? 'textBoxReplacements' : 'hidden'}
            variant='body1'
            style={{
              borderColor: typeToColor(props.type), fontSize: 'calc(11px + 0.2vw)',
              marginLeft: 'calc(2px + 0.2vw)', marginRight: 'calc(2px + 0.2vw)'
            }}>
            {props.replacements[0]}
          </Typography>
          <Typography className={props.replacements.length > 1 && props.replacements[1] !== '' ? 'textBoxReplacements' : 'hidden'}
            variant='body1'
            style={{
              borderColor: typeToColor(props.type), fontSize: 'calc(11px + 0.2vw)',
              marginLeft: 'calc(2px + 0.2vw)', marginRight: 'calc(2px + 0.2vw)'
            }}>
            {props.replacements[1]}
          </Typography>
          <Typography className={props.replacements.length > 2 && props.replacements[2] !== '' ? 'textBoxReplacements' : 'hidden'}
            variant='body1'
            style={{
              borderColor: typeToColor(props.type), fontSize: 'calc(11px + 0.2vw)',
              marginLeft: 'calc(2px + 0.2vw)', marginRight: 'calc(2px + 0.2vw)'
            }}>
            {props.replacements[2]}
          </Typography>
        </div>
      </div>
    </>
    );
  };


  /**
   * Transparent div that handles onClick events on highlighted text
   * @property {Object} coords - Array of the coordinates on the page where the mistake is
   * @property {number} type - Number for type of mistake
   * @returns ClickableTextDiv component
   */
  const ClickableTextDiv = (props) => {
    return (
      <div onClick={e => handleHighlightClick(e, props.coords)} className='clickableTextDiv'
        style={{
          backgroundColor: typeToColor(props.type), left: props.coords[0] - 2, top: props.coords[1],
          width: props.coords[2] - props.coords[0] + 4,
          height: props.coords[3] - props.coords[1], borderRadius: '4px'
        }}>
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
      return '#785EF080'
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
      return 'Language & Style'
    } else if (type === 1) {
      return 'Cohesion'
    } else if (type === 2) {
      return 'Structure'
    } else {
      return 'Source Integration & Content'
    }
  };


  return (
    <>
      <div className="all-page-container" id="all-page-container" style={{ width: '50%' }}>
        {/** potentially convert document to pdf and show document on page */}
        <AllPagesPDFViewer
          pdf={`https://api.writingdashboard.xyz/fileapi/display?filepath=${path}&filetype=${type}`}
          docId={location.state.fileId}
          docName={location.state.fileName}
        />
        {explanations.map((explanation, i) =>
          <ClickableTextDiv
            key={explanation.explId} number={i}
            coords={[explanation.X1, explanation.Y1, explanation.X2, explanation.Y2]} type={explanation.type}
          />
        )}
      </div>
      <div className='rightFloat' style={{ width: '50%' }}>
        {/* The barchart for the scores of this tool: */}
        <Plot
          data={[
            {
              // Order of the bars is as follows: first source integration, then cohesion, then structure, then language & style:
              x: ['Language & Style', 'Cohesion', 'Structure', 'Source Integration & <br> Content'],
              y: [scoreStyle, scoreCohesion, scoreStructure, scoreIntegration],
              marker: { color: ['#785EF0', '#FE6100', '#FFB000', '#DC267F'] },
              type: 'bar',
            },
          ]}
          // The title of the char is 'scores':
          layout={{
            // title: 'Scores',
            margin: { l: 50, r: 50, b: 40, t: 30, pad: 4 },
            // Scores can be between 0 and 10, so the y-axis range is set accordingly:
            yaxis: {
              range: [0, 10],
              fixedrange: true,
              type: 'linear'
            },
            xaxis: {
              fixedrange: true,
            }
          }}
          // Do not display the plotly modebar:
          config={{
            displayModeBar: false, // this is the line that hides the bar.
          }}
          // Show all explanations of the clicked type
          onClick={(data) => {
            showAllExplanationsOfType(data.points[0].pointNumber);
          }}
          // So the chart can resize:
          useResizeHandler={true}
          style={{ width: '100%', height: '300px' }}
          onHover={e => {
            e.event.target.style.cursor = 'pointer' // Changes cursor on hover to pointer
          }}
          onUnhover={e => {
            e.event.target.style.cursor = 'default' // Change cursor back on unhover
          }}
        />

        <hr className="horizontalline" />

        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <Tooltip title="Display feedback Language and Style.">
            <button className="buttonShowExplanationsStyle" onClick={e => showAllExplanationsOfType(0)}>Language & Style</button>
          </Tooltip>
          <Tooltip title="Display feedback Cohesion.">
            <button className="buttonShowExplanationsCohesion" onClick={e => showAllExplanationsOfType(1)}>Cohesion</button>
          </Tooltip>
          <Tooltip title="Display feedback Structure.">
            <button className="buttonShowExplanationsStructure" onClick={e => showAllExplanationsOfType(2)}>Structure</button>
          </Tooltip>
          <Tooltip title="Display feedback Source Integration and Content.">
            <button className="buttonShowExplanationsIntegration" onClick={e => showAllExplanationsOfType(3)}>Source Integration & Content</button>
          </Tooltip>
        </div>

        <br />

        {explanations.map((explanation, i) =>
          <TextBoxExplanation
            key={explanation.explId} number={i} text={explanation.mistakeText}
            type={explanation.type} expl={explanation.explanation}
            replacements={[explanation.replacement1, explanation.replacement2, explanation.replacement3]}
          />
        )}
      </div>
    </>
  );
}

export default Document;