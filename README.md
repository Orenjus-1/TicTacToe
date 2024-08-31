# Tic-Tac-Toe Game by [ReingelTubongbanua]

A classic Tic-Tac-Toe game implemented in Python using Pygame. This project features both single-player and multiplayer modes, a customizable theme system, sound effects, and a score-tracking mechanism. This was Made and Developed with the assistance from AI ChatGPT.

# NOTE TO RUN THE GAME!
## After unzipping the downloaded file, open the folder in Visual Studio Code as is. 
- If an error such as "FileNotFoundError: No file 'images/themes/default/background.png' found in working directory" appears, you can try changing the file path.
  ```bash
  themes = {
    "default": {
        "image_path": "TicTacToe-main/images/themes/default/", #####change or delete "TicTacToe-main/"
        "sound_path": "TicTacToe-main/sounds/default/"
    },
    "classic": {
        "image_path": "TicTacToe-main/images/themes/classic/", ####change or delete "TicTacToe-main/"
        "sound_path": "TicTacToe-main/sounds/classic/"
    },
    "retro": {
        "image_path": "TicTacToe-main/images/themes/retro/", ####change or delete "TicTacToe-main/"
        "sound_path": "TicTacToe-main/sounds/retro/"
    }
}

- Run main.py file


## Features

- **Single Player Mode**: Play against a simple AI that uses basic strategy with a mix of randomness.
- **Multiplayer Mode**: Play with a friend on the same device.
- **Custom Themes**: Choose between different themes (`default`, `classic`, and `retro`), each with its own set of images and sounds.
- **Score Tracking**: Track player scores in both modes. In multiplayer mode, the scores of Player X and Player O are displayed separately.
- **Dynamic End Screens**: Shows different screens based on the game result, including win, draw, and game over conditions.
- **Windowed Mode**: The game runs in a windowed screen size of 600x600 pixels, providing a consistent and compact play 
area.

# main.py

## Bug Fixes

- **Score Display Fixes**: Resolved issues where scores were not shown properly in both single-player and multiplayer modes.
- **Overlap Correction**: Fixed the overlapping of single-player and multiplayer scores, ensuring clear display of relevant scores for each mode.

## Added Features

- **New Themes**: Added two new themes, `classic` and `retro`, each with unique visuals and sound effects.
- **Sound Effects**: Introduced sound effects for every theme, enhancing the game experience with audio cues that match the selected theme.

## Game Modes

1. **Single Player**: Play against the AI. You can choose to play as either X or O.
2. **Multiplayer**: Play with a friend, taking turns as Player X and Player O.

## Controls

- Click on the menu options to navigate.
- Click on the grid to place your symbol (X or O).
- Use the buttons on the score screen to retry, continue, or return to the menu.

# How to Run 

## Prerequisites

- Python 3.x installed on your machine.
- Pygame library installed. You can install it using pip:

  ```bash
  pip install pygame

## Folder Structure for Reference

 ```bash
TicTacToe_main/
│
├── images/
│   └── themes/
│       ├── default/
│       ├── classic/
│       └── retro/
│
├── sounds/
│   ├── default/
│   ├── classic/
│   └── retro/
│
└── Final/
│   ├── main.py
│   └── README.md
│
└── default_preview
│
└── classic_preview
│
└── retro_preview

```
## Theme Customization

- You can customize themes by modifying the themes dictionary in main.py. Add new themes by specifying the path to your custom images and sound files:

 ```bash
themes = {
    "default": {
        "image_path": "images/themes/default/",
        "sound_path": "sounds/default/"
    },
    ...
}

```
## Future Improvements
Enhance the AI with more advanced algorithms.
Add online multiplayer functionality.
Create more themes and sound packs.

### Acknowledgments 
Pygame Documentation - For game development resources.
Sound and image assets were custom-made or sourced from free assets libraries.
