from chatbot.base import ChatbotBase
from chatbot.user_profile import UserProfile
import pandas as pd
import os

class FatLossChatBot(ChatbotBase):
    def __init__(self):
        self.user_profile = None
        self.state = 'INIT'  # INIT, ASKED_WEIGHT, ASKED_TARGET
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(base_dir, "..", "data", "food_plans_500_en.csv")
            self.food_df = pd.read_csv(csv_path)
        except:
            self.food_df = pd.DataFrame()

    def generate_response(self, user_input: str) -> str:
        if self.state == 'INIT':
            self.state = 'ASKED_GENDER'
            return "Welcome to LeHealthBot! Please enter your gender (male/female):"

        if self.state == 'ASKED_GENDER':
            gender = user_input.strip().lower()
            if gender not in ['male', 'female']:
                return "Please enter 'male' or 'female':"
            self.temp_gender = gender
            self.state = 'ASKED_WEIGHT'
            return "Please enter your current weight (kg):"

        if self.state == 'ASKED_WEIGHT':
            try:
                weight = float(user_input)
                self.temp_current_weight = weight
                self.state = 'ASKED_TARGET'
                return "Please enter your target weight (kg):"
            except:
                return "Please enter a valid number for weight."

        if self.state == 'ASKED_TARGET':
            try:
                target = float(user_input)
                self.user_profile = UserProfile(self.temp_gender, self.temp_current_weight, target)
                self.state = 'READY'
                kcal = self.user_profile.recommend_calorie_intake()
                return f"✅ Profile set! You aim to lose {self.user_profile.loss_needed:.1f} kg. Recommended daily intake: {kcal:.0f} kcal. Would you like meal suggestions for today?"
            except:
                return "Please enter a valid target weight (kg)."

        if self.state == 'READY':
            if not self.food_df.empty:
                kcal = self.user_profile.recommend_calorie_intake()
                filtered = self.food_df[self.food_df["calories"] <= kcal].sample(n=3, replace=True)
                response = "🍽️ Here are your recommended meals for today:\n"
                for i, row in filtered.iterrows():
                    response += f"{i+1}. {row['title']} ({row['calories']} kcal)\n"
                    response += f"   Ingredients: {row['ingredients']}\n"
                    response += f"   Instructions: {row['instructions']}\n\n"
                return response.strip()
            else:
                return "⚠️ Unable to load meal data. Please try again later."

        return "I didn't understand that. Could you please try again?"
