# Função Lambda `Router`

## Descrição

A função Lambda `Router` atua como um roteador, encaminhando solicitações HTTP para outras funções Lambda com base no caminho (`path`) e no método HTTP (`httpMethod`) da solicitação. Isso facilita a separação de lógica e a organização de diferentes funcionalidades no sistema.

## Funcionalidades

- **Encaminhamento de Solicitações**: Redireciona as solicitações para funções Lambda apropriadas como `authFunction`, `usersFunction`, `tokenFunction`, `aiFunction`, e `codigoFunction`.
- **Verificação de Caminho e Método HTTP**: Verifica o caminho da URL e o método HTTP para determinar a função de destino.
- **Logs para Depuração**: Gera logs detalhados para ajudar na depuração e no monitoramento.

## Estrutura do Código

- **lambda_handler(event, context)**: Função principal que recebe o evento, verifica o caminho e o método HTTP, e encaminha a solicitação para a função Lambda correspondente.

## Utilização

### Roteamento

A função `Router` roteia as solicitações para diferentes funções Lambda com base nos seguintes caminhos e métodos:

- **/auth** (POST): Encaminha para `authFunction`.
- **/users** (POST, GET, PATCH): Encaminha para `usersFunction`.
- **/token** (POST): Encaminha para `tokenFunction`.
- **/ai** (POST): Encaminha para `aiFunction`.
- **/codigo** (POST): Encaminha para `codigoFunction`.

### Exemplo de Solicitação

#### Autenticação (POST /auth)
```json
{
  "httpMethod": "POST",
  "path": "/auth",
  "body": "{...}" // JSON com as credenciais do usuário
}
```

#### Cadastro de Usuários (POST /users)
```json
{
  "httpMethod": "POST",
  "path": "/users",
  "body": "{...}" // JSON com os dados do usuário
}
```

### Resposta

A resposta da função `Router` será baseada na resposta recebida da função Lambda de destino, incluindo o código de status e o corpo da resposta.

## Permissões

Certifique-se de que a função `Router` tenha permissões para invocar outras funções Lambda dentro do mesmo projeto.

