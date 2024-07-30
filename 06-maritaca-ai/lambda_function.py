import json
import requests

def get_maritalk_response(request_data, headers):
    url = "https://chat.maritaca.ai/api/chat/inference"  # Substitua pela URL da API do Maritaka
    
    response = requests.post(
        url,
        json=request_data,
        headers=headers
    )

    if not response.ok:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
    return response.json()

def lambda_handler(event, context):
    try:
        messages = [
            {"role": "user", "content": "bom dia, esta é a mensagem do usuario"},
            {"role": "assistant", "content": "bom dia, esta é a resposta do assistente"},
            {"role": "user", "content": "Você pode me falar quanto é 25 + 27?"}
        ]

        request_data = {
            "messages": messages,
            "do_sample": True,
            'max_tokens': 200,
            "temperature": 0.7,
            "top_p": 0.95,
            "model": "sabia-2-medium"
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Key {sua chave}"  # Substitua pela sua chave de API
        }

        response = get_maritalk_response(request_data, headers)
        guidance = response.get("answer", "Sem resposta")

        return {
            'statusCode': 200,
            'body': json.dumps({"guidance": guidance})
        }
    
    except requests.exceptions.RequestException as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"error": f"Request failed: {str(e)}"})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }

