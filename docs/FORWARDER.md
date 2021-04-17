# How the forwarder works:

Messages are forwarded in this way:
* Listens to all new messages in your account
* If the message comes from a source that is in the rules file, it stores the message in queue.
* Every second, if the queue is not empty, all messages are forwarded to their corresponding destination. Note that grouped media messages are also forwarded grouped.