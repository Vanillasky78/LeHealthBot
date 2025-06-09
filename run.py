from chatbot.personal_chatbot import LeHealthBot

def main():
    bot = LeHealthBot()
    print("🤖 LeHealthBot: Hello! I'm your personalized fat-loss assistant.")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("👋 Goodbye! Stay healthy!")
            break
        response = bot.generate_response(user_input)
        print("🤖 LeHealthBot:", response)

if __name__ == "__main__":
    main()