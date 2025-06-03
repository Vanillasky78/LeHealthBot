from chatbot.personal_chatbot import FatLossChatBot

def main():
    bot = FatLossChatBot()
    print("🤖 LeHealthBot: 你好，我是你的个性化减脂助手！")

    while True:
        user_input = input("你: ")
        if user_input.lower() in ["quit", "exit"]:
            print("再见，继续加油哦！💪")
            break
        response = bot.generate_response(user_input)
        print("🤖 LeHealthBot:", response)

if __name__ == "__main__":
    main()