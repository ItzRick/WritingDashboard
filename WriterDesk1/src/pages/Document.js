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

  useEffect(() => {
    setTitle('Document');
  });

  const path = 'C:\\Users\\20183163\\PycharmProjects\\SEP2021\\WriterDesk1\\src\\example2.pdf'
  const type = 'pdf'

  const handleScroll = (e) => {

    console.log("scrollTop", e.target.scrollTop);
    console.log("scrollHeight", e.target.scrollHeight);
    console.log("scrollWidth", e.target.scrollWidth);
  }

  const mistakes = [
  {name: 1, explanation: 'expl1', color: 'rgba(200, 0, 0, 0.3)', coords: [156.9016876220703, 157.89927673339844, 183.29876708984375, 169.56455993652344]},
  {name: 2, explanation: 'expl2', color: 'rgba(0, 200, 0, 0.3)', coords: [464.495361328125, 468.1363525390625, 514.29833984375, 480.14129638671875]},
  {name: 3, explanation: 'expl3', color: 'rgba(0, 0, 200, 0.3)', coords: [126.9016876220703, 157.89927673339844, 213.29876708984375, 169.56455993652344]}
  ];


  const handleClick = (e) => {
    let rect = e.target.getBoundingClientRect();
    let x = e.clientX - rect.left;
    let y = e.clientY - rect.top;


    for (let i = 0; i < mistakes.length; i++) {
      if ((mistakes[i].coords[0] <= x) && (x <= mistakes[i].coords[2]) && (mistakes[i].coords[1] <= y) && (y <= mistakes[i].coords[3])) {
        console.log(x, y);
        document.getElementById('textBoxExpl' + i).style.display = "block";
      } else {
        document.getElementById('textBoxExpl' + i).style.display = "none";
      }
    }

  }

  const mousePointer = (e) => {
    let rect = e.target.getBoundingClientRect();
    let x = e.clientX - rect.left;
    let y = e.clientY - rect.top;
    let setPointer = false;


    for (let i = 0; i < mistakes.length; i++) {
      if (((mistakes[i].coords[0] <= x) && (x <= mistakes[i].coords[2]) && (mistakes[i].coords[1] <= y) && (y <= mistakes[i].coords[3]))) {
        setPointer = true
      }
    }

    if (setPointer) {
        document.getElementById('all-page-container').style.cursor = "pointer";
    } else {
        document.getElementById('all-page-container').style.cursor = "default";
    }

  }

  const TextBoxExplanation = props => (
      <div className='textBoxExpl' id={'textBoxExpl' + props.number} style={{backgroundColor: props.color, borderColor:props.color}}>
        <Typography>{props.mistake}</Typography>
        <Typography>{props.expl}</Typography>
      </div>
  )


  return (
    <>
      <div className="all-page-container" id="all-page-container" onClick={e=>handleClick(e)} onScroll={(e) => handleScroll(e)} onMouseMove={(e) => mousePointer(e)}>
        <AllPagesPDFViewer pdf={`http://127.0.0.1:5000/converttopdf/convert?filepath=${path}&filetype=${type}`} />
      </div>
      <div className='rightFloat'>
        <img className='smallGraph' src={placeholder} />
        <br />

        {/*<TextBoxExplanation mistake={'mistake'} color = {'rgba(200, 0, 0, 0.3)'}/>*/}
        {mistakes.map((mistake, i) => <TextBoxExplanation key={i} number={i} mistake={mistake.name} color={mistake.color} expl={mistake.explanation}/>)}
      </div>
    </>

  );
}

export default Document;