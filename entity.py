
class Entity:
    def __init__(self, x, y, char, color, name, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


def get_blocking_entities_at_location(entities, dest):
    for entity in entities:
        if entity.blocks and dest.x == entity.x and dest.y == entity.y:
            return entity
    return None


