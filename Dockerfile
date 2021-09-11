FROM python:3
WORKDIR /forwarder-app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "cli.py"]
