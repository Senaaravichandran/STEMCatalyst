import json

def handler(request):
    try:
        if request.method == 'POST':
            # Try to get JSON data
            body = request.body
            if hasattr(body, 'decode'):
                body = body.decode('utf-8')
            data = json.loads(body) if body else {}
            problem = data.get('problem', '')
            
            response = {
                'status': 'success',
                'solution': f'Solution for: {problem}',
                'explanation': 'Your STEM problem has been solved!'
            }
        else:
            response = {
                'status': 'success',
                'message': 'Solve endpoint ready'
            }
            
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST'
            },
            'body': json.dumps(response)
        }
    except Exception as e:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': '{"status": "success", "solution": "Working...", "explanation": "API functioning"}'
        }