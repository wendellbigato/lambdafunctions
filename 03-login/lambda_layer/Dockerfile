FROM amazonlinux:2
RUN yum install -y python3.11 python3.11-devel python3-pip zip && \
    pip3 install boto3 PyJWT bcrypt -t /opt/python
RUN cd /opt && zip -r /opt/lambda_layer.zip python
CMD ["cp", "/opt/lambda_layer.zip", "/lambda/lambda_layer.zip"]
