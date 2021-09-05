# Telegram Forwarder App

### Functionalities

##### 1. Forward messages:

Forward messages from a chat to another chat.
The forwarder is prepared to forward from one source to n destinations (one to many)
To specify the source and destination you can add new rules in the _forwarder-app.config.yml_ file. Example (note: this is just an example):

```yaml
forward:
  - id: Rule 1
    source: -1001234567890
    destination:
      - 1234567890
    options: {}
    send_copy: true
    remove_caption: false

  - id: Rule 2
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

The structure of this file is very simple:

- id: Give a unique name to your rule, **make sure that is unique in this file**
- source: Source chat id, only one chat id
- destination: Destination chat ids, can be multiple
- options: Options for the message
  - disable_notification: Disable the push notification
  - from_background: Sent from the background
- send_copy: Send copy or not
- remove_caption: Remove caption

For more information about the options: Go to [TDLib documentation page](https://core.telegram.org/tdlib/docs/classtd_1_1td__api_1_1forward_messages.html#a6c645037c9b1fb40a3cad767f7bf2c15)

### Setup

This project depends on [TDLib](https://github.com/tdlib/td). TDLib is a cross-platform library for building Telegram clients writed in C++.

##### Basic setup:

1. Setup binaries for TDLib. In the _lib/_ folder there are binaries for Windows and Linux (both ARM64). If you need other binaries, you can build your own following [these instructions](https://tdlib.github.io/td/build.html).
2. Secondly, you need to put your API_ID and API_HASH as an environment variable in your desktop/server (recommended) or put it directly in the .env file. Go to [Telegram page](https://my.telegram.org) to get them.
3. Configure the forwarder to fit your needs. The _config.py_ contains the instructions to control the behaviour of the forwarder and the client. On the other side, the forwarder-app.config.yml contains the rules for forwarding (source, destination, options...)

To execute the script:

- Go to the root of the project:

```
python cli.py
```

Once executed and authorized, the forwarder will automatically start listening to all chats specified in the forwarder-app.config.yml file for messages to forward.

To interrupt the execution just press CTRL + C or close the CLI.

##### Hosting

It is recommended to run this app on a server such as Heroku, AWS S3... or on your own Raspberry Pi.

### Libraries

In the _lib/_ are located the binaries for Windows and Linux. If you need other binaries to make it work for your machine, go to the [tdlib build page](https://tdlib.github.io/td/build.html)

### Logs

All actions and errors from the forwarder are logged in _log/app.log_.

### Issues

If you have any problems or questions, open a ticket and I will get back to you as soon as possible.
