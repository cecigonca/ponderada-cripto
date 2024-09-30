import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; 
import Dashboard from './pages/Dashboard';
import Predicao from './pages/Predicao';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/predicao" element={<Predicao />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
