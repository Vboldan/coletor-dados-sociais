import os
import uvicorn
from typing import Optional
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI(title="Coletor de Dados Sociais - Morena Dados")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URL de conexão EXTERNA do PostgreSQL no Render
DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql://banco_coletor_user:4K8UcYQDwjqGp85eKrgXxB5yX6JXa1lf@dpg-d9lvul8ae00c73b613q0-a.oregon-postgres.render.com/banco_coletor"
)

def obter_conexao():
    return psycopg2.connect(DATABASE_URL)

# Função para garantir que a tabela Respostas existe no banco
def criar_tabela_se_nao_existir():
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "Respostas" (
                id SERIAL PRIMARY KEY,
                "CEP" VARCHAR(20),
                "Bairro" VARCHAR(100),
                "Gênero" VARCHAR(50),
                "Raça" VARCHAR(50),
                "Idade" VARCHAR(10),
                "Escolaridade" VARCHAR(100),
                "Avaliação_Transporte" VARCHAR(50),
                "Avaliação_Pavimentação" VARCHAR(50),
                "Avaliação_Posto_Saúde" VARCHAR(50)
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Tabela 'Respostas' verificada/criada com sucesso no PostgreSQL!")
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")

# Executa a verificação ao iniciar
criar_tabela_se_nao_existir()

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
        conn = obter_conexao()
        cursor = conn.cursor()
        
        sql = """
            INSERT INTO "Respostas" 
            ("CEP", "Bairro", "Gênero", "Raça", "Idade", "Escolaridade", "Avaliação_Transporte", "Avaliação_Pavimentação", "Avaliação_Posto_Saúde")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        valores = (
            cep, bairro, genero, etnia, str(idade), escolaridade, 
            transporte, asfalto, saude
        )
        
        cursor.execute(sql, valores)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {"mensagem": "Dados salvos com sucesso no PostgreSQL do Render!"}

    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}

# Rota para visualizar todos os dados salvos no banco
@app.get("/listar")
async def listar_dados():
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "Respostas";')
        
        # Pega o nome das colunas dinamicamente
        colunas = [desc[0] for desc in cursor.description]
        resultados = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return {"total": len(resultados), "dados": resultados}
    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}

if __name__ == "__main__":
    print("Iniciando o servidor do Coletor de Dados...")
    uvicorn.run(app, host="0.0.0.0", port=8000)