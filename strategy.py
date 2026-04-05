# Strategy pattern
# This class defines how a clothing item is scored
# based on current weather conditions

class RecommendationStrategy:
    # simple scoring logic (can be improved later)
    # currently returns a constant score for simplicity
    def score(self, item, weather):
        return 1