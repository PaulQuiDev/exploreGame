# Jeu de Mouvement avec Terrain et Entités

Ce projet implémente un jeu avec des entités mobiles évoluant sur un terrain généré de manière procédurale. Les entités peuvent se déplacer, interagir avec des objets comme des coffres, et le terrain contient des éléments comme des lacs et des murs. Le jeu utilise une architecture basée sur les composants pour la gestion des entités et des systèmes de jeu.

## Fonctionnalités principales

- **Système de Mouvement** : Permet aux entités de se déplacer sur une grille, avec des vérifications de collision avec des murs ou des lacs.
- **Système de Rendu** : Affiche les entités et le terrain, en utilisant des images pour représenter les objets et le fond du jeu.
- **Logique du Jeu** : Gère les interactions, comme la collecte de coffres, et réinitialise le jeu en cas de succès.

## Installation

### Prérequis

- Python 3.10 - 3.11
- `Pillow` pour la gestion des images (si vous n'avez pas cette bibliothèque, installez-la avec `pip install Pillow`).
- pip install opensimplex


### Installation des dépendances

1. Clonez ce dépôt :

   ```bash
   git clone <url-du-dépôt>
   cd <nom-du-dossier>

```bash
/jeu
│
├── /assets                  # Dossier contenant les ressources du jeu (images, sons, etc.)
│   ├── character.png        # Image de l'entité principale (par exemple, un joueur)
│   ├── chest.png            # Image représentant un coffre
│   └── water.png            # Image représentant un lac
│
├── components.py            # Définit les composants (Position, Render, Collidable, Terrain)
│
├── img                      # Dossier contenant des images supplémentaires pour les entités
│   ├── wall.png             # Image représentant un mur
│   ├── lake.png             # Image représentant un lac
│   └── player.png           # Image représentant un joueur
│
├── interface.py             # Contient la logique de l'interface graphique (création des fenêtres et des interactions)
│
├── main.py                  # Point d'entrée du jeu, initialise tout et démarre l'interface
│
├── systems.py               # Contient les systèmes du jeu (Mouvement, Rendu, Logique, Génération de Terrain)
│
├── terrain_generator.py     # Contient la logique de génération du terrain procédural
│
└── README.md                # Documentation du projet (ce fichier)

