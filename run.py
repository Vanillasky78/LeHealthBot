from chatbot.personal_chatbot import LeHealthBot

def main():
    bot = LeHealthBot()
    print("💬 LeHealthBot: Hello! I'm your personalized fat-loss assistant.\n(Type 'exit' anytime to quit.)")

    while True:
        try:
            user_input = input("🧑 You: ").strip()
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("👋 Goodbye! Stay healthy!")
                break

            response = bot.generate_response(user_input)
            print("🤖 LeHealthBot:", response)

        except Exception as e:
            print("⚠️ An error occurred:", str(e))
            continue

if __name__ == "__main__":
    main()
