import logo from './logo.svg';
import './App.css';

import { BsArrowsMove } from "react-icons/bs";   // App Logo

import React from 'react';
import ReactDOM from 'react-dom';

import Editor from '@monaco-editor/react';


function App() {
  return (

    
    <div className="App">

      <header className="App-header-coder">
        <div className="App-logo-Coder">
          <BsArrowsMove size={25} />
        </div>
      </header>

      <header className="App-header">

      <Editor  
    width = "50vw"
    height= "70vh"
    theme="vs-dark"
    defaultLanguage={"python"}
    defaultValue="# write your code here"
    
    />



      </header>
    </div>
  );
  
}

export default App;
