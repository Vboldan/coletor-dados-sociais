import csv
import os
import uvicorn
from typing import Optional
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Coletor de Dados Sociais - Morena Dados")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ATUALIZADO: Agora aponta direto para o ponto de montagem do pendrive
FILE_NAME = "/home/usuario/Área de trabalho/dados_coletados.csv"

# Cria o arquivo CSV com cabeçalho na REDE se ele não existir por algum motivo
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["CEP", "Bairro", "Gênero", "Etnia", "Idade", "Profissão", "Escolaridade", "Transporte", "Asfalto", "Saúde"])

@app.post("/salvar")
async def salvar_dados(
    cep: str = Form(...), 
    bairro: str = Form(...), 
    genero: str = Form(...),
    etnia: str = Form(...), 
    idade: int = Form(...), 
    profissao: Optional[str] = Form("Não se aplica"),      # Opcional para < 14 anos
    escolaridade: Optional[str] = Form("Sem idade escolar"), # Opcional para < 4 anos
    transporte: str = Form(...), 
    asfalto: str = Form(...), 
    saude: str = Form(...)
):
    # Tratamento caso venham vazios do formulário
    if not profissao or profissao.strip() == "":
        profissao = "Não se aplica"
    if not escolaridade or escolaridade.strip() == "":
        escolaridade = "Sem idade escolar"

    with open(FILE_NAME, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([cep, bairro, genero, etnia, idade, profissao, escolaridade, transporte, asfalto, saude])
        f.flush()  # <--- ADICIONE ESTA LINHA AQUI! Ela força a gravação imediata no pendrive.
        
    return {"mensagem": "Dados salvos com sucesso!"}

if __name__ == "__main__":
    print("Iniciando o servidor do Coletor de Dados...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
