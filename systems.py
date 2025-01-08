# systems.py
import random  
from components import PositionComponent, RenderComponent, CollidableComponent
from PIL import Image, ImageTk
import os

class System:
    def update(self, entities, components):
        raise NotImplementedError

class MovementSystem(System):
    def __init__(self, grid_size):
        self.grid_size = grid_size

    def move(self, entity, dx, dy, components, entities, terrain):
        if PositionComponent in components[entity]:
            pos = components[entity][PositionComponent]
            new_x = pos.x + dx
            new_y = pos.y + dy

            # Vérifie les limites de la grille
            if not (0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size):
                return  # Hors de la grille, ne pas bouger

            # Vérifie si la case cible est un lac
            if terrain[new_x][new_y] == "lake":
                if random.random() < 0.4:  # Par exemple, 40% de chance de ne pas avancer
                    return  # Ne pas bouger si la chance échoue

            # Vérifie les collisions avec les murs
            for other_entity in entities:
                if other_entity != entity and CollidableComponent in components[other_entity]:
                    other_pos = components[other_entity][PositionComponent]
                    if other_pos.x == new_x and other_pos.y == new_y:
                        return  # Collision avec un mur, ne pas bouger

            # Si tout est bon, déplace l'entité
            pos.x, pos.y = new_x, new_y
            
class RenderSystem:
    def __init__(self, canvas, grid_size, cell_size, default_bg_image=None):
        self.canvas = canvas
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.image_cache = {}  # Cache pour les images chargées
        self.default_bg_image = default_bg_image  # Chemin de l'image par défaut pour le fond

    def load_image(self, image_path):
        if image_path not in self.image_cache:
            if os.path.exists(image_path):
                image = Image.open(image_path).resize((self.cell_size, self.cell_size), Image.Resampling.LANCZOS)
                self.image_cache[image_path] = ImageTk.PhotoImage(image)
            else:
                self.image_cache[image_path] = None
        return self.image_cache[image_path]

    def draw_background(self):
        # Charge l'image de fond ou utilise une couleur blanche par défaut
        bg_image = self.load_image(self.default_bg_image) if self.default_bg_image else None

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                if bg_image:
                    self.canvas.create_image(x1, y1, anchor="nw", image=bg_image)
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")

    def update(self, entities, components):
        self.canvas.delete("all")  # Efface l'ancien rendu

        # Dessine le fond d'écran
        self.draw_background()

        # Dessine les entités
        for entity in entities:
            position = components.get(entity, {}).get(PositionComponent)
            render = components.get(entity, {}).get(RenderComponent)

            if position and render:
                x1 = position.x * self.cell_size
                y1 = position.y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # Chargement et affichage de l'image ou de la couleur
                if render.image_path:
                    image = self.load_image(render.image_path)
                    if image:
                        self.canvas.create_image(x1, y1, anchor="nw", image=image)
                    else:
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill=render.color)
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=render.color)


class GameLogicSystem(System):
    def __init__(self, message_label, game):
        self.message_label = message_label
        self.game = game  # Référence au jeu pour pouvoir réinitialiser

    def update(self, entities, components):
        for entity in entities:
            if PositionComponent in components[entity]:
                pos = components[entity][PositionComponent]
                for other_entity in entities:
                    if other_entity != entity and RenderComponent in components[other_entity]:
                        other_pos = components[other_entity][PositionComponent]
                        render = components[other_entity][RenderComponent]
                        # Si le joueur atteint le coffre
                        if pos.x == other_pos.x and pos.y == other_pos.y and render.color == "gold":
                            self.message_label.config(text="Vous avez trouvé le coffre !")
                            self.game.reset_game()  # Réinitialise le jeu
                            return

        self.message_label.config(text="")  # Réinitialise le message s'il n'y a pas de coffre atteint

