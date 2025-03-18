
import React, { useState } from 'react';
import { BsArrowsMove } from "react-icons/bs"; // App Logo
import Editor from '@monaco-editor/react';
import axios from 'axios';

function App() {
  const [code, setCode] = useState("# Enter your code here");
  const [output, setOutput] = useState("");

  const handleCodeChange = (newCode) => {
    setCode(newCode);
  };

  const executeCode = async () => {
    const options = {
      method: "POST",
      url: "https://judge0-ce.p.rapidapi.com/submissions",
      params: { base64_encoded: "false", wait: "true" },
      headers: {
        "content-type": "application/json",
        "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com",
        "X-RapidAPI-Key": process.env.REACT_APP_JUDGE0_KEY, // Replace with your API key
      },
      data: {
        language_id: 71, // Python (adjust for different languages)
        source_code: code,
        stdin: "",
      },
    };

    try {
      const response = await axios.request(options);
      setOutput(response.data.stdout || response.data.stderr || "No output");
    } catch (error) {
      setOutput("Error executing code.");
    }
  };

  return (
    <div className="App">
      <header className="App-header-coder">
        <div className="App-logo-Coder">
          <BsArrowsMove size={25} />
        </div>
      </header>

      <div className="Coder-container">
        <Editor
          width="50vw"
          height="70vh"
          theme="vs-dark"
          defaultLanguage="python"
          value={code}
          onChange={handleCodeChange}
        />
        <button onClick={executeCode} style={{ marginTop: "10px" }}>
          Run Code
        </button>
        <div className="output">
          <h3>Output:</h3>
          <pre>{output}</pre>
        </div>
      </div>
    </div>
  );
}

export default App;
