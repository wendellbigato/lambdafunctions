# Função Lambda `Token`

## Descrição

A função Lambda `Token` é responsável por validar tokens JWT fornecidos pelos usuários. Ela verifica a validade do token, incluindo a assinatura e a data de expiração, para autenticar solicitações de acesso a recursos protegidos.

## Funcionalidades

- **Verificação de Token JWT**: Decodifica e valida o token JWT para garantir que seja válido e não tenha expirado.
- **Retorno de Informações do Usuário**: Retorna o ID do usuário extraído do token JWT se a validação for bem-sucedida.

## Estrutura do Código

- **lambda_handler(event, context)**: Função principal que processa o evento de entrada, verifica o token JWT e retorna a resposta adequada com base na validade do token.

## Utilização

### Requisição de Validação de Token (POST /token)

- **Método**: POST
- **Corpo**: JSON contendo o token JWT a ser validado.

Exemplo:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Resposta de Sucesso

- **Status**: 200 OK
- **Corpo**: JSON contendo a mensagem de sucesso e o ID do usuário.

Exemplo:
```json
{
  "message": "Token válido",
  "user_id": "uuid-do-usuario"
}
```

### Resposta de Falha

- **Token Não Fornecido**
  - **Status**: 400 Bad Request
  - **Corpo**: JSON com a mensagem "Token não fornecido".

- **Token Expirado**
  - **Status**: 401 Unauthorized
  - **Corpo**: JSON com a mensagem "Token expirado".

- **Token Inválido**
  - **Status**: 401 Unauthorized
  - **Corpo**: JSON com a mensagem "Token inválido".

## Segurança e Boas Práticas

- **Segredo do JWT**: O segredo (`SECRET_KEY`) deve ser mantido seguro e nunca exposto publicamente.
- **Validação de Expiração**: Tokens expirados são rejeitados para garantir a segurança da sessão.

## Configuração

- **SECRET_KEY**: Substitua `'your_super_secret_key'` pela sua chave secreta para decodificar tokens JWT.
- **ALGORITHM**: Define o algoritmo usado para verificar a assinatura do JWT, geralmente `HS256`.


