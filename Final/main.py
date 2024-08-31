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
    "default": {
        "image_path": "TicTacToe-main/images/themes/default/",
        "sound_path": "TicTacToe-main/sounds/default/"
    },
    "classic": {
        "image_path": "TicTacToe-main/images/themes/classic/",
        "sound_path": "TicTacToe-main/sounds/classic/"
    },
    "retro": {
        "image_path": "TicTacToe-main/images/themes/retro/",
        "sound_path": "TicTacToe-main/sounds/retro/"
    }
}
selected_theme = "default"

# Paths to images and sounds
theme_path = themes[selected_theme]["image_path"]
sound_path = themes[selected_theme]["sound_path"]

BACKGROUND_IMG = theme_path + "background.png"
GRID_IMG = theme_path + "grid.png"
X_IMG = theme_path + "x.png"
O_IMG = theme_path + "o.png"
BUTTON_IMG = theme_path + "button.png"
TITLE_IMG = theme_path + "title.png"
SCORE_IMG = theme_path + "scoreboard.png"
RULES_IMG = theme_path + "rules.png"

CLICK_SOUND = sound_path + "click.wav"
PLACE_SOUND = sound_path + "place.wav"
WIN_SOUND = sound_path + "win.wav"

# Load images
background = pygame.image.load(BACKGROUND_IMG)
grid_img = pygame.image.load(GRID_IMG)
x_img = pygame.image.load(X_IMG)
o_img = pygame.image.load(O_IMG)
button_img = pygame.image.load(BUTTON_IMG)
title_img = pygame.image.load(TITLE_IMG)
score_img = pygame.image.load(SCORE_IMG)
rules_img = pygame.image.load(RULES_IMG)

# Scale images
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
grid_img = pygame.transform.scale(grid_img, (GRID_SIZE * 3, GRID_SIZE * 3))
x_img = pygame.transform.scale(x_img, (GRID_SIZE - 20, GRID_SIZE - 20))
o_img = pygame.transform.scale(o_img, (GRID_SIZE - 20, GRID_SIZE - 20))
button_img = pygame.transform.scale(button_img, (200, 50))
title_img = pygame.transform.scale(title_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
score_img = pygame.transform.scale(score_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
rules_img = pygame.transform.scale(rules_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load sounds
click_sound = pygame.mixer.Sound(CLICK_SOUND)
place_sound = pygame.mixer.Sound(PLACE_SOUND)
win_sound = pygame.mixer.Sound(WIN_SOUND)

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
player2_score = 0  # This will track the second player's score in multiplayer mode

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

def update_theme():
    global theme_path, sound_path, background, grid_img, x_img, o_img, button_img, title_img, score_img, rules_img
    global click_sound, place_sound, win_sound

    theme_path = themes[selected_theme]["image_path"]
    sound_path = themes[selected_theme]["sound_path"]

    # Update image paths
    background = pygame.image.load(theme_path + "background.png")
    grid_img = pygame.image.load(theme_path + "grid.png")
    x_img = pygame.image.load(theme_path + "x.png")
    o_img = pygame.image.load(theme_path + "o.png")
    button_img = pygame.image.load(theme_path + "button.png")
    title_img = pygame.image.load(theme_path + "title.png")
    score_img = pygame.image.load(theme_path + "scoreboard.png")
    rules_img = pygame.image.load(theme_path + "rules.png")

    # Update sound paths
    click_sound = pygame.mixer.Sound(sound_path + "click.wav")
    place_sound = pygame.mixer.Sound(sound_path + "place.wav")
    win_sound = pygame.mixer.Sound(sound_path + "win.wav")

    # Scale images
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    grid_img = pygame.transform.scale(grid_img, (GRID_SIZE * 3, GRID_SIZE * 3))
    x_img = pygame.transform.scale(x_img, (GRID_SIZE - 20, GRID_SIZE - 20))
    o_img = pygame.transform.scale(o_img, (GRID_SIZE - 20, GRID_SIZE - 20))
    button_img = pygame.transform.scale(button_img, (200, 50))
    title_img = pygame.transform.scale(title_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    score_img = pygame.transform.scale(score_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    rules_img = pygame.transform.scale(rules_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

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

def choose_player_mode(single_player=True):
    global player_choice, ai_choice
    if single_player:
        choosing = True
        while choosing:
            screen.blit(background, (0, 0))
            screen.blit(rules_img, (0, 0))
            draw_button_with_text("Play as X", (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))
            draw_button_with_text("Play as O", (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20))
            draw_button_with_text("Back to Menu", (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 90))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50, 200, 50).collidepoint(mouse_pos):
                        click_sound.play()
                        player_choice = "X"
                        ai_choice = "O"
                        choosing = False
                    elif pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20, 200, 50).collidepoint(mouse_pos):
                        click_sound.play()
                        player_choice = "O"
                        ai_choice = "X"
                        choosing = False
                    elif pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 90, 200, 50).collidepoint(mouse_pos):
                        click_sound.play()
                        show_menu()
                        return
            pygame.display.update()
        reset_board()
        game_loop()
    else:
        # For multiplayer, just start the game
        player_choice = "X"  # Player 1
        ai_choice = "O"      # Player 2
        reset_board()
        game_loop()

def reset_board():
    global board, player_turn, game_over
    board = [["", "", ""], ["", "", ""], ["", "", ""]]
    player_turn = True  # Ensure "X" always goes first
    game_over = False

def update_scores(winner):
    global player_score, ai_score, player2_score, round_count
    if single_player_mode:
        if winner == player_choice:
            player_score += 1
        elif winner == ai_choice:
            ai_score += 1
    else:  # Multiplayer mode
        if winner == "X":
            player_score += 1
        elif winner == "O":
            player2_score += 1

    round_count += 1

def check_best_of_3():
    return player_score >= 2 or ai_score >= 2

def show_end_screen(winner, consecutive_draws=0):
    screen.blit(score_img, (0, 0))
    win_sound.play()

    # Display scores based on game mode
    if single_player_mode:
        score_text = f"Player: {player_score}  AI: {ai_score}"
    else:
        score_text = f"Player X: {player_score}  Player O: {player2_score}"
    
    score_display = font.render(score_text, True, GREEN)
    score_rect = score_display.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
    screen.blit(score_display, score_rect)

    if winner:
        if single_player_mode:
            message = "Congratulations, you won!" if winner == player_choice else "AI Wins!"
        else:
            message = f"Player {winner} Wins!"
    elif consecutive_draws >= 3:
        message = "No one wins after 3 consecutive draws!"
    else:
        message = "It's a Draw!"
    
    text = font.render(message, True, GREEN)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(text, text_rect)
    
    draw_button_with_text("Retry", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100))
    draw_button_with_text("Menu", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 160))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50).collidepoint(mouse_pos):
                    click_sound.play()
                    return True  # Retry
                elif pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 160, 200, 50).collidepoint(mouse_pos):
                    click_sound.play()
                    return False  # Menu

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
    global single_player_mode, player_score, ai_score, player2_score
    # Reset scores when returning to the menu
    player_score = 0
    ai_score = 0
    player2_score = 0
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
                    choose_player_mode(single_player=True)
                elif pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20, 200, 50).collidepoint(mouse_pos):
                    click_sound.play()
                    menu_running = False
                    single_player_mode = False
                    choose_player_mode(single_player=False)
                elif pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 90, 200, 50).collidepoint(mouse_pos):
                    click_sound.play()
                    show_settings()
                elif pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 160, 200, 50).collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def game_loop():
    global player_turn, game_over, player_choice, ai_choice, consecutive_draws
    reset_board()
    draw_board()
    pygame.display.update()

    # If player chooses O, AI should make the first move as X
    if single_player_mode and player_choice == "O":
        ai_move = ai_best_move()
        if ai_move:
            board[ai_move[0]][ai_move[1]] = ai_choice
            place_sound.play()
            draw_board()
            pygame.display.update()
            player_turn = True

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked_row, clicked_col = mouse_y // GRID_SIZE, mouse_x // GRID_SIZE

                if board[clicked_row][clicked_col] == "":
                    if single_player_mode:
                        if player_turn:
                            board[clicked_row][clicked_col] = player_choice
                            place_sound.play()
                            draw_board()
                            pygame.display.update()
                            if check_winner() == player_choice:
                                update_scores(player_choice)
                                game_over = True
                                winner = player_choice
                            player_turn = False

                            # AI Move after player
                            if not game_over:
                                pygame.time.wait(500)  # Reduced delay before AI moves
                                ai_move = ai_best_move()
                                if ai_move:
                                    board[ai_move[0]][ai_move[1]] = ai_choice
                                    place_sound.play()
                                    draw_board()
                                    pygame.display.update()
                                    if check_winner() == ai_choice:
                                        update_scores(ai_choice)
                                        game_over = True
                                        winner = ai_choice
                                player_turn = True
                    else:
                        if player_turn:
                            board[clicked_row][clicked_col] = "X"
                            place_sound.play()
                            draw_board()
                            pygame.display.update()
                            if check_winner() == "X":
                                update_scores("X")
                                game_over = True
                                winner = "X"
                            player_turn = False
                        else:
                            board[clicked_row][clicked_col] = "O"
                            place_sound.play()
                            draw_board()
                            pygame.display.update()
                            if check_winner() == "O":
                                update_scores("O")
                                game_over = True
                                winner = "O"
                            player_turn = True

                draw_board()
                pygame.display.update()

        if not any("" in row for row in board) and not game_over:
            update_scores(None)
            game_over = True
            winner = None

    if check_best_of_3():
        if player_score == 2:
            winner = player_choice
        elif ai_score == 2:
            winner = ai_choice
        else:
            winner = None

        show_end_screen(winner)
        if winner == player_choice or winner == ai_choice:
            pygame.time.wait(2000)  # Wait before returning to menu if there is a final winner
        show_menu()  # Return to menu and reset scores
    else:
        pygame.time.wait(1000)
        if show_end_screen(winner):
            game_loop()  # Retry
        else:
            show_menu()  # Return to menu


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
    
# Start the game
show_menu()

