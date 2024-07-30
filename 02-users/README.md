# Função Lambda `Users`

## Descrição

A função Lambda `Users` é responsável por gerenciar o cadastro, consulta e atualização de informações dos usuários. Ela interage com uma tabela DynamoDB para armazenar e recuperar os dados dos usuários.

## Funcionalidades

- **Cadastro de Usuário (POST)**: Registra um novo usuário no sistema.
- **Consulta de Usuário (GET)**: Recupera informações de um usuário com base em seu ID ou CPF.
- **Atualização de Dados do Usuário (PATCH)**: Atualiza as informações de um usuário existente.

## Estrutura do Código

- **validar_cpf(cpf)**: Valida o CPF informado.
- **cpf_ja_cadastrado(table, cpf, user_id=None)**: Verifica se o CPF já está cadastrado no sistema.
- **normalize_field_names(data)**: Normaliza os nomes dos campos para o padrão do sistema.
- **denormalize_field_names(data)**: Desnormaliza os nomes dos campos para a resposta.
- **lambda_handler(event, context)**: Função principal que lida com as requisições e distribui para as operações corretas (POST, GET, PATCH).

## Utilização

### Cadastro de Usuário (POST /users)

- **Método**: POST
- **Corpo**: JSON com os seguintes campos obrigatórios: `nome`, `email`, `cpf`, `senha`, `dataNascimento`.

Exemplo:
```json
{
  "nome": "João da Silva",
  "email": "joao.silva@example.com",
  "cpf": "12345678909",
  "senha": "senhaSegura123",
  "dataNascimento": "1990-01-01",
  "telefone": "11987654321"
}
```

### Consulta de Usuário (GET /users)

- **Método**: GET
- **Parâmetros de Consulta**: `id` para buscar por ID ou `cpf` para buscar por CPF.

Exemplo:
```json
{
  "id": "uuid-do-usuario"
}
```

### Atualização de Dados do Usuário (PATCH /users)

- **Método**: PATCH
- **Parâmetros de Consulta**: `id` do usuário a ser atualizado.
- **Corpo**: JSON com os campos a serem atualizados.

Exemplo:
```json
{
  "email": "novo.email@example.com",
  "telefone": "1122334455"
}
```

## Segurança e Boas Práticas

- **Validação de CPF**: Inclui verificação para garantir que o CPF seja válido e único no sistema.
- **Hashing de Senha**: As senhas são armazenadas utilizando hashing seguro com `bcrypt`.

## Permissões

Certifique-se de que a função Lambda `Users` tenha permissões adequadas para acessar a tabela DynamoDB.

