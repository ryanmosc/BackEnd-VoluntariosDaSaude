from flask import Blueprint, jsonify, request
from routes.utils.logger import logger
from extensions import limiter
from routes.db.conexao import conectar
from funcoes.validar_email import validar_email
from funcoes.validar_mensagem import validar_msg
import datetime

fale_conosco_bp = Blueprint('fale_conosco_bp', __name__, url_prefix='/api')


@fale_conosco_bp.route('/fale_conosco', methods=['POST'])
@limiter.limit("3 per minute; 10 per hour")
def teste():
    dados = request.get_json()
    
    dados_obrigatorios = ['nome', 'email', 'mensagem']
    if not all(campo in dados for campo in dados_obrigatorios):
        logger.warning(f"Tentativa de envio com campos faltando de {request.remote_addr}: {dados}")
        return jsonify({'error': 'Todos os campos devem estar preenchidos'}),400
   
    
    nome = dados['nome']
    email = dados['email']
    mensagem = dados['mensagem']
    data_cadastro = datetime.datetime.now()
    
    email_valido = validar_email(email)
    if not email_valido:
        logger.warning(f"Tentativa de envio com email inválido de {request.remote_addr}: {email}")
        return jsonify({'error':'Email inválido! Use um formato válido (ex.: usuario@dominio.com)'}),400
    
    
    mensagem_atualizada = validar_msg(mensagem)
    if not mensagem_atualizada:
        logger.warning(f"Mensagem muito longa de {request.remote_addr}")
        return jsonify({'error': 'Mensagem muito longa'}),400
    
    
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute('''INSERT INTO fale_conosco 
                       (nome, email, mensagem,data_cadastro) 
                       VALUES (%s, %s, %s, %s)''',
                       (nome, email, mensagem_atualizada,data_cadastro ))
       
        conn.commit()
        
        logger.info(f"Mensagem registrada com sucesso: {nome}")
        return jsonify({'message': 'Sucesso'})
    except Exception as e:
        logger.error(f"Erro ao inserir na base de dados: {str(e)}")
        return jsonify({'error': f'Erro ao inserir na base de dados: {str(e)}'}), 500

    finally:
        cursor.close()
        conn.close()

    
    

