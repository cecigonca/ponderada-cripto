from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from modelos import modelo_gru, modelo_arima, modelo_hwinters, modelo_random_forest
import logging
from utils.file_handler import save_file
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'dados')

app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_origins=["*"]
)

@app.get("/hello")
def principal():
    logging.info("Rota /hello acessada")
    return {"message": "Hello, World!"}

@app.post("/novabase")
async def inserir_base(file: UploadFile = File(...)):
    try:
        file_location = save_file(file, DATA_DIR)
        logging.info(f"Arquivo '{file.filename}' salvo com sucesso em {file_location}.")
        return {"info": f"Arquivo '{file.filename}' salvo com sucesso em {file_location}"}
    except Exception as e:
        logging.error(f"Erro ao salvar o arquivo '{file.filename}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao salvar o arquivo: {str(e)}")

@app.get("/executar/gru")
def executar_gru():
    try:
        logging.info("Executando GRU")
        predictions = modelo_gru()
        logging.info(f"Previsão GRU: {predictions[:5]}") 
        return {"predictions": predictions.tolist()}
    except Exception as e:
        logging.error(f"Erro ao executar o modelo GRU: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao executar o modelo GRU: {str(e)}")

@app.get("/executar/arima")
def executar_arima():
    try:
        logging.info("Executando ARIMA")
        predictions = modelo_arima()
        logging.info(f"Previsão ARIMA: {predictions[:5]}")  # Log das 5 primeiras previsões
        return {"predictions": predictions.tolist()}
    except Exception as e:
        logging.error(f"Erro ao executar o modelo ARIMA: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao executar o modelo ARIMA: {str(e)}")

@app.get("/executar/holtwinters")
def executar_holt_winters():
    try:
        logging.info("Executando Holt-Winters")
        predictions = modelo_hwinters()
        logging.info(f"Previsão Holt-Winters: {predictions[:5]}")  # Log das 5 primeiras previsões
        return {"predictions": predictions.tolist()}
    except Exception as e:
        logging.error(f"Erro ao executar o modelo Holt-Winters: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao executar o modelo Holt-Winters: {str(e)}")

@app.get("/executar/randomforest")
def executar_random_forest():
    try:
        logging.info("Executando Random Forest")
        predictions = modelo_random_forest()
        logging.info(f"Previsão Random Forest: {predictions['predictions'][:5]}, Acurácia: {predictions['accuracy']}")
        return {"accuracy": predictions['accuracy'], "predictions": predictions['predictions'].tolist()}
    except Exception as e:
        logging.error(f"Erro ao executar o modelo Random Forest: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao executar o modelo Random Forest: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
