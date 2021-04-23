# Telegram Forwarder App

### Functionalities 

##### 1. Forward messages: 
Forward messages from a chat to another chat. If you want to know how it works, go to [docs/forward.md](docs/forward.md).
To specify the source and destination you can add new rules in the *rules.json* file. Example (note: this is just an example):
```json
{
  "forward": [
    {
      "id": "Rule 1",
      "from_chat": -1003672971871,
      "to_chat": -1001393359729,
      "options": {},
      "send_copy": true,
      "remove_caption": false
    }
  ]
}
```
The structure is very simple:
* id: Give a unique name to your rule, **make sure that is unique in this file** (Text)
* from: Source chat id (Number)
* to: Destination chat id (Number)
* options: Options for the message (Array)
* send_copy: Send copy or not (Boolean)
* remove_caption: Remove caption (Boolean)

For more information: Go to [TDLib documentation page](https://core.telegram.org/tdlib/docs/classtd_1_1td__api_1_1forward_messages.html#a6c645037c9b1fb40a3cad767f7bf2c15)

##### 2. Get main chat list: 
Get main chat list of the user. Before anything, you need to know the ids of the groups that you want to add in the *rules.json* file. This will allows you to see all information about all chats you have in the *log/output_log.json* file. You can filter the chat you are interested in by name. If you can't find your chat, you can change in the *config.py* file, the value of LIMIT_CHATS (be careful, if you put a larger number of chats than you have, you will get an error).

##### 3. Get chat by id
Get chat info by its id.

##### 4. Listen requests/updates: 
Listen all events and writes it to a file. This feature is only for testing purposes.

### Setup
This project depends on [TDLib](https://github.com/tdlib/td).

First of all, open the *config.py* file to adjust the parameters of the application:
1. You need to get the dll/so files and put it in the lib/ folder, then you need to put the path in the lib variable. You can see more info about how to get these files [here](https://tdlib.github.io/td/build.html).
2. You need to put your API_ID and API_HASH as an environment variable (recommended) or directly in the file. Go to [your Telegram page](https://my.telegram.org).

There are two ways to execute the script:
* Running the module normally:
```
python -m forwarder
```
Once executed, command options will appear to start an action.

* Passing an additional argument:
```
python -m forwarder fwd
```
List of possible arguments are:
* fwd - Starts listening to new messages for forwarding
* l - Listen all updates/requests (for testing)

To interrupt the execution just press CTRL + C.

### Libraries
In the *lib/* folder is where you should put the library files necessary to use TDLib.

### Logs
This app logs all activities in different files located in *log/* folder:
* All actions and errors from the forwarder are logged in *log/app.log*.
* Output from get main chat list, get chat and listen features are logged in *log/events.json*.

### Issues
If you have any issue or question, please open a ticket and I will answer you as soon as possible.
