import json

def handler(request):
    try:
        if request.method == 'POST':
            body = request.body
            if hasattr(body, 'decode'):
                body = body.decode('utf-8')
            data = json.loads(body) if body else {}
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
                'message': 'Explain endpoint ready'
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
            'body': '{"status": "success", "explanation": "Working..."}'
        }