from flask import Blueprint, request, make_response, redirect, current_app,jsonify
from routes.db.conexao import conectar
from routes.utils.logger import logger
from extensions import limiter
import bcrypt
import jwt
import os
import datetime
from dotenv import load_dotenv

load_dotenv()


login_bp = Blueprint('login_bp', __name__, url_prefix='/api')

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "JWT_SECRET_KEY_KEY")

@login_bp.route('/login', methods=['POST'])
@limiter.limit("3 per minute; 10 per hour")
def verificar_login():

    if request.is_json:
        dados = request.get_json()
    else:
        dados = request.form

    nome_usuario = dados.get("nome")
    senha = dados.get("senha")

    if not nome_usuario or not senha:
        logger.warning(f"Tentativa de envio com campos faltando ou inexsistentes {request.remote_addr}:{dados}")
        return jsonify({"error":"Nome de usuário e senha são obrigatórios"}), 400

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id, nome, senha FROM usuarios WHERE nome = %s",
            (nome_usuario,)
        )
        resultado = cursor.fetchone()

        if not resultado:
            logger.warning(f"Tentativa de envio com nome incorreto {request.remote_addr}:{nome_usuario}")
            return jsonify({"error":"Nome de usuário ou senha incorretos"}), 400

        id_usuario, nome, hash_armazenado = resultado
        senha_bytes = senha.encode('utf-8')
        if isinstance(hash_armazenado, str):
            hash_armazenado = hash_armazenado.encode('utf-8')

        if not bcrypt.checkpw(senha_bytes, hash_armazenado):
            logger.warning(f"Tentativa de envio com senha incorreta {request.remote_addr}:{nome_usuario}")
            return jsonify({"error":"Nome de usuário ou senha incorretos"}), 400

        
        payload = {
            "id_usuario": id_usuario,
            "nome": nome,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")


        resp = make_response(redirect('/admin/eventos'))
        resp.set_cookie(
            'token',
            token,
            httponly=True,
            secure=False,
            max_age=3600
        )
        return resp

    except Exception as e:
        logger.error(f"Erro ao verificar login: {e}")
        return "Erro interno no servidor", 500

    finally:
        cursor.close()
        conexao.close()
