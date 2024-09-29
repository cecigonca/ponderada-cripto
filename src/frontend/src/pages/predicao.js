import React from 'react';
import Navbar from '../components/Navbar';  // Certifique-se que o caminho da Navbar está correto
import './Predicao.css';  // Você pode criar um arquivo CSS separado para estilizar a página de predição

function Predicao() {
  return (
    <div className="predicao-container">
      <Navbar />  {/* Adicionando a Navbar na página de predição */}
      
      <h1>Predição dos Preços do Ethereum</h1>

      {/* Adicione aqui os elementos necessários para a página de predição */}
      <div className="predicao-content">
        {/* Isso pode ser um gráfico, uma tabela, ou qualquer visualização relacionada à predição */}
        <p>Aqui estará o conteúdo da predição</p>
      </div>
    </div>
  );
}

export default Predicao;
