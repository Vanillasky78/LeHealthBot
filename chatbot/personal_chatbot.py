from chatbot.base import ChatbotBase
from chatbot.user_profile import UserProfile
from config import SUGAR_KEYWORDS, FRY_KEYWORDS, DEFAULT_CALORIES
import pandas as pd
import os

class LeHealthBot(ChatbotBase):
    """
    LeHealthBot is a personalized chatbot for fat-loss meal recommendation.
    It guides the user through health screening and provides calorie-appropriate
    food suggestions with risk classification based on sugar and fried ingredients.
    """

    def __init__(self):
        self.user_profile = None
        self.state = 'INIT'
        self.meal_queue = []
        self.fatty_liver_risk = None
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(base_dir, "..", "data", "food_plans_500_en.csv")
            self.food_df = pd.read_csv(csv_path)
        except Exception:
            self.food_df = pd.DataFrame()

    def classify_meal_risk(self, ingredients: str) -> str:
        """Classify meal risk based on presence of sugar or fried keywords."""
        ingredients = ingredients.lower()
        has_sugar = any(kw in ingredients for kw in SUGAR_KEYWORDS)
        has_fried = any(kw in ingredients for kw in FRY_KEYWORDS)

        if has_sugar and has_fried:
            return "🔴 High Risk: Sugar + Fried"
        elif has_sugar or has_fried:
            return "🟠 Moderate Risk: Sugar or Fried"
        else:
            return "🟢 Low Risk"

    def generate_response(self, user_input: str) -> str:
        if self.state == 'INIT':
            self.state = 'ASKED_FATTY_HISTORY'
            return "🩺 Have you ever been told you have fatty liver in a medical check-up? (yes/no)"

        if self.state == 'ASKED_FATTY_HISTORY':
            answer = user_input.strip().lower()
            if answer not in ['yes', 'no']:
                return "❓ Please answer 'yes' or 'no'."
            self.fatty_liver_risk = (answer == 'yes')
            self.state = 'ASKED_GENDER'
            return "👤 Please enter your gender (male/female):"

        if self.state == 'ASKED_GENDER':
            gender = user_input.strip().lower()
            if gender not in ['male', 'female']:
                return "❓ Please enter 'male' or 'female':"
            self.temp_gender = gender
            self.state = 'ASKED_WEIGHT'
            return "⚖️ Please enter your current weight (kg):"

        if self.state == 'ASKED_WEIGHT':
            try:
                weight = float(user_input)
                self.temp_current_weight = weight
                self.state = 'ASKED_TARGET'
                return "🎯 Please enter your target weight (kg):"
            except:
                return "❗ Please enter a valid number for weight."

        if self.state == 'ASKED_TARGET':
            try:
                target = float(user_input)
                self.user_profile = UserProfile(self.temp_gender, self.temp_current_weight, target)
                self.state = 'READY'
                kcal = self.user_profile.recommend_calorie_intake()
                message = f"✅ Profile set! You aim to lose {self.user_profile.loss_needed:.1f} kg. Recommended daily intake: {kcal:.0f} kcal."
                if self.fatty_liver_risk:
                    message += "\n⚠️ Since you've indicated fatty liver history, we suggest minimizing sugar and fried food intake."
                message += "\nClick below to receive today's personalized meal recommendation."
                return message
            except:
                return "❗ Please enter a valid target weight (kg)."

        if self.state == 'READY':
            if not self.food_df.empty:
                if not self.meal_queue:
                    kcal = self.user_profile.recommend_calorie_intake()
                    filtered = self.food_df[self.food_df["calories"] <= kcal].sample(n=3, replace=True)
                    self.meal_queue = filtered.to_dict(orient='records')
                meal = self.meal_queue.pop(0)
                risk_level = self.classify_meal_risk(meal['ingredients']) if self.fatty_liver_risk else ""
                response = f"🍽️ Today's recommendation:\n"
                response += f"**{meal['title']}** ({meal['calories']} kcal)\n"
                response += f"{risk_level}\n"
                response += f"**Ingredients:** {meal['ingredients']}\n"
                response += f"**Instructions:** {meal['instructions']}"
                if not self.meal_queue:
                    response += "\n✅ That's all for today. Stay consistent and check back tomorrow!"
                else:
                    response += "\n➡️ Click again for the next suggestion."
                return response.strip()
            else:
                return "⚠️ Unable to load meal data. Please try again later."

        return "❓ I didn't understand that. Could you please try again?"
