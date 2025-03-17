import logo from './logo.svg';
import './App.css';

import { BsArrowsMove } from "react-icons/bs";

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
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
