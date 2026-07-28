import os
import uvicorn
from typing import Optional
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

app = FastAPI(title="Coletor de Dados Sociais - Morena Dados")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pega as credenciais de forma segura pelas variáveis de ambiente do servidor
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Inicializa o cliente do Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.post("/salvar")
async def salvar_dados(
    cep: str = Form(...), 
    bairro: str = Form(...), 
    genero: str = Form(...),
    etnia: str = Form(...), 
    idade: int = Form(...), 
    profissao: Optional[str] = Form("Não se aplica"),
    escolaridade: Optional[str] = Form("Sem idade escolar"),
    transporte: str = Form(...), 
    asfalto: str = Form(...), 
    saude: str = Form(...)
):
    if not profissao or profissao.strip() == "":
        profissao = "Não se aplica"
    if not escolaridade or escolaridade.strip() == "":
        escolaridade = "Sem idade escolar"

    try:
        dados = {
            "CEP": cep,
            "Bairro": bairro,
            "Gênero": genero,
            "Raça": etnia,
            "Idade": str(idade),
            "Escoridade": escolaridade,
            "Avaliação_Pos": transporte,
            "Avaliação_Pav": asfalto,
            "Avaliação_Trar": saude
        }

        response = supabase.table("Respostas").insert(dados).execute()
        
        return {"mensagem": "Dados salvos com sucesso no Supabase!"}

    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}

if __name__ == "__main__":
    print("Iniciando o servidor do Coletor de Dados...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    