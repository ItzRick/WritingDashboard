import {useEffect, useState} from 'react'
import axios from "axios";
import logo from './logo.svg';
import './App.css';
import React from 'react';
import ReactDOM from 'react-dom';


function App() {

    // new line start
    const [profileData, setProfileData] = useState(null)
    const [textStr, setTextStr] = useState(null);

    function getDataText() {

        axios({
            method: "GET",
            url: "/text",
        })
            .then((response) => {
                const res = response.data
                setTextStr(({
                    text: res.text,
                    background: res.background
                }))
            }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
        })
    }

    function getData() {
        axios({
            method: "GET",
            url: "/profile",
        })
            .then((response) => {
                const res = response.data
                setProfileData(({
                    profile_name: res.name,
                    about_me: res.about
                }))
            }).catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
        })
    }

    function multipleTexts() {
        let textArr = textStr.text.split('');
        let bgArr = textStr.background.split(',');
        let divs = [];
        for (let i = 0; i < textArr.length; i++) {
            if (textArr[i] == '\n') {
                divs.push(<br/>);
            }
            else if (bgArr.includes('' + i)) {
                divs.push(<Text value1={textArr[i]} value2={'red'}/>);
            }
            else {
                divs.push(<Text value1={textArr[i]} value2={'none'}/>);
            }
        }
        return divs;
    }


    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo"/>
                <p>
                    Edit <code>src/App.js</code> and save to reload.
                </p>
                <a
                    className="App-link"
                    href="https://reactjs.org"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Learn React
                </a>

                {/* new line start*/}
                <div id="textDiv">
                    {getDataText()}
                    {textStr && multipleTexts()}
                </div>

                <p>To get your profile details: </p>
                <button onClick={getData}>Click me</button>
                {profileData && <div>
                    <p>Profile name: {profileData.profile_name}</p>
                    <p>About me: {profileData.about_me}</p>
                </div>
                }
                {/* end of new line */}
            </header>
        </div>
    );
}

class Text extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            character: props.value1,
            background: props.value2
        };
    }
    render() {
        return (
            <span style={{backgroundColor: this.props.value2}}>{this.props.value1}</span>
        )
    }
}

export default App;