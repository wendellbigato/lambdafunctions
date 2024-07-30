import json
import boto3

client = boto3.client('lambda')

def lambda_handler(event, context):
    print("Entrando na função lambda_handler com o evento: ", json.dumps(event))  # Log inicial para depurar a estrutura do evento

    path = event.get('path')
    http_method = event.get('httpMethod')
    body = event.get('body')

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'
    }

    if not path or not http_method:
        print("Erro: Falta path ou httpMethod no evento")
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps('Bad request: missing path or httpMethod')
        }

    try:
        print(f"Processando a solicitação: path={path}, httpMethod={http_method}")

        # Verifique e encaminhe a solicitação para a função Lambda apropriada
        if path == '/auth' and http_method == 'POST':
            print("Encaminhando para a função authFunction")
            response = client.invoke(
                FunctionName='authFunction',
                InvocationType='RequestResponse',
                Payload=json.dumps(event)
            )
        elif path == '/users' and http_method in ['POST', 'GET', 'PATCH']:
            print(f"Encaminhando para a função usersFunction com evento: {json.dumps(event)}")
            response = client.invoke(
                FunctionName='usersFunction',
                InvocationType='RequestResponse',
                Payload=json.dumps(event)
            )
        elif path == '/token' and http_method == 'POST':
            print("Encaminhando para a função tokenFunction")
            response = client.invoke(
                FunctionName='tokenFunction',
                InvocationType='RequestResponse',
                Payload=json.dumps(event)
            )
        elif path == '/ai' and http_method == 'POST':
            print("Encaminhando para a função aiFunction")
            response = client.invoke(
                FunctionName='aiFunction',
                InvocationType='RequestResponse',
                Payload=json.dumps(event)
            )
        elif path == '/codigo' and http_method == 'POST':
            print("Encaminhando para a função codigoFunction")
            response = client.invoke(
                FunctionName='codigoFunction',
                InvocationType='RequestResponse',
                Payload=json.dumps(event)
            )
        else:
            print("Erro: Rota não suportada")
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps('Rota não suportada')
            }

        print(f"Recebendo resposta da função Lambda chamada: {response}")

        # Processar a resposta da função Lambda chamada
        response_payload = json.loads(response['Payload'].read().decode('utf-8'))
        print(f"Payload da resposta: {response_payload}")

        return {
            'statusCode': response_payload.get('statusCode', 200),
            'headers': headers,
            'body': response_payload.get('body', '')
        }
    except Exception as e:
        print(f"Erro na função API: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(f"Erro interno: {str(e)}")
        }

