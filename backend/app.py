import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from datetime import datetime
import json
import hashlib
import time

from api.routes import api_bp
from services.ai_service import AIService
from services.data_service import DataService

# Load environment variables
load_dotenv()

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
    app.config['MISTRAL_API_KEY'] = os.getenv('MISTRAL_API_KEY', '3BstpDMkoMclOAZyqdI6lNHQlTLo127I')
    app.config['HUGGINGFACE_TOKEN'] = os.getenv('HUGGINGFACE_TOKEN')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Enable CORS with detailed configuration
    CORS(app, origins=['http://localhost:3000'], 
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization'])
    
    # Add request logging
    @app.before_request
    def log_request_info():
        logger.info(f"Request: {request.method} {request.path}")
        if request.is_json:
            logger.info(f"Request data: {request.get_json()}")
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Initialize services
    app.ai_service = AIService()
    app.data_service = DataService()
    
    # Initialize voice service (with error handling)
    try:
        from services.voice_service import VoiceService
        app.voice_service = VoiceService()
        logger.info("Voice service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize voice service: {e}")
        app.voice_service = None
    
    # Health check endpoints
    @app.route('/health')
    def health_check():
        """Enhanced health check endpoint with performance metrics"""
        start_time = time.time()
        
        services_status = {}
        
        # Check AI service
        try:
            ai_health = app.ai_service.health_check()
            services_status['ai_service'] = {
                "status": "healthy" if ai_health['overall_status'] else "degraded",
                "details": ai_health
            }
        except Exception as e:
            services_status['ai_service'] = {"status": "error", "error": str(e)}
        
        # Check voice service
        if app.voice_service:
            services_status['voice_service'] = {"status": "healthy"}
        else:
            services_status['voice_service'] = {"status": "disabled"}
        
        # Check data service
        try:
            data_health = app.data_service.get_stats()
            services_status['data_service'] = {
                "status": "healthy",
                "stats": data_health
            }
        except Exception as e:
            services_status['data_service'] = {"status": "error", "error": str(e)}
        
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
            "response_time_ms": round(response_time, 2),
            "services": services_status,
            "environment": {
                "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
                "flask_debug": app.config.get('DEBUG', False)
            }
        }), 200
    
    @app.route('/api/health/ai')
    def ai_health_check():
        """AI services health check"""
        try:
            health_status = app.ai_service.health_check()
            return jsonify({
                "status": "healthy" if health_status['overall_status'] else "degraded",
                "services": health_status,
                "timestamp": datetime.now().isoformat()
            }), 200 if health_status['overall_status'] else 503
        except Exception as e:
            logger.error(f"AI health check failed: {str(e)}")
            return jsonify({
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }), 503
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Endpoint not found",
            "message": "The requested resource was not found on this server.",
            "status": 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
            "status": 500
        }), 500
    
    return app
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=app.config['DEBUG']
    )
