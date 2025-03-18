import './App.css';
import { BsArrowsMove } from "react-icons/bs";   // App Logo
import React, { useState } from "react";
import ReactDOM from 'react-dom';
import Editor from '@monaco-editor/react';

import axios from 'axios'; // handles API HTTP Call Requests



function App() {
  // creates functions
  const [output, setOutputs] = useState("# Enter your code here");  // for code
  const [loading, setLoadings] = useState("");
  
  // handles when code changes 
  const handleCodeChange = (newCode) => {
    setOutputs(newCode);
  };
  
  // Function to execute the code
  const codeExecution = async () =>  {
    // setLoading(true); // Set loading to true while the request is being made

    const options = {
    method: 'POST',
    url: 'https://judge029.p.rapidapi.com/submissions',
    params: {
      base64_encoded: 'true', // allows for printing (Keep right now for Testing) - set true
      wait: 'true' // allows for you to get responses quickly
    },

    headers: {
      'x-rapidapi-key': process.env.REACT_APP_JUDGE0_KEY, //API Key
      'x-rapidapi-host': 'judge029.p.rapidapi.com',
      'Content-Type': 'application/json'
    },
    
    data: {
      source_code: output, // this is my code that i would enter into the editor
      language_id: 71,
      stdin: "",
    }
  };
 
  try {
    const response = await axios.request(options);
    setLoadings(true); // Set loading to false after the request
    console.log(response.data || "No Output");
  } catch (error) {
    setLoadings(true); // Set loading to false in case of an error
    console.error(error);
  }
  };

  return (

    

    
    <div className="App">

      <header className="App-header-coder">
        <div className="App-logo-Coder">
          <BsArrowsMove size={25} />
        </div>
      </header>

      <header className="App-coder-main">

    <div className="Coder-container">
      <Editor  
    width = "50vw"
    height= "70vh"
    theme="vs-dark"
    defaultLanguage={"python"}
    defaultValue="# Enter your code here"
    onChange={handleCodeChange}
    />


        <button onClick={codeExecution} style={{ marginTop: "10px" }}>
          Run Code
        </button>
        <div className="output">
          <h3>Output:</h3>
          <pre>{codeExecution}</pre>
        </div>


    </div>

    


      </header>
    </div>
  );
  
}

export default App;
