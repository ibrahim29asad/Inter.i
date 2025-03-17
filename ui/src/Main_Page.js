import logo from './logo.svg';
import './App.css';

import { BsArrowsMove } from "react-icons/bs";   // App Logo
import { FaQuestion } from "react-icons/fa";     // info button

function App() {
  return (
    <div className="App">
      <header className="App-header">
       <div className= "App-logo">
       <BsArrowsMove size = {80}/>
       </div>
        <p>
          Welcome to Inter.i
        </p>
        
        <a
          className="Start-link-Button"
        >
          Start
        </a>

        <a
          className="Question-link-Button"
        >
          <FaQuestion size = {15}/>
        </a>


      </header>
    </div>
  );
}

export default App;
