# Docker

1. Pull the docker repository

For AMD64:

```
docker pull alvhix/forwarder-app
```

For ARMv7 (Raspberry PI):

```
docker pull alvhix/forwarder-app:armv7l
```

2. Make a separate folder and inside it:
   - Write your forwarder-app.config.yml file
   - Write your environment variables into the .env file.

Make sure you have read [how the config file works](https://github.com/Alvhix/ForwarderApp/blob/main/README.md)

3. Run the docker container inside the folder you have created:

For AMD64:

```
docker run -v absolute/path/to/forwarder-app.config.yml:/forwarder-app/forwarder-app.config.yml --env-file .env -it alvhix/forwarder-app
```

For ARMv7:

```
docker run -v absolute/path/to/forwarder-app.config.yml:/forwarder-app/forwarder-app.config.yml --env-file .env -it alvhix/forwarder-app:armv7l
```

You are passing your forwarder-app.config.yml file and the .env file to the docker container. You can optional pass the parameter --restart=always to make sure that the container starts on boot. For more info, go to this [page](https://docs.docker.com/config/containers/start-containers-automatically/).

4. Next time you want to run the container, just use this command replacing my_container by the container you just created in the step before:

```
docker start my_container
```

5. (Recommended): If you want to run the app for long periods of time in your server, I recommend you to create a cron job in your Linux machine to avoid an OOM. TDLib caches all data to be that fast, so it can take all your server memory if you have a lot of chats and let the app run for long periods of time. To fix this possible problem, follow this steps:

   - Create a cron job

   ```
   crontab -e
   ```

   - Put this at the bottom of the file, replacing my_container by the name of your container and save it

   ```
   0 0 * * 0 /usr/bin/docker restart my_container
   ```

This will make your docker container restart at 00:00 on every Sunday. For more info, you can check this [page](https://crontab.guru/).

6. To interrupt your docker container, just type

```
docker stop my_container
```
