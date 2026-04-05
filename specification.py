class TempSpec:
    def is_satisfied(self, item, weather):
        return item["temp_min_c"] <= weather["temp"] <= item["temp_max_c"]