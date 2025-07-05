from flask import Flask,render_template
from routes.api import init_routes
from extensions import limiter
from routes.utils.logger import start_bot
from threading import Thread






def create_app():
    app = Flask(__name__)
    limiter.init_app(app)
    Thread(target=start_bot, daemon=True).start()
    
    
    
    @app.route('/')
    def index():
        return render_template('index.html')
       
    @app.route('/sobre-nos')
    def sobre_nos():
        return render_template('sobreNos.html')

    @app.route('/transparencia')
    def transparencia():
        return render_template('transparencia.html')

    @app.route('/fale-conosco')
    def fale_conosco():
        return render_template('fale_conosco.html')

    @app.route('/seja-voluntario')
    def seja_voluntario():
        return render_template('seja_voluntario.html')

    @app.route('/doacao')
    def doacao():
        return render_template('doacao.html')
    
    @app.route('/login')
    def login():
        return render_template('login.html')
    
    

    
    
    init_routes(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
