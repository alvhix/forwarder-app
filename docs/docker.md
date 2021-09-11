# Docker

1. Pull the docker repository

2. Make a separate folder and inside it:
   - Write your forwarder-app.config.yml file
   - Write your environment variables into the .env file.

Make sure you have read [how the config file works](https://github.com/Alvhix/ForwarderApp/blob/main/README.md)

3. Run the docker container with the following line:

```
docker run -v absolute/path/to/forwarder-app.config.yml:/forwarder-app/forwarder-app.config.yml --env-file .env -it alvhix/forwarder-app
```

You are passing your forwarder-app.config.yml file with the rules and the .env file to the docker container.
