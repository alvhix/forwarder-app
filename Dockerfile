FROM python:3-slim
WORKDIR /forwarder-app
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install zlib1g-dev libssl-dev gperf php-cli libc++-dev libc++abi-dev -y
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "cli.py"]
