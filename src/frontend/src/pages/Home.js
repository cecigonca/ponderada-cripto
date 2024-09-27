import React from 'react';

const Home = () => {
  return (
    <div>
      <h1>Análise Exploratória de Dados</h1>
      {/* Exibe os gráficos que estão na pasta public */}
      <img src="/grafico_bollinger.png" alt="Gráfico Bollinger" style={{ width: '100%' }} />
      <img src="/grafico_closes.png" alt="Gráfico Closes" style={{ width: '100%' }} />
      <img src="/grafico_cross.png" alt="Gráfico Cross" style={{ width: '100%' }} />
    </div>
  );
};

export default Home;
