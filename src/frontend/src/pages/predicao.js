import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import './Predicao.css';  // Certifique-se de ajustar o CSS para o layout

function Predicao() {
  const [previsoes, setPrevisoes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [file, setFile] = useState(null);

  // Função para executar a chamada à API e obter previsões
  const handlePrediction = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://127.0.0.1:8000/executar_modelos');
      const data = await response.json();
      setPrevisoes(data);
    } catch (err) {
      setError('Erro ao executar os modelos. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  // Função para carregar um novo dataset e executar o retrain
  const handleUpload = async () => {
    if (!file) {
      setError('Nenhum arquivo selecionado');
      return;
    }
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/inserirBase', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      alert(data.info);
      handlePrediction();  // Executar os modelos após o upload bem-sucedido
    } catch (err) {
      setError('Erro ao carregar o arquivo.');
    }
  };

  return (
    <div className="predicao-container">
      <Navbar />
      <h1>Predição dos Preços do Ethereum</h1>

      <div className="button-container">
        <button onClick={handlePrediction} className="button">
          Predição Ethereum
        </button>

        <div className="file-input-wrapper">
          <label htmlFor="file-upload" className="file-input-label">
            Subir Nova Base de Dados
          </label>
          <input
            id="file-upload"
            type="file"
            className="file-input"
            onChange={(e) => setFile(e.target.files[0])}
          />
        </div>
        

        <button onClick={handleUpload} className="button">
          Subir Nova Base de Dados e Retreinar
        </button>
      </div>

      {previsoes && (
        <div className="prediction-results">
          <p className="recommendation">
            <strong>Recomendação:</strong> {previsoes.recomendacao}
          </p>

          <div className="result-container">
            <div className="table-section">
              <h2>Resultados da Predição</h2>
              <table>
                <thead>
                  <tr>
                    <th>Modelo</th>
                    <th>Previsões</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>GRU</td>
                    <td>{previsoes.previsoes.GRU.join(', ')}</td>
                  </tr>
                  <tr>
                    <td>ARIMA</td>
                    <td>{previsoes.previsoes.ARIMA.join(', ')}</td>
                  </tr>
                  <tr>
                    <td>Holt-Winters</td>
                    <td>{previsoes.previsoes.Holt_Winters.join(', ')}</td>
                  </tr>
                  <tr>
                    <td>Random Forest</td>
                    <td>{previsoes.previsoes.Random_Forest.join(', ')}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div className="graph-section">
              <h2>Gráfico de Previsão</h2>
              <img src="/graph_output.png" alt="Gráfico de Previsões" />
            </div>
          </div>
        </div>
      )}

      {loading && <p>Carregando...</p>}
      {error && <p>{error}</p>}
    </div>
  );
}

export default Predicao;
