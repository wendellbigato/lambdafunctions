import json
import boto3
import jwt
import bcrypt
import datetime
from boto3.dynamodb.conditions import Key

# Configurações de JWT
SECRET_KEY = 'your_super_secret_key'  # Substitua pelo seu segredo
ALGORITHM = 'HS256'

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')  # Certifique-se de que o nome da tabela está correto

def lambda_handler(event, context):
    body = json.loads(event['body'])
    cpf = body['cpf']
    senha = body['senha']
    
    # Verificar credenciais no DynamoDB
    response = table.scan(
        FilterExpression=Key('cpf').eq(cpf)
    )
    
    if response['Items']:
        user = response['Items'][0]
        hashed_password = user['senha']
        
        # Verificar a senha
        if bcrypt.checkpw(senha.encode('utf-8'), hashed_password.encode('utf-8')):
            # Gerar token JWT
            token = jwt.encode({
                'cpf': cpf,
                'user_id': user['id'],  # Adiciona o ID do usuário ao token
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, SECRET_KEY, algorithm=ALGORITHM)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
                },
                'body': json.dumps({
                    'token': token,
                    'user_id': user['id']  # Retorna o ID do usuário separadamente
                })
            }
    
    return {
        'statusCode': 401,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        },
        'body': json.dumps({'message': 'Credenciais inválidas'})
    }

