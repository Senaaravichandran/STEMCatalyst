from http.server import BaseHTTPRequestHandler
import json
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Parse the URL path
        path = urllib.parse.urlparse(self.path).path
        
        if path == '/' or path == '/health':
            response = {
                'status': 'connected',
                'message': 'API working'
            }
        elif path == '/formulas':
            response = {
                'status': 'success',
                'formulas': [
                    {'category': 'Physics', 'formula': 'F = ma', 'description': 'Newtons Second Law'},
                    {'category': 'Math', 'formula': 'a² + b² = c²', 'description': 'Pythagorean Theorem'},
                    {'category': 'Chemistry', 'formula': 'PV = nRT', 'description': 'Ideal Gas Law'}
                ]
            }
        elif path == '/study-tips':
            response = {
                'status': 'success',
                'tips': [
                    {
                        'category': 'Math',
                        'tip': 'Practice daily for 30 minutes',
                        'description': 'Consistent practice improves problem-solving skills'
                    },
                    {
                        'category': 'Science',
                        'tip': 'Create visual diagrams',
                        'description': 'Visualizing concepts helps with understanding'
                    },
                    {
                        'category': 'General',
                        'tip': 'Explain concepts to others',
                        'description': 'Teaching helps reinforce your own understanding'
                    }
                ]
            }
        else:
            response = {
                'status': 'success',
                'message': f'Endpoint {path} ready'
            }
        
        self.wfile.write(json.dumps(response).encode())
        
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Parse the URL path
        path = urllib.parse.urlparse(self.path).path
        
        # Get POST data
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data.decode()) if post_data else {}
        except:
            data = {}
        
        if path == '/solve':
            problem = data.get('problem', '')
            response = {
                'status': 'success',
                'solution': f'Solution for: {problem}',
                'explanation': 'Your STEM problem has been solved!'
            }
        elif path == '/explain':
            concept = data.get('concept', '')
            response = {
                'status': 'success',
                'explanation': f'Explanation for: {concept}',
                'examples': ['Example 1', 'Example 2'],
                'tips': ['Tip 1', 'Tip 2']
            }
        else:
            response = {
                'status': 'success',
                'message': 'POST request processed'
            }
        
        self.wfile.write(json.dumps(response).encode())
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()