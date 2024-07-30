import json
import boto3
import uuid
import random
import string
import time
from botocore.exceptions import ClientError

def send_verification_code(email, code):
    ses_client = boto3.client('ses')
    try:
        response = ses_client.send_email(
            Source='your_verified_email@example.com',  # Substitua pelo seu endereço de e-mail verificado no SES
            Destination={
                'ToAddresses': [email]
            },
            Message={
                'Subject': {
                    'Data': 'Seu Código de Verificação'
                },
                'Body': {
                    'Text': {
                        'Data': f'Seu código de verificação é: {code}'
                    }
                }
            }
        )
    except ClientError as e:
        print(f'Erro ao enviar e-mail: {e}')
        return False
    return True

def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    pacientes_table = dynamodb.Table('users')  # Certifique-se de que o nome da tabela está correto
    codigo_table = dynamodb.Table('verificationCodes')  # Certifique-se de que o nome da tabela está correto

    body = json.loads(event.get('body', '{}'))
    cpf = body.get('cpf')

    if not cpf:
        return {
            'statusCode': 400,
            'body': json.dumps('O campo CPF é obrigatório.')
        }

    # Verificar se o CPF existe na tabela de usuários
    response = pacientes_table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('cpf').eq(cpf)
    )
    pacientes = response.get('Items', [])

    if not pacientes:
        return {
            'statusCode': 404,
            'body': json.dumps('Usuário não encontrado.')
        }

    paciente = pacientes[0]
    user_id = paciente.get('id')
    email = paciente.get('email')
    if not email:
        return {
            'statusCode': 400,
            'body': json.dumps('Usuário não possui um e-mail cadastrado.')
        }

    # Gerar código de verificação
    verification_code = generate_verification_code()
    expiration_time = 300  # 5 minutos

    # Salvar o código na tabela de códigos de verificação
    codigo_id = str(uuid.uuid4())
    codigo_table.put_item(
        Item={
            'codigoId': codigo_id,
            'cpf': cpf,
            'codigo': verification_code,
            'ExpirationTime': int(time.time()) + expiration_time,
        }
    )

    # Enviar o código para o e-mail do usuário
    if not send_verification_code(email, verification_code):
        return {
            'statusCode': 500,
            'body': json.dumps('Falha ao enviar o e-mail com o código de verificação.')
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'Código de verificação enviado para o e-mail: {email[:2]}***{email[-2:]}', 'userId': user_id})
    }

