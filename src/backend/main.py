from fastapi import FastAPI, File, UploadFile, HTTPException
import logging
import uvicorn
import os
import shutil
import pandas as pd
from src.backend.modelos import executar_modelos, processar_csv 
from fastapi.middleware.cors import CORSMiddleware

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
LOG_FILE = os.path.join(LOG_DIR, "arquivo_logs")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Onde salva arquivos para retreino
UPLOAD_DIRECTORY = "uploaded_data"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.get("/")
def root():
    return {"message": "API está funcionando"}

@app.post("/inserirBase")
async def inserir_base(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logging.info(f"Arquivo '{file.filename}' salvo em {file_location}")
        df_anexado = pd.read_csv(file_location)  
        processar_csv(df_anexado) 
        return {"info": f"Arquivo '{file.filename}' salvo e processado com sucesso."}
    except Exception as e:
        logging.error(f"Erro ao salvar o arquivo '{file.filename}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao salvar o arquivo: {str(e)}")

@app.get("/executar_modelos")
def executar_todos_modelos():
    try:
        logging.info("Executando todos os modelos.")
        pred_gru, pred_arima, pred_hwinters, pred_rf, recomendacao = executar_modelos()  
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