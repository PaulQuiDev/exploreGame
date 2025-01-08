import tkinter as tk
from interface import GameInterface
from terrain_generator import TerrainGenerator
from components import PositionComponent, RenderComponent, CollidableComponent
from systems import MovementSystem, RenderSystem, GameLogicSystem
import random

class Entity:
    def __init__(self):
        self.id = id(self)

class Game:
    def __init__(self, root, grid_size=35, cell_size=20 , background_image="img/terre.png"):
        self.entities = []
        self.components = {}
        self.systems = []
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.seed = random.randint(0, 100000)  # Générer un seed aléatoire
        self.background_image = background_image
        self.wall_textures = ["img/pierre.png", "img/lave.png", "img/pierre2.png", "img/lave2.png"]
        self.water_textures = ["img/eau.png", "img/eau2.png", "img/eau.jpeg", "img/harbre.png"]
        self.ground_textures = ["img/terre.jpeg", "img/terre3.png", "img/terre.png", "img/sable.png", "img/sable2.png", "img/feux.png"]


        # Interface graphique
        self.interface = GameInterface(root, self)

        # Systèmes
        self.movement_system = MovementSystem(grid_size)
        self.render_system = RenderSystem(self.interface.canvas, grid_size, cell_size, self.background_image)
        self.logic_system = GameLogicSystem(self.interface.message_label, self)


    def create_entity(self):
        entity = Entity()
        self.entities.append(entity)
        self.components[entity] = {}
        return entity

    def add_component(self, entity, component):
        self.components[entity][type(component)] = component

    def add_system(self, system):
        # Vérifie si le système existe déjà dans la liste des systèmes
        for existing_system in self.systems:
            if isinstance(existing_system, type(system)):  # Vérifie si le système est du même type
                self.systems.remove(existing_system)  # Retire l'ancien système
        
        # Ajoute le nouveau système à la liste
        self.systems.append(system)


    def update(self):
        for system in self.systems:
            system.update(self.entities, self.components)
        # Met à jour les détails du joueur
        self.interface.update_player_details(self.components.get(self.player, {}))

    def move_player(self, dx, dy):
        self.movement_system.move(self.player, dx, dy, self.components, self.entities, self.terrain)
        self.update()


    def setup(self, scale=0.1, threshold_wall=0.5, threshold_lake=-0.3, 
          wall_texture="img/pierre.png", water_texture="img/eau.png"):
        generator = TerrainGenerator(self.grid_size, self.seed)
        self.terrain = generator.generate_perlin_terrain(scale, threshold_wall, threshold_lake)
        
        # Crée les entités du terrain
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.terrain[x][y] == "wall":
                    wall = self.create_entity()
                    self.add_component(wall, PositionComponent(x, y))
                    self.add_component(wall, RenderComponent("gray", wall_texture))  # Texture aléatoire pour le mur
                    self.add_component(wall, CollidableComponent())
                elif self.terrain[x][y] == "lake":
                    lake = self.create_entity()
                    self.add_component(lake, PositionComponent(x, y))
                    self.add_component(lake, RenderComponent("blue", water_texture))  # Texture aléatoire pour l'eau
    
        # Crée le joueur
        self.player = self.create_entity()
        self.add_component(self.player, PositionComponent(0, 0))
        self.add_component(self.player, RenderComponent("green", "img/hero.png"))
    
        # Place le coffre
        while True:
            self.treasure = generator.place_treasure(self)
            if self.treasure.x != 0 or self.treasure.y != 0:  # Évite de placer le coffre sur le joueur
                break
            
        self.add_component(self.treasure, PositionComponent(self.treasure.x, self.treasure.y))
        self.add_component(self.treasure, RenderComponent("gold", "img/cofre.png"))
    
        # Ajouter des systèmes
        self.add_system(self.render_system)
        self.add_system(self.logic_system)
    
        self.update()

    def reset_game(self):
        """Réinitialise le jeu avec de nouveaux paramètres et textures."""
        # Génère un nouveau seed pour le terrain
        self.seed = random.randint(0, 100000)

        # Modifie les paramètres pour plus de variété
        new_scale = random.uniform(0.05, 0.15)
        new_threshold_wall = random.uniform(0.3, 0.6)
        new_threshold_lake = random.uniform(-0.4, -0.2)

        
        # Sélection des textures aléatoires
        wall_texture = random.choice(self.wall_textures)
        water_texture = random.choice(self.water_textures)
        ground_texture = random.choice(self.ground_textures)
        #print("wall_texture:", wall_texture , " water" , water_texture ,"ground" , ground_texture)
        self.entities.clear()
        self.components.clear()

        self.background_image = ground_texture
        # Réinitialise le jeu avec les nouveaux paramètres et textures
        self.setup(scale=new_scale, 
                   threshold_wall=new_threshold_wall, 
                   threshold_lake=new_threshold_lake,
                   wall_texture=wall_texture,
                   water_texture=water_texture)



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Jeu d'exploration")

    game = Game(root)
    game.setup()

    # Liens clavier pour déplacer le joueur
    root.bind("<KeyRelease-Up>", lambda event: game.move_player(0, -1))
    root.bind("<KeyRelease-Down>", lambda event: game.move_player(0, 1))
    root.bind("<KeyRelease-Left>", lambda event: game.move_player(-1, 0))
    root.bind("<KeyRelease-Right>", lambda event: game.move_player(1, 0))


    root.mainloop()
