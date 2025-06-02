import pandas as pd
import re
import random
import warnings
import logging
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from chatbot_base import ChatbotBase  # Importing the base class

# Suppress Hugging Face warnings
warnings.filterwarnings('ignore', category=UserWarning, message=".*Setting pad_token_id to eos_token_id.*")

# Set log level to ERROR to suppress other informational logs
logging.getLogger('transformers').setLevel(logging.ERROR)

# Suppress Tokenizer parallelism warning
os.environ['TOKENIZERS_PARALLELISM'] = 'False'

# Define the chatbot class
class InstructLLMChatbot(ChatbotBase):
    def __init__(self, name="LeChefAI", device='cpu'):
        super().__init__(name)
        self.device = device

        # Set hyperparameters for text generation
        self.max_tokens = 100
        self.temperature = 0.3
        self.top_p = 0.99
        self.min_p = 0.1

        # System prompt
        self.system_prompt = {
            "role": "system",
            "content": "You are a friendly chatbot that answers questions in short sentences.",
        }

        # Model checkpoint
        checkpoint = "HuggingFaceTB/SmolLM-135M-Instruct"

        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        self.model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)

        # Explicitly set pad_token_id and eos_token_id to avoid warnings
        self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        self.model.config.pad_token_id = self.tokenizer.eos_token_id

    def process_input(self, user_input):
        return user_input.strip()

    def greeting(self):
        super().greeting()  # Call base class greeting
        print("I can help you find healthy recipes based on the ingredients you have on hand.")
        print("You can ask me for meal ideas, seasonal ingredients, cooking tips, or recipes based on a specific ingredient!")
        print("\nFor example, you can say:")
        print(" - 'Seasonal ingredients for fall'")
        print(" - 'Give me meal ideas with chicken'")
        print(" - 'Give me cooking tips'")
        print(" - 'Recipes for apple'")

    def farewell(self):
        responses = ['Goodbye', 'Have a nice day', 'See you later!', 'Take care, bye!']
        print(random.choice(responses))
        super().farewell()  # Call base class farewell

    def prepare_instruct_str(self, processed_input):
        user_prompt = {
            "role": "user",
            "content": processed_input
        }
        messages = [self.system_prompt, user_prompt]
        input_str = self.tokenizer.apply_chat_template(messages, tokenize=False)
        return input_str

    def respond_with_LLM(self, processed_input):
        input_str = self.prepare_instruct_str(processed_input)
        input_tokens = self.tokenizer.encode(input_str, return_tensors="pt").to(self.device)
        input_token_len = input_tokens.shape[-1]

        output = self.model.generate(input_tokens, max_new_tokens=self.max_tokens, temperature=self.temperature, top_p=self.top_p, min_p=self.min_p, do_sample=True)
        out_str = self.tokenizer.decode(output[0][input_token_len:])
        out_str = re.sub(r'(<\|im_start\|>assistant\n)|(<\|im_end\|>)', '', out_str)
        return out_str

    def generate_response(self, processed_input):
        bye_regex = r'^(bye|goodbye|end|exit|quit)$'
        if re.search(bye_regex, processed_input.lower()):
            return self.farewell()
        else:
            return self.respond_with_LLM(processed_input)


# Define LeChefAI class
class LeChefAI(InstructLLMChatbot):
    def __init__(self, name="LeChefAI", device='cpu', recipe_file='/Users/zhangxinyi/Documents/GitHub/Zhang-xinyi/Food Ingredients and Recipe Dataset with Image Name Mapping.csv'):
        super().__init__(name, device)
        self.recipes_data = self.load_recipes_data(recipe_file)
        self.preprocess_recipes()

    def load_recipes_data(self, file_path):
        """Load recipe data"""
        try:
            df = pd.read_csv(file_path)
            print(f"Recipe data loaded successfully from {file_path}")
            print("Data columns:", df.columns)  # Print column names to confirm
            return df
        except Exception as e:
            print(f"Failed to load data: {e}")
            return None

    def preprocess_recipes(self):
        """Preprocess recipe data"""
        if self.recipes_data is not None:
            self.recipes_data['Cleaned_Ingredients'] = self.recipes_data['Cleaned_Ingredients'].apply(lambda x: x.lower() if isinstance(x, str) else '')
        else:
            print("No recipe data available for processing.")

    def suggest_recipe(self, user_ingredients):
        """Suggest recipes based on the ingredients the user provides"""
        matched_recipes = []
        user_ingredients = [ingredient.lower() for ingredient in user_ingredients]

        for index, row in self.recipes_data.iterrows():
            ingredients = row['Cleaned_Ingredients'].split(",")
            if all(ingredient in [i.strip().lower() for i in ingredients] for ingredient in user_ingredients):
                matched_recipes.append(row)

        if matched_recipes:
            return matched_recipes
        else:
            return None

    def provide_recipe(self, recipe):
        """Provide detailed instructions for a found recipe"""
        response = f"Recipe: {recipe['Title']}\nIngredients: {recipe['Ingredients']}\nInstructions: {recipe['Instructions']}"
        return response

    def suggest_seasonal_ingredients(self, season):
        seasonal_ingredients = {
            "spring": ["asparagus", "peas", "spinach", "strawberries"],
            "summer": ["tomato", "cucumber", "zucchini", "watermelon"],
            "fall": ["pumpkin", "sweet potato", "apples", "carrot"],
            "winter": ["kale", "brussels sprouts", "squash", "oranges"]
        }

        season = season.lower()
        if season in seasonal_ingredients:
            ingredients = ", ".join(seasonal_ingredients[season])
            return f"Seasonal ingredients for {season}: {ingredients}"
        else:
            return "Sorry, I don't have seasonal ingredient suggestions for that season."

    def provide_meal_ideas(self, ingredients):
        meal_ideas = {
            "chicken": "Try making a chicken salad, grilled chicken with vegetables, or a chicken stir-fry!",
            "tomato": "How about a tomato soup, caprese salad, or pasta with tomato sauce?",
            "spinach": "Spinach can be used in a salad, a spinach quiche, or sautéed with garlic!",
            "apple": "Make a fresh apple pie, apple sauce, or a healthy apple salad!"
        }
        ingredients = [ingredient.lower() for ingredient in ingredients]
        ideas = []
        for ingredient in ingredients:
            if ingredient in meal_ideas:
                ideas.append(meal_ideas[ingredient])
        if ideas:
            return "\n".join(ideas)
        else:
            return "I don't have specific meal ideas for those ingredients, but I can help you find recipes!"

    def provide_cooking_tips(self):
        cooking_tips = [
            "Always preheat your oven before baking.",
            "To keep herbs fresh longer, store them in a damp paper towel in the fridge.",
            "Use a sharp knife for better control and safety.",
            "Let your meat rest for a few minutes after cooking to keep it juicy.",
            "When cooking pasta, salt the water generously to enhance the flavor of the pasta."
        ]
        return "\n".join(cooking_tips)

    def generate_response(self, user_input):
        user_input = user_input.lower()

        # Check if the user provided ingredients information
        ingredient_match = re.search(r"ingredients?: (.*)", user_input)
        if ingredient_match:
            user_ingredients = ingredient_match.group(1).split(",")
            matched_recipes = self.suggest_recipe(user_ingredients)
            if matched_recipes:
                responses = [self.provide_recipe(recipe) for recipe in matched_recipes]
                return "\n\n".join(responses)
            else:
                return "Sorry, I couldn't find any recipes with those ingredients. Try adding more ingredients or check your input."

        # Check if the user is asking for seasonal ingredients
        season_match = re.search(r"seasonal ingredients for (\w+)", user_input)
        if season_match:
            season = season_match.group(1)
            return self.suggest_seasonal_ingredients(season)

        # Check if the user is asking for meal ideas
        meal_match = re.search(r"meal ideas? (with|for)? (.*)", user_input)
        if meal_match:
            ingredients = meal_match.group(2).split(",")
            return self.provide_meal_ideas(ingredients)

        # Check if the user is asking for cooking tips
        cooking_tips_match = re.search(r"cooking tips?", user_input)
        if cooking_tips_match:
            return self.provide_cooking_tips()

        # Suggest recipe based on specific ingredients
        ingredient_only_match = re.search(r"recipes for (\w+)", user_input)
        if ingredient_only_match:
            ingredient = ingredient_only_match.group(1)
            matched_recipes = self.suggest_recipe([ingredient])
            if matched_recipes:
                responses = [self.provide_recipe(recipe) for recipe in matched_recipes]
                return "\n\n".join(responses)
            else:
                return f"Sorry, I couldn't find any recipes for {ingredient}. Try adding more ingredients or check your input."

        return super().generate_response(user_input)


