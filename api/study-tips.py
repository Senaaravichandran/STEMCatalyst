import json

def handler(request):
    try:
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
            'body': '{"status": "success", "tips": []}'
        }