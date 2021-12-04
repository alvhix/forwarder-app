# Telegram Forwarder App

### Description

The forwarder-app is a Python client that forwards messages automatically from a chat to another by using your personal Telegram account.

Every rule allows you to forward from one source to n destinations (one to many)

You can have as many rules as you want or until your machine can take it.

### Setup

This project depends on [TDLib](https://github.com/tdlib/td). TDLib is the official cross-platform library for building Telegram clients written in C++.

##### Basic setup:

1. Setup binaries for TDLib. In the _lib/_ folder there are binaries for Windows and Linux (both AMD64). If you need other binaries, you can build your own following [these instructions](https://tdlib.github.io/td/build.html).

2. Secondly, you need to put your API_ID and API_HASH as an environment variable in your desktop/server (recommended) or put it directly in the .env file. Go to [Telegram page](https://my.telegram.org) to get them.

Example of the .env file:

```
API_ID=1234567
API_HASH=f10123h41l142jl134nngnl143543lep
```

3. Configure the forwarder to fit your needs. The _config.py_ contains the instructions to control the behaviour of the forwarder and the client. On the other side, the forwarder-app.config.yml contains the rules for forwarding (source, destination, options...).

To specify the source and destination of different chats, you can add new rules in the _forwarder-app.config.yml_ file. Example:

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

To execute the script:

1. From the [CLI](docs/cli.md).

2. From [Docker](docs/docker.md) (recommended for serious use).

Once executed for the first time, the app will ask you for authentication. Once you have been authorized, the forwarder will automatically start listening to all chats specified in the forwarder-app.config.yml file for messages to forward.

##### Hosting

The best way to host this application is in a dedicated server as AWS, Google Cloud, Azure...

Warning: The TDLib library stores data in memory throughout the life cycle of the application. It is recommended to restart the application from time to time for prolonged uses.

### Libraries

In the _lib/_ are located the binaries for Windows and Linux. If you need other binaries or you want to build by your own, go to the [TDLib build page](https://tdlib.github.io/td/build.html).

### Logs

All actions and errors from the forwarder-app are logged in _log/app.log_ file. In the other side, TDLib logs are printed directly in the terminal.

### Issues

If you detect a [bug](.github/ISSUE_TEMPLATE/bug_report.md) or you have a [suggestion](.github/ISSUE_TEMPLATE/feature_request.md), open a ticket with the corresponding template.
