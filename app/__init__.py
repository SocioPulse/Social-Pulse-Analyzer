from flask import Flask
from api.routes import social_pulse
from config.settings import settings

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(social_pulse, url_prefix='/api')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 