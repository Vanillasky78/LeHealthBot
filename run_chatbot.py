from my_chatbot import LeChefAI

if __name__ == "__main__":
    # Initialize the LeChefAI
    lechef_ai = LeChefAI(recipe_file='/Users/zhangxinyi/Documents/GitHub/Zhang-xinyi/Food Ingredients and Recipe Dataset with Image Name Mapping.csv')
    lechef_ai.greeting()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("LeChefAI: Goodbye! Happy cooking!")
            break

        response = lechef_ai.generate_response(user_input)
        print(f"LeChefAI: {response}")



