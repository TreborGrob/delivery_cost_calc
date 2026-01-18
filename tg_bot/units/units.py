class Cloth:
    def __init__(self, name: int, weight: int, length: int, width: int, height: int):
        self.name = name
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height

    def get_params(self):
        return self.name, self.weight, self.length, self.width, self.height
