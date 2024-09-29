from fastapi import FastAPI, File, UploadFile, HTTPException
import logging
import uvicorn
import os
from modelos import executar_modelos  # Importando a função de modelos
from fastapi.middleware.cors import CORSMiddleware

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configura o logging para salvar em arquivo
LOG_FILE = os.path.join(LOG_DIR, "arquivo_logs")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = FastAPI()

# Configurar CORS para permitir chamadas do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode restringir para seu frontend, se necessário
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API está funcionando"}

@app.get("/hello")
def principal():
    logging.info("Rota /hello acessada")
    return {"message": "Hello, World!"}

@app.post("/inserirBase")
async def inserir_base(file: UploadFile = File(...)):
    try:
        file_location = UPLOAD_DIRECTORY / file.filename
        # Salvando o arquivo na pasta especificada
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logging.info(f"Arquivo '{file.filename}' salvo em {file_location}")
        return {"info": f"Arquivo '{file.filename}' salvo com sucesso em {file_location}"}
    except Exception as e:
        logging.error(f"Erro ao salvar o arquivo '{file.filename}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao salvar o arquivo: {str(e)}")

@app.get("/executar_modelos")
def executar_todos_modelos():
    try:
        logging.info("Executando todos os modelos.")
        
        # Chamar a função que executa os modelos e capturar as previsões
        pred_gru, pred_arima, pred_hwinters, pred_rf, recomendacao = executar_modelos()  
        
        # Retornar os resultados dos modelos e a recomendação final
        return {
            "status": "Modelos executados com sucesso!",
            "previsoes": {
                "GRU": pred_gru.tolist(),
                "ARIMA": pred_arima.tolist(),
                "Holt_Winters": pred_hwinters.tolist(),
                "Random_Forest": pred_rf.tolist(),
            },
            "recomendacao": recomendacao
        }
    except Exception as e:
        logging.error(f"Erro ao executar os modelos: {str(e)}")
        return {"status": "Erro ao executar os modelos.", "detalhe": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)