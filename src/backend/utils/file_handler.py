import os
from fastapi import UploadFile

def save_file(file: UploadFile, directory: str) -> str:
    """Função para salvar o arquivo em um diretório específico"""
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_location = os.path.join(directory, file.filename)
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_location
