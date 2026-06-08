import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  const handleQueryChange = (event) => {
    setQuery(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/query', { query });
      setResponse(response.data.response);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="App">
      <header>
        <h1>RAG Chatbot</h1>
      </header>
      <main>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={query}
            onChange={handleQueryChange}
            placeholder="Ask a question..."
          />
          <button type="submit">Submit</button>
        </form>
        {response && (
          <div className="response">
            <p>{response}</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
