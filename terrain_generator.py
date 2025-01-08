from opensimplex import OpenSimplex
import random

class TerrainGenerator:
    def __init__(self, grid_size, seed):
        self.grid_size = grid_size
        self.seed = seed
        self.noise_gen = OpenSimplex(seed)  # Générateur de bruit simplex
        self.wall_textures = ["img/pierre.png", "img/lave.png", "img/pierre2.png", "img/lave2.png"]
        self.water_textures = ["img/eau.png", "img/eau2.png", "img/eau.jpeg"]
        self.ground_textures = ["img/terre.jpeg", "img/terre3.png", "img/terre.png", "img/sable.png", "img/sable2.png", "img/feux.png"]

    def generate_perlin_terrain(self, scale=0.1, threshold_wall=0.5, threshold_lake=-0.3):
        terrain = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                # Utilisation de opensimplex pour un bruit plus lisse
                noise_value = self.noise_gen.noise2(x * scale, y * scale)

                if noise_value > threshold_wall:
                    terrain[x][y] = "wall"
                elif noise_value < threshold_lake:
                    terrain[x][y] = "lake"

        return terrain

    def place_treasure(self, game):
        attempts = 0

        while attempts < 15:
            x = random.randint(0, game.grid_size - 1)
            y = random.randint(0, game.grid_size - 1)

            if self.is_position_valid(game, x, y):
                treasure = game.create_entity()
                treasure.x, treasure.y = x, y
                return treasure

            attempts += 1

        self.regenerate_game(game)

    def is_position_valid(self, game, x, y):
        if game.terrain[x][y] is not None:
            return False

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < game.grid_size and 0 <= ny < game.grid_size:
                if game.terrain[nx][ny] is None:
                    return True

        return False

    def regenerate_game(self, game):
        game.seed = random.randint(0, 100000)  
        game.entities.clear()
        game.components.clear()
        game.setup()
