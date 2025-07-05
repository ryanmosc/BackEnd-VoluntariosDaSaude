from routes.utils.logger import logger
from flask import Blueprint, jsonify, request,render_template
from functools import wraps
import jwt
import os
from dotenv import load_dotenv

load_dotenv()




protected_bp = Blueprint('protected_bp', __name__)

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "JWT_SECRET_KEY_KEY")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
    
        token = request.cookies.get('token', None)

       
        if not token:
            auth = request.headers.get('Authorization', '')
            if auth.startswith('Bearer '):
                token = auth.split()[1]

        if not token:
            logger.warning(f"Tentativa de envio sem o token {request.remote_addr}")
            return render_template('index.html')

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = payload
        except jwt.ExpiredSignatureError:
            logger.warning(f"Tentativa de envio com token expirado {request.remote_addr}")
            return render_template('index.html')
        except jwt.InvalidTokenError:
            logger.warning(f"Tentativa de envio com token invalido ou modificado {request.remote_addr}")
            return render_template('index.html')

        return f(*args, **kwargs)
    return decorated


@protected_bp.route('/admin/eventos')
@token_required
def eventos():
    return render_template('formulario_teste_uploads.html')
