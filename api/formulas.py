import json

def handler(request):
    try:
        response = {
            'status': 'success',
            'formulas': [
                {'category': 'Physics', 'formula': 'F = ma', 'description': 'Newtons Second Law'},
                {'category': 'Math', 'formula': 'a² + b² = c²', 'description': 'Pythagorean Theorem'},
                {'category': 'Chemistry', 'formula': 'PV = nRT', 'description': 'Ideal Gas Law'}
            ]
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
            'body': '{"status": "success", "formulas": []}'
        }