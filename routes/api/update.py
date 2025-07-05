from flask import Blueprint, jsonify, request, url_for, current_app
import uuid
import os
import werkzeug
from routes.db.conexao import conectar
from routes.utils.jwt_decoder import token_required
from routes.utils.logger import logger

update_evento_bp = Blueprint('update_evento_bp', __name__, url_prefix='/api')


@update_evento_bp.route('/eventos/<int:id>', methods=['PUT'])
@token_required
def update_evento(id):
    texto = request.form.get('texto')
    imagem = request.files.get('imagem')

    if not texto or texto.strip() == "":
        logger.warning(f"Tentativa de atualização sem texto | IP: {request.remote_addr}")
        return jsonify({"error": "Campo 'texto' é obrigatório"}), 400

    try:
        conn = conectar()
        cur = conn.cursor()

        if imagem:
            
            if imagem.mimetype not in ['image/jpeg', 'image/png']:
                logger.warning(f"Tipo de imagem inválido | IP: {request.remote_addr} | Tipo: {imagem.mimetype}")
                return jsonify({"error": "Apenas imagens JPEG e PNG são permitidas"}), 400

         
            upload_folder = os.path.join(current_app.root_path, 'static/uploads')
            os.makedirs(upload_folder, exist_ok=True)
            filename = f"{uuid.uuid4()}_{werkzeug.utils.secure_filename(imagem.filename)}"
            filepath = os.path.join(upload_folder, filename)
            imagem.save(filepath)

            image_url = url_for('static', filename=f'uploads/{filename}')

            cur.execute(
                "UPDATE eventos SET texto = %s, imagem = %s WHERE id = %s",
                (texto.strip(), image_url, id)
            )
        else:
            cur.execute(
                "UPDATE eventos SET texto = %s WHERE id = %s",
                (texto.strip(), id)
            )

        conn.commit()
        logger.info(f"Evento {id} atualizado com sucesso | IP: {request.remote_addr}")
        return jsonify({"message": "Evento atualizado com sucesso"}), 200

    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao atualizar evento {id} | IP: {request.remote_addr} | Erro: {str(e)}")
        return jsonify({"error": "Erro ao atualizar o evento"}), 500

    finally:
        cur.close()
        conn.close()
