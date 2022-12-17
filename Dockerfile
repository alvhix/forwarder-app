FROM python:3.8-alpine
WORKDIR /forwarder-app
RUN apk update && \
    apk upgrade && \
    apk add --update alpine-sdk linux-headers zlib-dev openssl-dev
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "cli.py"]
