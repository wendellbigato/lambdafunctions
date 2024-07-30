# Função Lambda `Login`

## Descrição

A função Lambda `Login` é responsável pela autenticação dos usuários. Ela verifica as credenciais fornecidas (CPF e senha), e se forem válidas, gera e retorna um token JWT para acesso seguro a recursos protegidos.

## Funcionalidades

- **Verificação de Credenciais**: Compara o CPF e a senha fornecidos com os armazenados no DynamoDB.
- **Geração de Token JWT**: Gera um token JWT para o usuário autenticado, com uma expiração de 1 hora.
- **Retorno de Informações do Usuário**: Retorna o ID do usuário juntamente com o token JWT.

## Estrutura do Código

- **lambda_handler(event, context)**: Função principal que lida com as requisições de login. Verifica as credenciais e retorna o token JWT ou uma mensagem de erro.

## Utilização

### Requisição de Login (POST /login)

- **Método**: POST
- **Corpo**: JSON com os seguintes campos obrigatórios: `cpf`, `senha`.

Exemplo:
```json
{
  "cpf": "12345678909",
  "senha": "senhaSegura123"
}
```

### Resposta de Sucesso

- **Status**: 200 OK
- **Corpo**: JSON contendo o token JWT e o ID do usuário.

Exemplo:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": "uuid-do-usuario"
}
```

### Resposta de Falha

- **Status**: 401 Unauthorized
- **Corpo**: JSON contendo a mensagem "Credenciais inválidas".

Exemplo:
```json
{
  "message": "Credenciais inválidas"
}
```

## Segurança e Boas Práticas

- **Hashing de Senha**: As senhas são armazenadas com hashing seguro usando `bcrypt`.
- **Token JWT**: O token JWT é assinado com uma chave secreta e inclui uma expiração para segurança adicional.

## Configuração

- **SECRET_KEY**: Substitua `'your_super_secret_key'` pela sua chave secreta para assinar tokens JWT.
- **ALGORITHM**: Define o algoritmo usado para assinar o JWT, geralmente `HS256`.

## Permissões

Certifique-se de que a função Lambda `Login` tenha permissões adequadas para acessar a tabela DynamoDB onde os dados dos usuários estão armazenados.


