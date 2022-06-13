# Telegram Forwarder App

## Description

forwarder-app is a Python client that forwards messages automatically from a chat to another by using your Telegram account.

Every rule allows you to forward from one source to n destinations (one to many)

You can have as many rules as you want or until your machine can take it.

## Setup

This project depends on [TDLib](https://github.com/tdlib/td). TDLib is the official cross-platform library for building Telegram clients written in C++.
Also, it depends on [pywtdlib](https://github.com/alvhix/pywtdlib) which is a synchronous python Telegram wrapper for TDLib.

### How to use it:

1. Pull the docker repository

   ```
   docker pull alvhix/forwarder-app
   ```

2. Make a separate folder and inside it:

   - Write your API_ID and API_HASH into the `.env` file.
     Go to [Telegram page](https://my.telegram.org) to get your API_ID and API_HASH, example:

     ```
     API_ID=1234567
     API_HASH=f10123h41l142jl134nngnl143543lep
     ```

   - Write your `forwarder-app.config.yml` file:
     To specify the source and destination of different chats, you may add new rules in the _forwarder-app.config.yml_ file. Example:

     ```yaml
     forward:
       - id: 'Rule 1'
         source: -1001234567890
         destination:
           - 1234567890
         options: {}
         send_copy: true
         remove_caption: false

       - id: 'Rule 2'
         source: -1000987654321
         destination:
           - 1234567890
           - -1001234567890
         options:
           disable_notification: true
           from_background: true
         send_copy: false
         remove_caption: true
     ```

     The structure of this file is very simple. Every rule has:

     - id: Give a unique name to your rule, **make sure that is unique in this file**
     - source: Source chat id, only one chat id
     - destination: Destination chat ids, can be multiple
     - options: Options for the message
       - disable_notification: Disable the push notification
       - from_background: Sent from the background
     - send_copy: Send copy or not
     - remove_caption: Remove caption

     For more information about the options: Go to [TDLib documentation page](https://core.telegram.org/tdlib/docs/classtd_1_1td__api_1_1forward_messages.html#a6c645037c9b1fb40a3cad767f7bf2c15)

3. Run the docker container inside the folder you have created:

   ```
   docker run \
   -v "$(pwd)/forwarder-app.config.yml:/forwarder-app/forwarder-app.config.yml" \
   --env-file .env \
   -it alvhix/forwarder-app:armv7l
   ```

- -v Bind your forwarder-app.config.yml with the one on the docker container
- --env-file Send your environment variables with your API_ID and API_HASH to the docker container
- it Execute the container in interactive mode so you can put your credentials

Optional: You can pass the parameter --restart=always to make sure that the container starts on boot. For more info, go to this [page](https://docs.docker.com/config/containers/start-containers-automatically/).

This will execute the docker container and it will ask you for your Telegram account phone number and a code that you will receive. To stop the session in your Telegram account, just go to Telegram app > Settings > Privacy and security > Devices > Active sessions (just delete here the pywtdlib app)

4. Next time you want to run the container, just use this command replacing my_container by the container you just created in the step before:

   ```
   docker start my_container
   ```

5. (Recommended): If you want to run the app for long periods of time in your server, I recommend you to create a cron job in your Linux machine to avoid an OOM. TDLib caches all data to be that fast, if you have a lot of chats and let the app run for long periods of time it can take all your server memory. To fix this possible problem, follow this steps:

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

### Configuration:

Configure the forwarder to fit your needs. The _config.py_ contains the instructions to control the behaviour of the forwarder and the client.

```python
FORWARDER = {
    "api_id": environ["API_ID"], # don't touch this
    "api_hash": environ["API_HASH"], # don't touch this
    "rules_path": path.join(_dirname, "forwarder-app.config.yml"), # you can specify other path to your rules file
    "group_messages": False,  # True to group media messages before forwarding, (it may take $(periodicity_fwd) second/s to forward)
    "periodicity_fwd": 1,  # second/s (not used if $(group_messages) is false)
    "verbosity": 1,
}
```

### Hosting

The best way to host this application is in a dedicated server as AWS, Google Cloud, Azure...

Warning: The TDLib library stores data in memory throughout the life cycle of the application. It is recommended to restart the application from time to time for prolonged uses.

## Logs

All actions and errors from the forwarder-app are logged in _log/app.log_ file. In the other side, TDLib logs are printed directly in the terminal.
To see your logs execute this with your docker container id: `docker exec my_container tail log/app.log`
Errors are registered by TDLib in console, to see the printed errors to console: `docker logs my_container`

## Issues

If you detect a [bug](.github/ISSUE_TEMPLATE/bug_report.md) or you have a [suggestion](.github/ISSUE_TEMPLATE/feature_request.md), open a ticket with the corresponding template.
