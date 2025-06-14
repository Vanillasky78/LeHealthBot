from config import DEFAULT_CALORIES

class UserProfile:
    def __init__(self, gender: str, current_weight: float, target_weight: float):
        self.gender = gender
        self.current_weight = current_weight
        self.target_weight = target_weight
        self.loss_needed = current_weight - target_weight

    def recommend_calorie_intake(self) -> float:
        base = DEFAULT_CALORIES["base"]
        if self.gender.lower() == "male":
            base += DEFAULT_CALORIES["male_bonus"]
        if self.loss_needed > 0:
            base -= self.loss_needed * DEFAULT_CALORIES["loss_penalty_per_kg"]
        return max(base, DEFAULT_CALORIES["min"])

