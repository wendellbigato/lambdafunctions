import json
import jwt

# Configurações de JWT
SECRET_KEY = "your_super_secret_key"  # Substitua pelo seu segredo
ALGORITHM = "HS256"

def lambda_handler(event, context):
    print("Evento recebido: ", json.dumps(event))
    body = json.loads(event["body"])
    token = body.get("token")
    
    if not token:
        print("Token não fornecido")
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            },
            "body": json.dumps({"message": "Token não fornecido"})
        }
    
    try:
        # Decodificar e verificar o token JWT
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = decoded_token['user_id']  # Extrair o ID do usuário do token
        print("Token válido. User ID: ", user_id)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            },
            "body": json.dumps({"message": "Token válido", "user_id": user_id})
        }
    except jwt.ExpiredSignatureError:
        print("Token expirado")
        return {
            "statusCode": 401,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            },
            "body": json.dumps({"message": "Token expirado"})
        }
    except jwt.InvalidTokenError:
        print("Token inválido")
        return {
            "statusCode": 401,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            },
            "body": json.dumps({"message": "Token inválido"})
        }

