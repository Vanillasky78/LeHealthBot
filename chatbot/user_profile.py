class UserProfile:
    def __init__(self, gender: str, current_weight: float, target_weight: float):
        self.gender = gender
        self.current_weight = current_weight
        self.target_weight = target_weight
        self.loss_needed = current_weight - target_weight
        self.days_elapsed = 0

    def recommended_daily_fat_loss(self, days: int = 30) -> float:
        return self.loss_needed / days

    def recommend_calorie_intake(self) -> float:
        deficit = self.recommended_daily_fat_loss() * 7200  # kcal per 1kg fat
        base = 2000 if self.gender == 'male' else 1600
        return max(1200, base - deficit)