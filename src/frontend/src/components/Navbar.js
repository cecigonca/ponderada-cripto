import React from 'react';
import './Navbar.css'; // Certifique-se de que você criou o arquivo de CSS para estilizar a navbar.

function Navbar() {
  return (
    <nav className="navbar">
      <button onClick={() => window.location.href = '/dashboard'}>DASHBOARD</button>
      <button onClick={() => window.location.href = '/predicao'}>PREDIÇÃO</button>
    </nav>
  );
}

export default Navbar;
