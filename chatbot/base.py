class ChatbotBase:
    def generate_response(self, user_input: str) -> str:
        raise NotImplementedError("Subclasses should implement this method.")