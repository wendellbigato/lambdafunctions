# Dockerfile para a função Lambda `budbemCodigo`
FROM amazonlinux:2

# Instale Python, pip e zip
RUN yum install -y python3 python3-pip zip

# Crie um diretório para a função lambda
RUN mkdir -p /lambda_function

# Copie o código da função lambda para o diretório
COPY lambda_function.py /lambda_function/

# Defina o diretório de trabalho
WORKDIR /lambda_function

# Crie o arquivo ZIP da função lambda
RUN zip -r lambda_function.zip .

# Comando final para copiar o arquivo ZIP para o diretório montado
CMD ["cp", "lambda_function.zip", "/mnt/lambda_function.zip"]

