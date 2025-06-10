from flask import Flask, CORS
from .routes.analytics import analytics_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(analytics_bp, url_prefix="/api/admissions")
    CORS(app,
         supports_credentials=True,
         resources={
             r"/api/*": {"origins": "http://localhost:5173"},
         }
         )
    return app
