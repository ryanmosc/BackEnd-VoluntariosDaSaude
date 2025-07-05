from flask import Blueprint, jsonify, request, current_app
import os
from routes.db.conexao import conectar
from routes.utils.logger import logger
from extensions import limiter
from routes.utils.jwt_decoder import token_required


deletar_evento_bp = Blueprint('deletar_evento_bp', __name__, url_prefix='/api')

@deletar_evento_bp.route('/eventos/<int:id>', methods=['DELETE'])
@limiter.limit("10 per minute; 20 per hour")
@token_required
def delete_evento(id):
    try:
        conn = conectar()
        cur = conn.cursor()


        cur.execute("SELECT imagem FROM eventos WHERE id = %s", (id,))
        resultado = cur.fetchone()
        if not resultado:
            logger.warning(f"Tentativa de deletar evento inexistente | ID: {id} | IP: {request.remote_addr}")
            cur.close()
            conn.close()
            return jsonify({"error": "Evento não encontrado"}), 404

        image_url = resultado[0]
        image_path = os.path.join(current_app.root_path, 'static', 'uploads', os.path.basename(image_url))

        
        cur.execute("DELETE FROM eventos WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()

     
        if os.path.exists(image_path):
            os.remove(image_path)
            logger.info(f"Imagem removida com sucesso | Caminho: {image_path}")
        else:
            logger.warning(f"Imagem não encontrada para deletar | Caminho: {image_path}")

        logger.info(f"Evento deletado com sucesso | ID: {id}")
        return jsonify({"message": "Evento deletado"}), 200

    except Exception as e:
        logger.error(f"Erro ao deletar evento | ID: {id} | Erro: {str(e)}")
        try:
            conn.rollback()
        except:
            pass
        return jsonify({"error": f"Erro ao deletar evento: {str(e)}"}), 500
