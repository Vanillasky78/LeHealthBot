class UserProfile:
    def __init__(self, gender: str, current_weight: float, target_weight: float):
        self.gender = gender
        self.current_weight = current_weight
        self.target_weight = target_weight
        self.loss_needed = current_weight - target_weight

    def recommend_calorie_intake(self) -> float:
        # Simple estimate: base + gender delta - weight loss goal
        base = 1800
        if self.gender == 'male':
            base += 200
        if self.loss_needed > 0:
            base -= self.loss_needed * 20
        return max(base, 1200)