# Função Lambda `maritaca-ai`

Esta função Lambda integra-se com a API Maritaca para realizar inferências de conversa, simulando uma interação entre um usuário e um assistente.

## Funcionalidades

- **Integração com a API Maritaca**: Envia mensagens para a API Maritaca e retorna as respostas geradas.
- **Manipulação de Erros**: Lida com erros de requisição e outras exceções, retornando mensagens de erro apropriadas.

## Estrutura do Código

- **get_maritalk_response(request_data, headers)**: Envia uma solicitação POST para a API Maritaca e retorna a resposta JSON.
- **lambda_handler(event, context)**: Função principal que lida com o evento Lambda e coordena o envio das mensagens e a recepção das respostas.

## Como Usar

### Configuração

Antes de usar, configure a URL da API Maritaca e a chave de autorização:

- **URL da API**: Substitua `"https://chat.maritaca.ai/api/chat/inference"` pela URL correta da API Maritaca, se necessário.
- **Chave de API**: Substitua `{sua-chave-api}` pela sua chave de API fornecida pelo Maritaca.

### Estrutura da Requisição

O corpo da requisição enviado para a API Maritaca é composto de:

- **messages**: Lista de mensagens simulando a conversa entre o usuário e o assistente.
- **do_sample**: Booleano indicando se a amostragem deve ser usada.
- **max_tokens**: Número máximo de tokens para a resposta.
- **temperature**: Controla a criatividade da resposta.
- **top_p**: Controla a diversidade da resposta.
- **model**: Modelo de linguagem a ser usado (e.g., "sabia-2-medium").

### Resposta

A resposta contém a orientação ou resposta do assistente, que é retornada ao chamador do Lambda.

## Permissões

Certifique-se de que sua função Lambda tenha permissões para fazer solicitações HTTP externas, se necessário.


