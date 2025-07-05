from flask import Blueprint, jsonify, request
from extensions import limiter
from routes.utils.logger import logger
from routes.db.conexao import conectar
from funcoes.validar_telefone import validar_telefone_final
from funcoes.validar_email import validar_email
from funcoes.validar_mensagem import validar_msg
import datetime

doacao_bp = Blueprint('doacao_bp', __name__, url_prefix='/api')

@doacao_bp.route('/doacao', methods=['POST'])
@limiter.limit("3 per minute; 10 per hour")
def teste():
    dados = request.get_json()
    
    dados_obrigatorios = ['nome_completo', 'email', 'telefone', 'cpf', 'endereco'  ]

    if not all(campo in dados for campo in dados_obrigatorios):
        logger.warning(f"Tentativa de envio com campos faltando de {request.remote_addr}: {dados}")
        return jsonify({'error': 'Todos os campos devem estar presentes'}), 400

   
    
    nome = dados['nome_completo']
    email = dados['email']
    telefone = dados['telefone']
    cpf = dados['cpf']
    endereco  = dados['endereco' ]
    data_cadastro = datetime.datetime.now()
    
    email_valido = validar_email(email)
    if not email_valido:
        logger.warning(f"Tentativa de envio com email inválido de {request.remote_addr}: {email}")
        return jsonify({'error':'Email inválido! Use um formato válido (ex.: usuario@dominio.com)'}),400
    
    telefone_atualizado = validar_telefone_final(telefone)
    if not telefone_atualizado:
        logger.warning(f"Tentativa de envio com telefone inválido de {request.remote_addr}: {telefone}")
        return jsonify({'error': 'Digite um número de telefone válido'}), 400
    
    
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute('''INSERT INTO doacao 
                       (nome_completo, email, telefone, cpf, endereco, data_cadastro) 
                       VALUES (%s, %s, %s, %s, %s, %s)''',
                       (nome, email, telefone_atualizado, cpf, endereco, data_cadastro ))
       
        conn.commit()
        
        logger.info(f"Mensagem registrada com sucesso: {cpf}")
        return jsonify({'message': 'Sucesso'})
    except Exception as e:
        logger.error(f"Erro ao inserir na base de dados: {str(e)}")
        return jsonify({'error': f'Erro ao inserir na base de dados: {str(e)}'}), 500

    finally:
        cursor.close()
        conn.close()

    
    

