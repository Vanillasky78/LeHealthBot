class ChatbotBase:
    def generate_response(self, user_input: str) -> str:
        raise NotImplementedError("This method should be overridden by subclasses")