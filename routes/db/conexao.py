import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DBNAME = os.getenv('DBNAME')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

def conectar():
    try:
        conexao = psycopg2.connect(
            dbname=DBNAME,
            user=USER,           
            password=PASSWORD, 
            host=HOST, 
            port=PORT
        )
        print("[OK] Conexão estabelecida com sucesso!, Ação bem sucedida!")
        return conexao
    except Exception as e:
        print(f"[ERRO] Falha na conexão: {e}")
        return None
