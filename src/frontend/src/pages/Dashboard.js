import React from 'react';
import Navbar from '../components/Navbar';
import './Dashboard.css';  // Certifique-se que o arquivo CSS está na pasta correta

function Dashboard() {
  return (
    <div className="dashboard-container">
      <Navbar />  {/* Adicionando a Navbar */}

      <h1>Gráficos para Melhor Visualização</h1>

      <div className="graphs-container">
        {/* Adicione aqui os gráficos que você gerou na análise exploratória */}
        <div className="graph">Gráfico 1</div>
        <div className="graph">Gráfico 2</div>
        <div className="graph">Gráfico 3</div>
        <div className="graph">Gráfico 4</div>
      </div>
    </div>
  );
}

export default Dashboard;
