import logging
import functools
import time
from flask import request, jsonify

logger = logging.getLogger(__name__)

def rate_limit(max_requests=100, window=3600):
    """
    Rate limiting decorator
    
    Args:
        max_requests: Maximum number of requests
        window: Time window in seconds
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Simple in-memory rate limiting
            # In production, use Redis or similar
            client_ip = request.remote_addr
            current_time = time.time()
            
            # For now, just log the request
            logger.info(f"API request from {client_ip} to {request.endpoint}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def validate_json_payload(required_fields=None):
    """
    Validate JSON payload decorator
    
    Args:
        required_fields: List of required field names
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Content-Type must be application/json'}), 400
            
            data = request.get_json()
            if not data:
                return jsonify({'error': 'JSON payload is required'}), 400
            
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    return jsonify({
                        'error': f'Missing required fields: {", ".join(missing_fields)}'
                    }), 400
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def log_api_call(func):
    """Log API calls"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info(f"API call started: {request.endpoint}")
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"API call completed: {request.endpoint} in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"API call failed: {request.endpoint} in {duration:.2f}s - {str(e)}")
            raise
    return wrapper
