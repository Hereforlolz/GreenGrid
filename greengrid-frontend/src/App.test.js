import React, { useState, useEffect } from 'react';
import { Amplify, API } from 'aws-amplify';
import config from './aws-exports';
import './App.css'; // Basic CSS

Amplify.configure(config);

function App() {
  const [energyData, setEnergyData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedLanguage, setSelectedLanguage] = useState('English');

  useEffect(() => {
    fetchEnergyData();
  }, []);

  const fetchEnergyData = async () => {
    try {
      const response = await API.get('greengridapi', '/energydata'); // 'greengridapi' is your API name, '/energydata' is the path
      setEnergyData(response);
      setLoading(false);
      console.log("Fetched Data:", response); // Log to see the structure
    } catch (err) {
      console.error("Error fetching data:", err);
      setError(err);
      setLoading(false);
    }
  };

  if (loading) return <div className="container">Loading GreenGrid Data...</div>;
  if (error) return <div className="container error">Error: {error.message || "Failed to load data."}</div>;

  const insights = energyData.insights?.recommendations || {};

  return (
    <div className="App">
      <header className="App-header">
        <h1>🏡 GreenGrid Dashboard</h1>
        <p>Smart, Equitable Energy for Modern Neighborhoods</p>
      </header>

      <main className="container">
        <h2>Current & Forecasted Usage (Simulated)</h2>
        <div className="data-display">
          {energyData.forecastedData && energyData.forecastedData.map((d, index) => (
            <div key={index} className="data-item">
              <p><strong>Household {d.household_id}</strong> at {new Date(d.timestamp).toLocaleTimeString()}</p>
              <p>Forecasted: {d.power_kW.toFixed(2)} kW</p>
              <p>Optimized: {energyData.optimizedData[index]?.adjusted_power_kW.toFixed(2)} kW</p>
            </div>
          ))}
        </div>

        <h2>Personalized Energy Insights</h2>
        <div className="language-selector">
          <label htmlFor="language-select">View in: </label>
          <select
            id="language-select"
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
          >
            {Object.keys(insights).map(lang => (
              <option key={lang} value={lang}>{lang}</option>
            ))}
          </select>
        </div>
        <div className="insights-display">
          {insights[selectedLanguage] ? (
            <p>{insights[selectedLanguage]}</p>
          ) : (
            <p>No insights available for this language or data is still processing.</p>
          )}
        </div>

        <p className="impact-note">
          GreenGrid helps your neighborhood reduce bills, stabilize the grid, and meet climate goals together!
        </p>
      </main>
    </div>
  );
}

export default App;