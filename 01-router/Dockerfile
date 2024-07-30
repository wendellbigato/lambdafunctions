FROM amazonlinux:2

# Atualizar e instalar pacotes necessários
RUN yum install -y zip

# Copiar o código da função lambda para o diretório /lambda_function
COPY lambda_function.py /lambda_function/

# Definir o diretório de trabalho
WORKDIR /lambda_function

# Comando para criar um arquivo zip da função lambda e copiá-lo para o diretório /mnt
CMD zip -r /lambda_function.zip . && cp /lambda_function.zip /mnt/lambda_function.zip

