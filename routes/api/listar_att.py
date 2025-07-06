from flask import Blueprint, jsonify, request, current_app
from routes.db.conexao import conectar
from routes.utils.logger import logger
from extensions import limiter
from routes.utils.jwt_decoder import token_required

listar_att_bp = Blueprint('listar_att_bp', __name__, url_prefix='/api')

@listar_att_bp.route('/atualizacao', methods=['GET'])
@limiter.limit("20 per minute; 100 per hour")
# @token_required
def list_eventos():
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT id, texto, imagem, data_criacao FROM atualizacoes ORDER BY data_criacao DESC")
        eventos = cur.fetchall()
        cur.close()
        conn.close()

        eventos_formatados = []
        for row in eventos:
            eventos_formatados.append({
                "id": row[0],
                "texto": row[1],
                "imagem": row[2],
                "data_criacao": row[3].strftime('%d/%m/%Y %H:%M:%S') if row[3] else None
            })

        logger.info(f"{len(eventos_formatados)} atualizacoes listadas com sucesso | IP: {request.remote_addr}")
        return jsonify(eventos_formatados), 200

    except Exception as e:
        logger.error(f"Erro ao listar eventos | IP: {request.remote_addr} | Erro: {str(e)}")
        return jsonify({"error": f"Erro ao listar atualizacoes: {str(e)}"}), 500
