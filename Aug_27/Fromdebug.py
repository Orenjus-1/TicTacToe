import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
GRID_SIZE = 200
LINE_WIDTH = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)

# Theme-related variables
themes = {
    "default": "images/themes/default/",
    "classic": "images/themes/classic/",
    "retro": "images/themes/retro/"
}
selected_theme = "default"

# Paths to images
theme_path = themes[selected_theme]
BACKGROUND_IMG = theme_path + "background.png"
GRID_IMG = theme_path + "grid.png"
X_IMG = theme_path + "x.png"
O_IMG = theme_path + "o.png"
BUTTON_IMG = theme_path + "button.png"
TITLE_IMG = theme_path + "title.png"
SMALL_IMG = theme_path + "small.png"
SCORE_IMG = theme_path + "scoreboard.png"
WINNER_IMG = theme_path + "winner.png"

# Load images
background = pygame.image.load(BACKGROUND_IMG)
grid_img = pygame.image.load(GRID_IMG)
x_img = pygame.image.load(X_IMG)
o_img = pygame.image.load(O_IMG)
button_img = pygame.image.load(BUTTON_IMG)
title_img = pygame.image.load(TITLE_IMG)
small_img = pygame.image.load(SMALL_IMG)
score_img = pygame.image.load(SCORE_IMG)
winner_img = pygame.image.load(WINNER_IMG)

# Scale images
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
grid_img = pygame.transform.scale(grid_img, (GRID_SIZE * 3, GRID_SIZE * 3))
x_img = pygame.transform.scale(x_img, (GRID_SIZE - 20, GRID_SIZE - 20))
o_img = pygame.transform.scale(o_img, (GRID_SIZE - 20, GRID_SIZE - 20))
button_img = pygame.transform.scale(button_img, (200, 50))
title_img = pygame.transform.scale(title_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
small_img = pygame.transform.scale(small_img, (GRID_SIZE - 20, GRID_SIZE - 20))
score_img = pygame.transform.scale(score_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
winner_img = pygame.transform.scale(winner_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load sounds
click_sound = pygame.mixer.Sound("sounds/click.wav")
place_sound = pygame.mixer.Sound("sounds/place.wav")
win_sound = pygame.mixer.Sound("sounds/win.wav")

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Fonts
font = pygame.font.Font(None, 30)

# Game variables
board = [["", "", ""], ["", "", ""], ["", "", ""]]
player_turn = True
game_over = False
player_choice = "X"
ai_choice = "O"
player_score = 0
ai_score = 0
round_count = 0
max_rounds = 3
single_player_mode = True  # Track if the game is single-player or multiplayer

def draw_board():
    screen.blit(background, (0, 0))
    screen.blit(grid_img, (0, 0))

    for row in range(3):
        for col in range(3):
            if board[row][col] == "X":
                screen.blit(x_img, (col * GRID_SIZE + 10, row * GRID_SIZE + 10))
            elif board[row][col] == "O":
                screen.blit(o_img, (col * GRID_SIZE + 10, row * GRID_SIZE + 10))

    # Draw lines (Optional if you want visual grid separation)
    pygame.draw.line(screen, BLACK, (0, GRID_SIZE), (SCREEN_WIDTH, GRID_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (0, GRID_SIZE * 2), (SCREEN_WIDTH, GRID_SIZE * 2), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (GRID_SIZE, 0), (GRID_SIZE, SCREEN_HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (GRID_SIZE * 2, 0), (GRID_SIZE * 2, SCREEN_HEIGHT), LINE_WIDTH)

def check_winner():
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != "":
            pygame.draw.line(screen, RED, (0, row * GRID_SIZE + GRID_SIZE // 2), 
                            (SCREEN_WIDTH, row * GRID_SIZE + GRID_SIZE // 2), LINE_WIDTH)
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "":
            pygame.draw.line(screen, RED, (col * GRID_SIZE + GRID_SIZE // 2, 0), 
                            (col * GRID_SIZE + GRID_SIZE // 2, SCREEN_HEIGHT), LINE_WIDTH)
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != "":
        pygame.draw.line(screen, RED, (0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), LINE_WIDTH)
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        pygame.draw.line(screen, RED, (SCREEN_WIDTH, 0), (0, SCREEN_HEIGHT), LINE_WIDTH)
        return board[0][2]
    return None

def ai_best_move():
    # AI moves with a mix of strategy and randomness
    if random.random() < 0.3:  # 30% chance to make a random move
        # Take a random available spot
        available_moves = [(row, col) for row in range(3) for col in range(3) if board[row][col] == ""]
        return random.choice(available_moves) if available_moves else None

    # Otherwise, follow the strategy
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                board[row][col] = ai_choice
                if check_winner() == ai_choice:
                    return row, col
                board[row][col] = ""

    # Block player from winning
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                board[row][col] = player_choice
                if check_winner() == player_choice:
                    board[row][col] = ai_choice
                    return row, col
                board[row][col] = ""

    # Take the center if available
    if board[1][1] == "":
        return 1, 1

    # Take a random available corner
    for row, col in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        if board[row][col] == "":
            return row, col

    # Take any remaining spot
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                return row, col
    return None

def display_message(message):
    screen.blit(background, (0, 0))
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)

def draw_button_with_text(text, position):
    button_rect = pygame.Rect(position, (200, 50))
    screen.blit(button_img, button_rect.topleft)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

def show_menu():
    global single_player_mode
    menu_running = True
    while menu_running:
        screen.blit(background, (0, 0))
        screen.blit(title_img, (0, 0))
        
        draw_button_with_text("Single Player", (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))
        draw_button_with_text("Multiplayer", (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20))
        draw_button_with_text("Settings", (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 90))
        draw_button_with_text("Exit", (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 160))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50, 200, 50).collidepoint(mouse_pos):
                    click_sound.play()
                    menu_running = False
                    single_player_mode = True
                    game_loop()
                elif pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20, 200, 50).collidepoint(mouse_pos):
                    click_sound.play()
                    menu_running = False
                    single_player_mode = False
                    game_loop()
                elif pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 90, 200, 50).collidepoint(mouse_pos):
                    click_sound.play()
                    show_settings()
                elif pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 160, 200, 50).collidepoint(mouse_pos):
                    click_sound.play()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def show_settings():
    global selected_theme
    settings_running = True
    while settings_running:
        screen.blit(background, (0, 0))
        screen.blit(title_img, (0, 0))
        
        draw_button_with_text(f"Theme: {selected_theme.title()}", (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))
        draw_button_with_text("Back", (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50, 200, 50).collidepoint(mouse_pos):
                    click_sound.play()
                    cycle_themes()
                elif pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20, 200, 50).collidepoint(mouse_pos):
                    click_sound.play()
                    settings_running = False

        pygame.display.update()

def cycle_themes():
    global selected_theme
    theme_keys = list(themes.keys())
    current_index = theme_keys.index(selected_theme)
    next_index = (current_index + 1) % len(theme_keys)
    selected_theme = theme_keys[next_index]
    # Update paths
    update_theme()

def update_theme():
    global theme_path, background, grid_img, x_img, o_img, button_img, title_img, small_img, score_img, winner_img

    theme_path = themes[selected_theme]
    background = pygame.image.load(theme_path + "background.png")
    grid_img = pygame.image.load(theme_path + "grid.png")
    x_img = pygame.image.load(theme_path + "x.png")
    o_img = pygame.image.load(theme_path + "o.png")
    button_img = pygame.image.load(theme_path + "button.png")
    title_img = pygame.image.load(theme_path + "title.png")
    small_img = pygame.image.load(theme_path + "small.png")
    score_img = pygame.image.load(theme_path + "scoreboard.png")
    winner_img = pygame.image.load(theme_path + "winner.png")

    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    grid_img = pygame.transform.scale(grid_img, (GRID_SIZE * 3, GRID_SIZE * 3))
    x_img = pygame.transform.scale(x_img, (GRID_SIZE - 20, GRID_SIZE - 20))
    o_img = pygame.transform.scale(o_img, (GRID_SIZE - 20, GRID_SIZE - 20))
    button_img = pygame.transform.scale(button_img, (200, 50))
    title_img = pygame.transform.scale(title_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    small_img = pygame.transform.scale(small_img, (GRID_SIZE - 20, GRID_SIZE - 20))
    score_img = pygame.transform.scale(score_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    winner_img = pygame.transform.scale(winner_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

def game_loop():
    global board, player_turn, game_over, round_count, player_score, ai_score
    board = [["", "", ""], ["", "", ""], ["", "", ""]]
    player_turn = True
    game_over = False
    round_count += 1

    while not game_over:
        draw_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and player_turn and not game_over:
                mouse_x, mouse_y = event.pos
                row, col = mouse_y // GRID_SIZE, mouse_x // GRID_SIZE

                if board[row][col] == "":
                    board[row][col] = player_choice
                    place_sound.play()
                    winner = check_winner()
                    if winner:
                        game_over = True
                        player_score += 1 if winner == player_choice else 0
                        ai_score += 1 if winner == ai_choice else 0
                        draw_board()
                        pygame.display.update()
                        time.sleep(2)
                    player_turn = False

        if not player_turn and not game_over and single_player_mode:
            ai_move = ai_best_move()
            if ai_move:
                row, col = ai_move
                board[row][col] = ai_choice
                place_sound.play()
                winner = check_winner()
                if winner:
                    game_over = True
                    player_score += 1 if winner == player_choice else 0
                    ai_score += 1 if winner == ai_choice else 0
                    draw_board()
                    pygame.display.update()
                    time.sleep(2)
            player_turn = True

        if game_over:
            if round_count < max_rounds:
                game_loop()  # Start a new round
            else:
                display_winner()
                show_menu()

        pygame.display.update()

def display_winner():
    screen.blit(winner_img, (0, 0))
    message = "Player Wins!" if player_score > ai_score else "AI Wins!" if ai_score > player_score else "It's a Tie!"
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(text, text_rect)
    pygame.display.update()
    time.sleep(3)

if __name__ == "__main__":
    show_menu()
