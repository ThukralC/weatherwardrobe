# Factory Method pattern
# This class is responsible for creating clothing item objects
# so that object creation is handled in one place

class ClothingFactory:
    def create(self, data):
        # return the item data (can be extended later if needed)
        return data