# components.py

class Component:
    pass

class PositionComponent(Component):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class RenderComponent(Component):
    def __init__(self, color, image_path=None):
        self.color = color
        self.image_path = image_path  # Chemin de l'image


class CollidableComponent(Component):
    """Indique qu'une entité est infranchissable."""
    pass
