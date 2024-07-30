import json
import boto3
import base64

s3_client = boto3.client('s3')
BUCKET_NAME = 'your-bucket-name'  # Substitua pelo nome do seu bucket S3

def generate_presigned_url(file_name):
    return s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': file_name},
        ExpiresIn=604800  # URL válida por 1 semana
    )

def lambda_handler(event, context):
    try:
        if event['httpMethod'] == 'POST':
            # Lida com upload de arquivo
            print("Received event:", json.dumps(event))
            if event.get('isBase64Encoded', False):
                body = base64.b64decode(event['body'])
            else:
                body = event['body'].encode('utf-8')
            content_type = event['headers'].get('Content-Type', 'application/octet-stream')
            key = event['queryStringParameters']['file_name']
            response = s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=key,
                Body=body,
                ContentType=content_type
            )
            presigned_url = generate_presigned_url(key)
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type, x-api-key',
                    'Access-Control-Allow-Methods': 'POST'
                },
                'body': json.dumps({'message': 'Arquivo enviado com sucesso', 'file_url': presigned_url})
            }

        elif event['httpMethod'] == 'GET':
            # Gera URL pré-assinada
            key = event['queryStringParameters']['file_name']
            presigned_url = generate_presigned_url(key)
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type, x-api-key',
                    'Access-Control-Allow-Methods': 'GET'
                },
                'body': json.dumps({'file_url': presigned_url})
            }

        elif event['httpMethod'] == 'DELETE':
            # Lida com a exclusão de arquivo
            key = event['queryStringParameters']['file_name']
            response = s3_client.delete_object(
                Bucket=BUCKET_NAME,
                Key=key
            )
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type, x-api-key',
                    'Access-Control-Allow-Methods': 'DELETE'
                },
                'body': json.dumps({'message': 'Arquivo excluído com sucesso'})
            }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type, x-api-key',
                'Access-Control-Allow-Methods': 'POST, GET, DELETE'
            },
            'body': json.dumps({'message': 'Falha na requisição', 'error': str(e)})
        }

