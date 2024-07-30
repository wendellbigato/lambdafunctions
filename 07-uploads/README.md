# Função Lambda de Uploads

Esta função Lambda permite o upload, a geração de URLs pré-assinadas e a exclusão de arquivos em um bucket S3.

## Funcionalidades

- **Upload de Arquivos**: Permite o upload de arquivos para o bucket S3 especificado.
- **Geração de URLs Pré-assinadas**: Gera URLs para acessar os arquivos de forma temporária.
- **Exclusão de Arquivos**: Permite a exclusão de arquivos do bucket S3.

## Estrutura do Código

- **generate_presigned_url(file_name)**: Gera uma URL pré-assinada para acessar o arquivo.
- **lambda_handler(event, context)**: Função principal que lida com as requisições HTTP POST (upload), GET (geração de URL) e DELETE (exclusão de arquivo).

## Como Usar

### Requisições POST

Para fazer o upload de um arquivo:

- **Método**: POST
- **Headers**: `Content-Type: application/octet-stream`, `x-api-key: {sua-chave-api}`
- **Corpo da Requisição**: O conteúdo do arquivo a ser enviado.
- **Parâmetros de Consulta**: `file_name` (nome do arquivo a ser salvo no bucket S3)

### Requisições GET

Para obter uma URL pré-assinada de um arquivo:

- **Método**: GET
- **Parâmetros de Consulta**: `file_name` (nome do arquivo para o qual se deseja gerar a URL)

### Requisições DELETE

Para excluir um arquivo:

- **Método**: DELETE
- **Parâmetros de Consulta**: `file_name` (nome do arquivo a ser excluído)

## Configuração

- **Bucket S3**: Certifique-se de substituir `'your-bucket-name'` pelo nome do seu bucket S3.
- **Permissões AWS**: Garanta que sua função Lambda tenha as permissões necessárias para acessar e modificar o bucket S3.


