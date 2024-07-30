FROM amazonlinux:2
RUN yum install -y python3 python3-pip zip && \
    python3 -m pip install bcrypt -t /lambda_function
COPY lambda_function.py /lambda_function/
WORKDIR /lambda_function
CMD zip -r /lambda_function.zip . && cp /lambda_function.zip /mnt/lambda_function.zip

