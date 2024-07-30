# Função Lambda `Recuperação-Login`

## Descrição

A função Lambda `Recuperação-Login` é usada para recuperar o acesso ao sistema através do envio de um código de verificação para o e-mail registrado do usuário. Este código é necessário para autenticação e redefinição de senha.

## Funcionalidades

- **Verificação de CPF**: Confirma se o CPF fornecido está registrado no sistema.
- **Geração de Código de Verificação**: Gera um código de verificação de 6 dígitos.
- **Envio de E-mail**: Envia o código de verificação para o e-mail registrado do usuário.
- **Armazenamento do Código**: Armazena o código de verificação e o CPF do usuário na tabela de códigos de verificação com um tempo de expiração.

## Estrutura do Código

- **send_verification_code(email, code)**: Envia o código de verificação para o e-mail do usuário usando o Amazon SES.
- **generate_verification_code()**: Gera um código de verificação aleatório de 6 dígitos.
- **lambda_handler(event, context)**: Função principal que processa a solicitação, verifica o CPF, gera o código, e envia o e-mail.

## Utilização

### Requisição para Recuperação de Login (POST /recuperacao-login)

- **Método**: POST
- **Corpo**: JSON contendo o CPF do usuário.

Exemplo:
```json
{
  "cpf": "12345678909"
}
```

### Resposta de Sucesso

- **Status**: 200 OK
- **Corpo**: JSON indicando que o código foi enviado com sucesso.

Exemplo:
```json
{
  "message": "Código de verificação enviado para o e-mail: jo***@example.com",
  "userId": "uuid-do-usuario"
}
```

### Resposta de Falha

- **CPF Não Fornecido**
  - **Status**: 400 Bad Request
  - **Corpo**: JSON com a mensagem "O campo CPF é obrigatório."

- **Usuário Não Encontrado**
  - **Status**: 404 Not Found
  - **Corpo**: JSON com a mensagem "Usuário não encontrado."

- **Erro ao Enviar E-mail**
  - **Status**: 500 Internal Server Error
  - **Corpo**: JSON com a mensagem "Falha ao enviar o e-mail com o código de verificação."

## Configuração

- **E-mail de Origem**: Substitua `'your_verified_email@example.com'` pelo seu e-mail verificado no Amazon SES para envio de mensagens.
- **Tabela DynamoDB**: Certifique-se de que os nomes das tabelas DynamoDB (`users` e `verificationCodes`) estão corretos e configurados.

## Segurança e Boas Práticas

- **Uso de UUIDs**: Utiliza UUIDs para identificar de forma única os registros de códigos de verificação.
- **Tempo de Expiração**: O código de verificação é válido por 5 minutos, aumentando a segurança.


