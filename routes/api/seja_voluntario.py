from flask import Blueprint, jsonify, request
from extensions import limiter
from routes.db.conexao import conectar
from funcoes.validar_telefone import validar_telefone_final
from funcoes.validar_email import validar_email
from routes.utils.logger import logger
from funcoes.validar_mensagem import validar_msg
import datetime

seja_voluntario_bp = Blueprint('seja_voluntario_bp', __name__, url_prefix='/api')

@seja_voluntario_bp.route('/seja_voluntario', methods=['POST'])
@limiter.limit("3 per minute; 10 per hour")
def teste():
    dados = request.get_json()
    
    dados_obrigatorios = ['nome', 'email', 'telefone', 'disponibilidade', 'mensagem']
    if not all(campo in dados for campo in dados_obrigatorios):
        logger.warning(f"Tentativa de envio com campos faltando de {request.remote_addr}: {dados}")
        return jsonify({'error': 'Todos os campos devem estar preenchidos'}), 400
    
    nome = dados['nome']
    email = dados['email']
    telefone = dados['telefone']
    disponibilidade = dados['disponibilidade']
    mensagem = dados['mensagem']
    data_cadastro = datetime.datetime.now()
    
    email_valido = validar_email(email)
    if not email_valido:
        logger.warning(f"Tentativa de envio com email inválido de {request.remote_addr}: {email}")
        return jsonify({'error': 'Email inválido! Use um formato válido (ex.: usuario@dominio.com)'}), 400
    
    telefone_atualizado = validar_telefone_final(telefone)
    if not telefone_atualizado:
        logger.warning(f"Tentativa de envio com telefone inválido de {request.remote_addr}: {telefone}")
        return jsonify({'error': 'Digite um número de telefone válido'}), 400
    
    mensagem_atualizada = validar_msg(mensagem)
    if not mensagem_atualizada:
        logger.warning(f"Mensagem muito longa de {request.remote_addr}")
        return jsonify({'error': 'Mensagem muito longa'}),400
    
    
    try:
        logger.info(f"Requisição recebida de {request.remote_addr}: {dados}")
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute('''INSERT INTO seja_voluntario 
                       (nome, email, telefone, disponibilidade, mensagem, data_cadastro) 
                       VALUES (%s, %s, %s, %s, %s, %s)''',
                       (nome, email, telefone_atualizado, disponibilidade, mensagem_atualizada, data_cadastro))
       
        conn.commit()
        logger.info(f"Voluntário registrado com sucesso: {nome}")
        return jsonify({'message': 'Sucesso'})
    
    except Exception as e:
        logger.error(f"Erro ao inserir na base de dados: {str(e)}")
        return jsonify({'error': f'Erro ao inserir na base de dados: {str(e)}'}), 500
    
    finally:
        cursor.close()
        conn.close()