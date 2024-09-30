import React from 'react';
import Navbar from '../components/Navbar';
import './Dashboard.css';

function Dashboard() {
  return (
    <div className="dashboard-container">
      <Navbar /> 
      <h1>Gráficos para Análise do Último Ano</h1>
      <div className="graphs-container">
        <div className="graph">
          <img src="/grafico1.png" alt="Gráfico 1" />
        </div>
        <div className="graph">
          <img src="/grafico2.png" alt="Gráfico 2" />
        </div>
        <div className="graph">
          <img src="/grafico3.png" alt="Gráfico 3" />
        </div>
        <div className="graph">
          <img src="/grafico4.png" alt="Gráfico 4" />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;


