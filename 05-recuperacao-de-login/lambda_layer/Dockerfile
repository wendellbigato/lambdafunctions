# Dockerfile para a camada da função Lambda
FROM amazonlinux:2

# Instale Python, pip e zip
RUN yum install -y python3 python3-pip zip

# Crie um diretório para as dependências
RUN mkdir -p /opt/python

# Instale as dependências no diretório da camada
RUN pip3 install requests boto3 -t /opt/python

# Crie o arquivo ZIP da camada
RUN cd /opt && zip -r /opt/lambda_layer.zip python

# Crie o diretório /lambda e copie o arquivo ZIP para lá
RUN mkdir -p /lambda && cp /opt/lambda_layer.zip /lambda/lambda_layer.zip

# Comando final para copiar o arquivo ZIP para o diretório montado
CMD ["cp", "/lambda/lambda_layer.zip", "/mnt/lambda_layer.zip"]

