import tkinter as tk
from components import PositionComponent

class GameInterface:
    def __init__(self, root, game):
        self.game = game

        canvas_width = game.grid_size * game.cell_size
        canvas_height = game.grid_size * game.cell_size
        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack()

        self.message_label = tk.Label(root, text="", font=("Arial", 14))
        self.message_label.pack()

        self.detail_frame = tk.Frame(root)
        self.detail_label = tk.Label(self.detail_frame, text="", font=("Arial", 12), justify="left", bg="lightgray", padx=10, pady=10)
        self.detail_label.pack()
        self.detail_frame.pack_forget()

        self.show_details_button = tk.Button(root, text="Afficher les détails", command=self.show_details)
        self.show_details_button.pack()

        self.hide_details_button = tk.Button(root, text="Masquer les détails", command=self.hide_details)
        self.hide_details_button.pack_forget()

    def show_details(self):
        self.detail_frame.pack()
        self.show_details_button.pack_forget()
        self.hide_details_button.pack()
        
        # Met à jour les détails du joueur
        player_components = self.game.components.get(self.game.player, {})
        self.update_player_details(player_components)


    def hide_details(self):
        self.detail_frame.pack_forget()
        self.hide_details_button.pack_forget()
        self.show_details_button.pack()

    def update_player_details(self, player_components):
        position = player_components.get(PositionComponent)
        if position:
            details = (
                f"Détails du personnage :\n"
                f"- Position : ({position.x}, {position.y})\n"
                
            )
            self.detail_label.config(text=details)
