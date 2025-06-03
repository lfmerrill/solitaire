# Solitaire

A classic Solitaire (Klondike) card game implemented in Python using Pygame.

## Features

- Standard Solitaire rules and gameplay
- Graphical interface with card images
- Clickable cards and piles
- "New Game" button
- Win detection

## Requirements

- Python 3.x
- [Pygame](https://www.pygame.org/)

## Installation

1. Clone this repository:
    ```sh
    git clone https://github.com/lfmerrill/solitaire.git
    cd solitaire
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Make sure the `images/` folder contains all card images (e.g., `2_of_clubs.png`, ..., `king_of_spades.png`, and `back_of_card.png`).

## How to Play

1. Run the game:
    ```sh
    python -m game.game
    ```

2. Use your mouse to:
    - Click cards to select and move them according to Solitaire rules.
    - Click the "New Game" button to restart.
    - Move cards between tableau, foundation, and waste piles.

3. The game ends when all cards are moved to the foundation piles.

## Project Structure

```
solitaire/
├── game/
│   ├── card.py
│   ├── deck.py
│   └── game.py
├── images/
│   ├── 2_of_clubs.png
│   ├── ...
│   └── back_of_card.png
├── requirements.txt
└── README.md
```

- [`game/card.py`](game/card.py): Card class and rendering logic
- [`game/deck.py`](game/deck.py): Deck creation and shuffling
- [`game/game.py`](game/game.py): Main game logic and Pygame loop

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.