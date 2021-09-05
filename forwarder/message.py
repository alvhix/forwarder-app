class Message:
    def __init__(self, update, rule) -> None:
        self.message_id = [update["id"]]
        self.source_id = update["chat_id"]
        self.destination_ids = rule["destination"]
        self.date = update["date"]
        self.message_type = update["content"]["@type"]
        self.content = update["content"]

        # options forwarding
        self.rule_id = rule["id"]
        self.options = rule["options"]
        self.send_copy = rule["send_copy"]
        self.remove_caption = rule["remove_caption"]

    def __str__(self) -> str:
        return (
            "{"
            + f"message_id: {self.message_id}, source_id: {self.source_id}, destination_id: {self.destination_ids}, date: {self.date}, message_type: {self.message_type}, rule_id: {self.rule_id}"
            + "}"
        )

    def __hash__(self) -> int:
        return hash(self.__str__())
