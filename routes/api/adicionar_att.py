from flask import Blueprint, jsonify, request, url_for, current_app
import uuid
import requests
import os
from routes.db.conexao import conectar
from routes.utils.logger import logger
from extensions import limiter
from routes.utils.jwt_decoder import token_required


adicionar_att_bp = Blueprint('adicionar_att_bp', __name__, url_prefix='/api')

@adicionar_att_bp.route('/atualizacao', methods=['POST'])
@limiter.limit("10 per minute; 20 per hour")
@token_required
def add_att():
    texto = request.form.get('texto')
    imagem = request.files.get('imagem')
    
    if not texto or not imagem:
        logger.warning(f"Erro, campos de texto e imagem são obrigatorios {request.remote_addr}")
        
        return jsonify({"error": "Texto e imagem são obrigatórios"}), 400
    
    if imagem and imagem.mimetype in ['image/jpeg', 'image/png']:
        upload_folder = os.path.join(current_app.root_path, 'static/uploads_att')
        os.makedirs(upload_folder, exist_ok=True)
        filename = f"{uuid.uuid4()}_{imagem.filename}"
        filepath = os.path.join(upload_folder, filename)
        imagem.save(filepath)
        image_url = url_for('static', filename=f'uploads_att/{filename}')
        
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO atualizacoes (texto, imagem, data_criacao) VALUES (%s, %s, CURRENT_TIMESTAMP) RETURNING id",
                (texto, image_url)
            )
            evento_id = cur.fetchone()[0]
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Erro ao inserir na base de dados: {str(e)}")
            return jsonify({"error": f"Erro ao salvar no banco: {str(e)}"}), 500
        finally:
            cur.close()
            conn.close()
        
        logger.info(f"Mensagem registrada com sucesso:{image_url},{evento_id}")
        return jsonify({"message": "Evento adicionado", 
                        "id": evento_id,
                        "image_url": image_url
                        }), 201
    logger.error(f"Erro, imagem ou formato inválido {imagem.mimetype}")
    return jsonify({"error": "Imagem inválida ou formato não suportado"}), 400





