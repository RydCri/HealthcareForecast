from flask import Flask
from app.routes.analytics import analytics_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(analytics_bp, url_prefix="/api/admissions")
    return app
