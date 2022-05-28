// materials
import {Typography} from "@mui/material";

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';

import React from 'react';
import AllPagesPDFViewer from "../components/all-pages";
import "../css/styles.css";
import "../css/main.css";
import placeholder from '../images/chartImage.png';


/**
 *
 * @returns Documents Page
 */
function Document() {
  //set title in parent 'base'
  const { setTitle } = useOutletContext();

  const [file, setFile] = useState('');
  // const [scrollPosY, setScrollPosY] = useState(0);
  // const [mousePosY, setMousePosY] = useState(0);

  const [showTextbox, setShowTextbox] = useState([]);



  useEffect(() => {
    setTitle('Document');
  });

  const path = 'C:\\Users\\20183163\\PycharmProjects\\SEP2021\\WriterDesk1\\src\\example2.pdf'
  const type = 'pdf'

  const mistakes = [
  {text: 'decade', explanation: 'expl1', type: 0, coords: [156.9016876220703, 157.89927673339844, 183.29876708984375, 169.56455993652344], page: 0, replacements: ['a', 'b', 'c']},
  {text: 'Furthermore', explanation: 'expl2', type: 1, coords: [464.495361328125, 468.1363525390625, 514.29833984375, 480.14129638671875], page: 0, replacements: ['as']},
  {text: 'past decade, a new ', explanation: 'expl3', type: 2, coords: [126.9016876220703, 157.89927673339844, 213.29876708984375, 169.56455993652344], page: 0, replacements: ['a', 'b', 'c']},
  {text: 'semantics', explanation: 'expl4', type: 3, coords: [390.88116455078125, 66.0565185546875, 430.1736755371094, 78.06145477294922], page: 1, replacements: []}
  ];


  const handleClick = (e, coords, pageNr) => {
    let rect = e.target.getBoundingClientRect();
    let x = coords[0] + e.clientX - rect.left;
    let y = coords[1] + e.clientY - rect.top;

    let newArrShowTextbox = [...showTextbox];

    for (let i = 0; i < mistakes.length; i++) {
      let left = mistakes[i].coords[0];
      let right = mistakes[i].coords[2];
      let top = mistakes[i].coords[1];
      let bottom = mistakes[i].coords[3];
      let mistakePage = mistakes[i].page;
      newArrShowTextbox[i] = (left <= x) && (x <= right) && (top <= y) && (y <= bottom) && (pageNr === mistakePage);
    }
    setShowTextbox(newArrShowTextbox);
  }



  const TextBoxExplanation = (props) => {
    return(
    <div className={showTextbox[props.number] ? 'textBoxExpl' : 'hidden'} id={'textBoxExpl' + props.number}
         style={{backgroundColor: typeToColor(props.type), borderColor: typeToColor(props.type)}}>
      <Typography className='textBoxType' style={{color: typeToColor(props.type)}}><b>{typeToName(props.type)}</b></Typography>
      <Typography variant='body1' className='textBoxWord'><b>{props.text}</b></Typography>
      <Typography variant='body2' style={{clear: 'both', marginTop: '30px', marginBottom:'10px'}}>{props.expl}</Typography>
      <Typography className={props.replacements.length > 0 ? 'replacementsText' : 'hidden'} variant='body2'> Possible replacements:</Typography>
      <Typography className='textBoxReplacements' variant='body1' sx={{ marginLeft: 0.6, marginRight: 0.6 }} style={{backgroundColor: typeToColor(props.type)}}> {props.replacements[0]}</Typography>
      <Typography className='textBoxReplacements' variant='body1' sx={{ marginLeft: 0.6, marginRight: 0.6 }} style={{backgroundColor: typeToColor(props.type)}}> {props.replacements[1]}</Typography>
      <Typography className='textBoxReplacements' variant='body1' sx={{ marginLeft: 0.6, marginRight: 0.6 }} style={{backgroundColor: typeToColor(props.type)}}> {props.replacements[2]}</Typography>
    </div>
    );
  };

  const ClickableTextDiv = (props) => {
    let totalPageHeight = 792 * props.page; // TODO: Set correct page height
    return(
     <div onClick={e=>handleClick(e, props.coords, props.page)} className='clickableTextDiv'
          style={{left: props.coords[0], top: props.coords[1] + totalPageHeight,
            width: props.coords[2] - props.coords[0],
            height: props.coords[3] - props.coords[1]}}>
     </div>
    );
  };

  const typeToColor = (type) => {
    if (type === 0) {
      return 'rgba(100, 143, 255, 0.5)'
    } else if (type === 1) {
      return 'rgba(220, 38, 127, 0.5)'
    } else if (type === 2) {
      return 'rgba(254, 97, 0, 0.5)'
    } else {
      return 'rgba(255, 176, 0, 0.5)'
    }
  };

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
        <AllPagesPDFViewer pdf={`http://127.0.0.1:5000/converttopdf/convert?filepath=${path}&filetype=${type}`} />
        {mistakes.map((mistake, i) =>
          <ClickableTextDiv key={i} number={i} coords={mistake.coords} page={mistake.page}
          />
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