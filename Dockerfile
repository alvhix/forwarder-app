FROM python:alpine
WORKDIR /forwarder-app
RUN apk update && \
    apk upgrade && \
    apk add --update alpine-sdk linux-headers git zlib-dev openssl-dev gperf php cmake
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "cli.py"]
