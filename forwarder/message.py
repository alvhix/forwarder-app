class Message:
    def __init__(self, message_id, chat_id, date, rule_id) -> None:
        self.message_id = message_id
        self.chat_id = chat_id
        self.date = date
        self.rule_id = rule_id

    def __str__(self) -> str:
        return (
            "{"
            + f"message_id: {self.message_id}, chat_id: {self.chat_id}, date: {self.date}, rule_id: {self.rule_id}"
            + "}"
        )
