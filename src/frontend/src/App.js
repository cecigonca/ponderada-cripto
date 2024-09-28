import React from 'react';
import './App.css';
import Dashboard from './pages/Dashboard';  // Certifique-se que o nome do arquivo é "Dashboard.js" e não "dashbord.js"

function App() {
  return (
    <div className="App">
      <Dashboard />  {/* Substitua o componente Home por Dashboard */}
    </div>
  );
}

export default App;
