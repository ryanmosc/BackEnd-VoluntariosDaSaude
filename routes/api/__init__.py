from .fale_conosco import fale_conosco_bp
from .seja_voluntario import seja_voluntario_bp
from .doacao import doacao_bp
from .adicionar_evento import adicionar_evento_bp
from .update import update_evento_bp
from .listar_eventos import listar_eventos_bp
from .deletar_eventos import deletar_evento_bp
from .login import login_bp
from ..utils.jwt_decoder import protected_bp

def init_routes(app):
    app.register_blueprint(fale_conosco_bp)
    app.register_blueprint(seja_voluntario_bp)
    app.register_blueprint(doacao_bp)
    app.register_blueprint(adicionar_evento_bp)
    app.register_blueprint(update_evento_bp)
    app.register_blueprint(listar_eventos_bp)
    app.register_blueprint(deletar_evento_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(protected_bp)
    
