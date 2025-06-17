import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');

  const fetchItems = async () => {
    try {
      const response = await fetch('https://x2sd07xt8j.execute-api.us-east-1.amazonaws.com/dev/items');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setMessage(JSON.stringify(data, null, 2));
    } catch (error) {
      setMessage('Error fetching items: ' + error.message);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to GreenGrid!</h1>
      </header>

      <div className="container">
        {/* Your existing placeholder content */}

        <div className="api-demo">
          <h3>API Demo</h3>
          <button onClick={fetchItems}>Fetch Items</button>
          <pre>{message}</pre>
        </div>
      </div>
    </div>
  );
}

export default App;
