from dotenv import load_dotenv
from psycopg2.pool import SimpleConnectionPool
import os

load_dotenv()

pool = SimpleConnectionPool(  
    minconn= 1,
    maxconn= 10,  
    host= os.getenv("DB_HOST"),
    database= os.getenv("DB_NAME"),
    user= os.getenv("DB_USER"),
    password= os.getenv("DB_PASS"),
    port= os.getenv("DB_PORT"),
    sslmode = "require"
)

def conexao():
    return pool.getconn()

def liberarConexao(conecta):
    pool.putconn(conecta)