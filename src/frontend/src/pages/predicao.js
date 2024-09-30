import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import './Predicao.css';

function Predicao() {
  const [previsoes, setPrevisoes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [file, setFile] = useState(null);

  const handlePrediction = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://127.0.0.1:8000/executar_modelos');
      const data = await response.json();
      setPrevisoes(data);
    } catch (err) {
      setError('Erro ao executar os modelos.');
    } finally {
      setLoading(false);
    }
  };

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
      handlePrediction();
    } catch (err) {
      setError('Erro ao carregar o arquivo.');
    }
  };

  return (
    <div className="predicao-container">
      <Navbar />
      <h1>Predição dos Preços</h1>
      <div className="button-container">
        <button onClick={handlePrediction} className="button">
          Predizer Ethereum
        </button>
        <div className="file-input-wrapper">
          <label htmlFor="file-upload" className="file-input-label">
            Selecionar Nova Base de Dados (.csv)
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
          </div>
        </div>
      )}

      {loading && <p>Carregando...</p>}
      {error && <p>{error}</p>}
    </div>
  );
}

export default Predicao;