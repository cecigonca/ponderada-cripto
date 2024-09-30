import React from 'react';
import { Link } from 'react-router-dom'; 
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/dashboard" className="nav-button">DASHBOARD</Link>
      <Link to="/predicao" className="nav-button">PREDIÇÃO</Link>
    </nav>
  );
}

export default Navbar;
