from chatbot.personal_chatbot import FatLossChatBot

def main():
    bot = FatLossChatBot()
    print("🤖 LeHealthBot: Hi! I'm your personalized fat-loss assistant.")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye", "goodbye"]:
            print("Goodbye! Stay healthy and motivated! 💪")
            break
        response = bot.generate_response(user_input)
        print("🤖 LeHealthBot:", response)

if __name__ == "__main__":
    main()