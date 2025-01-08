from noise import pnoise2
import random

class TerrainGenerator:
    def __init__(self, grid_size, seed):
        self.grid_size = grid_size
        self.seed = seed
        self.wall_textures = ["img/pierre.png", "img/lave.png", "img/pierre2.png", "img/lave2.png"]
        self.water_textures = ["img/eau.png", "img/eau2.png", "img/eau.jpeg"]
        self.ground_textures = ["img/terre.jpeg", "img/terre3.png", "img/terre.png", "img/sable.png", "img/sable2.png", "img/feux.png"]

    def generate_perlin_terrain(self, scale=0.1, threshold_wall=0.5, threshold_lake=-0.3):
        #print("Seed:", self.seed, "Scale:", scale, "Threshold Wall:", threshold_wall, "Threshold Lake:", threshold_lake)
        terrain = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                noise_value = pnoise2((x + self.seed) * scale, (y + self.seed) * scale)

                if noise_value > threshold_wall:
                    terrain[x][y] = "wall"
                elif noise_value < threshold_lake:
                    terrain[x][y] = "lake"

        return terrain

    def place_treasure(self, game):
        """Place un coffre dans une position valide ou régénère la carte si nécessaire."""
        attempts = 0

        while attempts < 15:
            x = random.randint(0, game.grid_size - 1)
            y = random.randint(0, game.grid_size - 1)

            if self.is_position_valid(game, x, y):
                # Crée une entité pour le coffre et retourne sa position
                treasure = game.create_entity()
                treasure.x, treasure.y = x, y
                return treasure

            attempts += 1

        # Si aucune position valide n'est trouvée, régénérer la carte
        self.regenerate_game(game)

    def is_position_valid(self, game, x, y):
        """Vérifie si une position est valide pour placer le coffre."""
        # Vérifie que la position n'est pas un mur, un lac ou occupée
        if game.terrain[x][y] is not None:
            return False

        # Vérifie qu'il y a des cases accessibles autour
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < game.grid_size and 0 <= ny < game.grid_size:
                if game.terrain[nx][ny] is None:  # Case libre
                    return True

        return False

    def regenerate_game(self, game):
        """Régénère le jeu si le placement du coffre échoue."""
        game.seed = random.randint(0, 100000)  # Nouveau seed pour le terrain
        game.entities.clear()
        game.components.clear()
        game.setup()  # Régénère les entités et la carte
