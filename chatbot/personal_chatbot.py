from chatbot.base import ChatbotBase
from chatbot.user_profile import UserProfile
import pandas as pd

class FatLossChatBot(ChatbotBase):
    def __init__(self):
        self.user_profile = None
        self.state = 'INIT'  # INIT, ASKED_WEIGHT, ASKED_TARGET
        try:
            self.food_df = pd.read_csv("data/food_plans_500_en.csv")
        except:
            self.food_df = pd.DataFrame()

    def generate_response(self, user_input: str) -> str:
        if self.state == 'INIT':
            self.state = 'ASKED_GENDER'
            return "欢迎来到 LeHealthBot！请告诉我你的性别（male/female）："

        if self.state == 'ASKED_GENDER':
            gender = user_input.strip().lower()
            if gender not in ['male', 'female']:
                return "请输入 male 或 female："
            self.temp_gender = gender
            self.state = 'ASKED_WEIGHT'
            return "请输入你目前的体重（kg）："

        if self.state == 'ASKED_WEIGHT':
            try:
                weight = float(user_input)
                self.temp_current_weight = weight
                self.state = 'ASKED_TARGET'
                return "请输入你的目标体重（kg）："
            except:
                return "请输入合法的数字体重："

        if self.state == 'ASKED_TARGET':
            try:
                target = float(user_input)
                self.user_profile = UserProfile(self.temp_gender, self.temp_current_weight, target)
                self.state = 'READY'
                kcal = self.user_profile.recommend_calorie_intake()
                return f"✅ 设定成功！你需要减掉 {self.user_profile.loss_needed:.1f} kg。我建议你每天摄入大约 {kcal:.0f} 千卡。今天你想我帮你推荐吃什么吗？"
            except:
                return "请输入合法的目标体重（kg）："

        if self.state == 'READY':
            if not self.food_df.empty:
                kcal = self.user_profile.recommend_calorie_intake()
                filtered = self.food_df[self.food_df["calories"] <= kcal].sample(n=3, replace=True)
                response = "🍽️ 今天我为你推荐以下饮食方案：\n"
                for i, row in filtered.iterrows():
                    response += f"{i+1}. {row['title']} ({row['calories']} kcal)\n"
                    response += f"   Ingredients: {row['ingredients']}\n"
                    response += f"   Instructions: {row['instructions']}\n\n"
                return response.strip()
            else:
                return "⚠️ 当前无法加载饮食数据，请稍后再试。"

        return "我还不太明白你的意思，能否再说一遍？"
