# Usar uma imagem base do Python 3.11
FROM python:3.11-slim

# Instalar zip e outras dependências necessárias
RUN apt-get update && apt-get install -y zip

# Definir o diretório de trabalho no contêiner
WORKDIR /lambda_function

# Copiar os arquivos de código para o contêiner
COPY lambda_function.py .

# Comando para criar o arquivo ZIP da função Lambda
RUN zip -r /lambda_function.zip .

# Copiar o arquivo ZIP para fora do contêiner
CMD ["sh", "-c", "cp /lambda_function.zip /lambda_function/lambda_function.zip"]
