
import pygame
import sys
import time

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

# Load images
background = pygame.image.load(BACKGROUND_IMG)
grid_img = pygame.image.load(GRID_IMG)
x_img = pygame.image.load(X_IMG)
o_img = pygame.image.load(O_IMG)

# Scale images
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
grid_img = pygame.transform.scale(grid_img, (GRID_SIZE * 3, GRID_SIZE * 3))
x_img = pygame.transform.scale(x_img, (GRID_SIZE - 20, GRID_SIZE - 20))
o_img = pygame.transform.scale(o_img, (GRID_SIZE - 20, GRID_SIZE - 20))

# Load sounds
click_sound = pygame.mixer.Sound("sounds/click.wav")
place_sound = pygame.mixer.Sound("sounds/place.wav")
win_sound = pygame.mixer.Sound("sounds/win.wav")

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Fonts
font = pygame.font.Font(None, 75)

# Game variables
board = [["", "", ""], ["", "", ""], ["", "", ""]]
player_turn = True
game_over = False
player_choice = "X"
ai_choice = "O"
player_score = 0
ai_score = 0
round_count = 1

def draw_board():
    screen.blit(background, (0, 0))
    screen.blit(grid_img, (0, 0))

    for row in range(3):
        for col in range(3):
            if board[row][col] == "X":
                screen.blit(x_img, (col * GRID_SIZE + 10, row * GRID_SIZE + 10))
            elif board[row][col] == "O":
                screen.blit(o_img, (col * GRID_SIZE + 10, row * GRID_SIZE + 10))

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
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                board[row][col] = ai_choice
                if check_winner() == ai_choice:
                    return row, col
                board[row][col] = ""

    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                board[row][col] = player_choice
                if check_winner() == player_choice:
                    board[row][col] = ai_choice
                    return row, col
                board[row][col] = ""

    if board[1][1] == "":
        return 1, 1

    for row, col in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        if board[row][col] == "":
            return row, col

    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                return row, col
    return None

def reset_board():
    global board, player_turn, game_over
    board = [["", "", ""], ["", "", ""], ["", "", ""]]
    player_turn = True
    game_over = False

def display_message(message):
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)

def draw_button(text, x, y, width, height):
    pygame.draw.rect(screen, (0, 128, 255), (x, y, width, height))  # Button background
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + width//2, y + height//2))
    screen.blit(text_surf, text_rect)

def show_menu():
    background_menu = pygame.image.load(BACKGROUND_IMG)  # Load the menu background image
    background_menu = pygame.transform.scale(background_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to screen size
    
    menu_running = True
    while menu_running:
        screen.blit(background_menu, (0, 0))  # Draw the background image

        draw_button("Single Player", 100, 200, 400, 60)
        draw_button("Multiplayer", 100, 300, 400, 60)
        draw_button("Settings", 100, 400, 400, 60)
        draw_button("Exit", 100, 500, 400, 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 150 <= event.pos[0] <= 450:
                    if 200 <= event.pos[1] <= 250:
                        click_sound.play()
                        menu_running = False
                        choose_player_mode(single_player=True)
                    elif 300 <= event.pos[1] <= 350:
                        click_sound.play()
                        menu_running = False
                        choose_player_mode(single_player=False)
                    elif 400 <= event.pos[1] <= 450:
                        click_sound.play()
                        show_settings()
                    elif 500 <= event.pos[1] <= 550:
                        pygame.quit()
                        sys.exit()

        pygame.display.update()

def choose_player_mode(single_player=True):
    choosing = True
    while choosing:
        screen.fill(WHITE)
        choose_text = font.render("Choose X or O", True, BLACK)
        x_text = font.render("X", True, RED)
        o_text = font.render("O", True, BLUE)

        choose_rect = choose_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        x_rect = x_text.get_rect(center=(SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2))
        o_rect = o_text.get_rect(center=(SCREEN_WIDTH//2 + 50, SCREEN_HEIGHT//2))

        screen.blit(choose_text, choose_rect)
        screen.blit(x_text, x_rect)
        screen.blit(o_text, o_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if x_rect.collidepoint(event.pos):
                    click_sound.play()
                    global player_choice, ai_choice, player_turn
                    player_choice = "X"
                    ai_choice = "O"
                    player_turn = True
                    choosing = False
                elif o_rect.collidepoint(event.pos):
                    click_sound.play()
                    player_choice = "O"
                    ai_choice = "X"
                    player_turn = False
                    choosing = False

        pygame.display.update()

    reset_board()
    
    main_game(single_player)

def main_game(single_player=True):
    global player_turn, game_over
    game_running = True

    while game_running:
        draw_board()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX, mouseY = event.pos
                clicked_row = mouseY // GRID_SIZE
                clicked_col = mouseX // GRID_SIZE

                if board[clicked_row][clicked_col] == "":
                    if player_turn:
                        board[clicked_row][clicked_col] = player_choice
                        place_sound.play()
                        player_turn = False
                        if check_winner():
                            win_sound.play()
                            game_over = True
                            display_message(f"{player_choice} Wins!")
                        elif all([all(row) for row in board]):
                            display_message("It's a Tie!")
                            game_over = True
                    elif not single_player and not player_turn:
                        board[clicked_row][clicked_col] = ai_choice
                        place_sound.play()
                        player_turn = True
                        if check_winner():
                            win_sound.play()
                            game_over = True
                            display_message(f"{ai_choice} Wins!")
                        elif all([all(row) for row in board]):
                            display_message("It's a Tie!")
                            game_over = True

        if single_player and not player_turn and not game_over:
            ai_move = ai_best_move()
            if ai_move:
                board[ai_move[0]][ai_move[1]] = ai_choice
                place_sound.play()
                player_turn = True
                if check_winner():
                    win_sound.play()
                    game_over = True
                    display_message(f"{ai_choice} Wins!")
                elif all([all(row) for row in board]):
                    display_message("It's a Tie!")
                    game_over = True

        pygame.display.update()

    time.sleep(2)
    reset_board()

def show_settings():
    # Placeholder for settings functionality
    pass

show_menu()
