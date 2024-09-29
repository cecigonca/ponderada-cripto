import React from 'react';
import './Navbar.css'; 

function Navbar() {
  return (
    <nav className="navbar">
      <button className="nav-button" onClick={() => window.location.href = '/Dashboard'}>DASHBOARD</button>
      <button className="nav-button" onClick={() => window.location.href = '/Predicao'}>PREDIÇÃO</button>
    </nav>
  );
}

export default Navbar;
