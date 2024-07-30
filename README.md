# Portfólio de Aprendizado com AWS e Lambda

Bem-vindo ao meu portfólio de aprendizado, onde compartilho o desenvolvimento e a implementação de várias funções Lambda utilizando a Amazon Web Services (AWS). Este repositório serve como um registro do meu progresso e das habilidades adquiridas na construção de aplicações serverless e no uso de diversos serviços da AWS.

## Introdução

Este projeto começou como uma iniciativa para aprender e explorar o potencial da computação serverless com AWS Lambda. O objetivo era construir uma série de funções Lambda que abordassem diferentes aspectos de uma aplicação web moderna, desde autenticação de usuários até recuperação de senhas, usando tecnologias e práticas recomendadas.

## Arquitetura do Projeto

O sistema é composto por várias funções Lambda, cada uma responsável por um aspecto específico da aplicação. Abaixo estão as principais funções e suas responsabilidades:

- **Login**: Lida com a autenticação dos usuários, verificando credenciais e gerando tokens JWT.
- **Token**: Valida tokens JWT para proteger rotas e recursos da aplicação.
- **Users**: Gerencia o cadastro, consulta e atualização de informações de usuários.
- **Recuperação-Login**: Permite a recuperação de acesso através do envio de códigos de verificação via e-mail.

### Diagramas de Arquitetura

Os diagramas de arquitetura ilustram como as funções Lambda interagem com outros serviços da AWS, como DynamoDB para armazenamento de dados e SES para envio de e-mails.

## Recursos Utilizados

### AWS Lambda

AWS Lambda é o serviço de computação serverless que permite executar código em resposta a eventos e automaticamente gerencia os recursos de computação necessários. Utilizei Lambda para criar funções modulares que realizam tarefas específicas de maneira eficiente e escalável.

### Amazon DynamoDB

DynamoDB é o serviço de banco de dados NoSQL da AWS. Foi usado para armazenar dados de usuários e códigos de verificação, aproveitando suas capacidades de escalabilidade e desempenho.

### Amazon SES (Simple Email Service)

Amazon SES foi utilizado para enviar e-mails de verificação e recuperação de acesso. É um serviço escalável e econômico para enviar e-mails em massa ou transacionais.

### Segurança e Autenticação

O uso de JWT (JSON Web Tokens) garante que somente usuários autenticados possam acessar recursos protegidos da aplicação. Senhas são armazenadas com hashing seguro utilizando bcrypt, seguindo as melhores práticas de segurança.

## Aprendizados

Este projeto proporcionou um profundo entendimento sobre:

- **Computação Serverless**: Criação e gerenciamento de funções Lambda.
- **Gerenciamento de Dados com DynamoDB**: Modelagem de dados NoSQL e operações com AWS SDK.
- **Autenticação e Segurança**: Implementação de autenticação com JWT e proteção de dados sensíveis.
- **Envio de E-mails com Amazon SES**: Configuração e uso para comunicação transacional com usuários.

## Como Usar

### Configuração Inicial

Certifique-se de configurar suas credenciais AWS e ajustar as variáveis de configuração como chaves secretas, nomes de tabelas DynamoDB, e endereços de e-mail para envio.

### Deploy

As funções Lambda e demais recursos podem ser implantados usando o AWS CLI ou o AWS Management Console. Instruções detalhadas de deploy estão disponíveis em cada subdiretório correspondente.

## Contribuições

Embora este repositório seja principalmente um portfólio de aprendizado, contribuições e sugestões são bem-vindas. Sinta-se à vontade para abrir issues ou pull requests com melhorias e correções.


