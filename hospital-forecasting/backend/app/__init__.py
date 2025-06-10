from flask import Flask
from flask_cors import CORS
from .routes.analytics import analytics_bp


def create_app():
    app = Flask(__name__)
    CORS(app,
         supports_credentials=True,
         resources={
             r"/api/*": {"origins": "http://localhost:5173"},
         }
         )
    app.register_blueprint(analytics_bp, url_prefix="/api/admissions")
    return app
