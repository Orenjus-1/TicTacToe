
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
SMALL_IMG = theme_path + "small.png"

# Load images
background = pygame.image.load(BACKGROUND_IMG)
grid_img = pygame.image.load(GRID_IMG)
x_img = pygame.image.load(X_IMG)
o_img = pygame.image.load(O_IMG)
button_img = pygame.image.load(BUTTON_IMG)
small_img = pygame.image.load(SMALL_IMG)

# Scale images
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
grid_img = pygame.transform.scale(grid_img, (GRID_SIZE * 3, GRID_SIZE * 3))
x_img = pygame.transform.scale(x_img, (GRID_SIZE - 20, GRID_SIZE - 20))
o_img = pygame.transform.scale(o_img, (GRID_SIZE - 20, GRID_SIZE - 20))
button_img = pygame.transform.scale(button_img, (200, 50))
small_img = pygame.transform.scale(small_img, (GRID_SIZE - 20, GRID_SIZE - 20))

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
    # Basic AI logic from the second code
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

def reset_board():
    global board, player_turn, game_over
    board = [["", "", ""], ["", "", ""], ["", "", ""]]
    player_turn = True
    game_over = False

def display_message(message):
    screen.blit(background, (0, 0))
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)

def show_menu():
    menu_running = True
    while menu_running:
        screen.blit(background, (0, 0))
        title_text = font.render("Tic-Tac-Toe", True, BLACK)
        single_player_text = font.render("Single Player", True, BLACK)
        multiplayer_text = font.render("Multiplayer", True, BLACK)
        settings_text = font.render("Settings", True, BLACK)
        exit_text = font.render("Exit", True, BLACK)

        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        single_player_rect = single_player_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        multiplayer_rect = multiplayer_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        settings_rect = settings_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))

        screen.blit(title_text, title_rect)
        screen.blit(single_player_text, single_player_rect)
        screen.blit(multiplayer_text, multiplayer_rect)
        screen.blit(settings_text, settings_rect)
        screen.blit(exit_text, exit_rect)

        pygame.draw.rect(screen, WHITE, single_player_rect.inflate(20, 20))
        pygame.draw.rect(screen, WHITE, multiplayer_rect.inflate(20, 20))
        pygame.draw.rect(screen, WHITE, settings_rect.inflate(20, 20))
        pygame.draw.rect(screen, WHITE, exit_rect.inflate(20, 20))

        screen.blit(button_img, single_player_rect.topleft)
        screen.blit(button_img, multiplayer_rect.topleft)
        screen.blit(button_img, settings_rect.topleft)
        screen.blit(button_img, exit_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if single_player_rect.collidepoint(event.pos):
                    click_sound.play()
                    menu_running = False
                    choose_player_mode(single_player=True)
                elif multiplayer_rect.collidepoint(event.pos):
                    click_sound.play()
                    menu_running = False
                    choose_player_mode(single_player=False)
                elif settings_rect.collidepoint(event.pos):
                    click_sound.play()
                    show_settings()
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def choose_player_mode(single_player=True):
    choosing = True
    while choosing:
        screen.blit(background, (0, 0))
        choose_text = font.render("Choose CROSS or CHECK", True, BLACK)
        x_text = font.render("X", True, RED)
        o_text = font.render("/", True, GREEN)

        choose_rect = choose_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        x_rect = x_text.get_rect(center=(SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2))
        o_rect = o_text.get_rect(center=(SCREEN_WIDTH//2 + 120, SCREEN_HEIGHT//2))

        screen.blit(small_img, x_rect.inflate(200, 135))
        screen.blit(small_img, o_rect.inflate(100, 135))

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

    play_game(single_player)

def play_game(single_player=True):
    global game_over, round_count, player_score, ai_score, player_turn  # Declare player_turn as global
    reset_board()
    while not game_over:
        draw_board()
        pygame.display.update()

        if player_turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    clicked_row = mouseY // GRID_SIZE
                    clicked_col = mouseX // GRID_SIZE

                    if board[clicked_row][clicked_col] == "" and not game_over:
                        place_sound.play()
                        board[clicked_row][clicked_col] = player_choice
                        winner = check_winner()
                        if winner:
                            game_over = True
                            if winner == player_choice:
                                player_score += 1
                                display_message(f"Player {player_choice} Wins!")
                            else:
                                ai_score += 1
                                display_message(f"Player {winner} Wins!")
                            if (player_score >= 2 or ai_score >= 2) and round_count < 3:
                                display_message(f"Game Over! Final Score - Player X: {player_score}, Player O: {ai_score}")
                                pygame.time.wait(2000)
                                show_end_screen()
                                return
                            elif round_count < 3:
                                round_count += 1
                                reset_board()
                                continue
                        elif not any("" in row for row in board):
                            game_over = True
                            display_message("It's a Draw!")
                        else:
                            player_turn = False
        else:
            if single_player:
                time.sleep(0.5)
                ai_move = ai_best_move()
                if ai_move:
                    board[ai_move[0]][ai_move[1]] = ai_choice
                    winner = check_winner()
                    if winner:
                        game_over = True
                        ai_score += 1
                        display_message(f"AI Wins!")
                        if (player_score >= 2 or ai_score >= 2) and round_count < 3:
                            display_message(f"Game Over! Final Score - Player X: {player_score}, Player O: {ai_score}")
                            pygame.time.wait(2000)
                            show_end_screen()
                            return
                        elif round_count < 3:
                            round_count += 1
                            reset_board()
                            continue
                    elif not any("" in row for row in board):
                        game_over = True
                        display_message("It's a Draw!")
                    else:
                        player_turn = True
            else:
                # Multiplayer mode
                time.sleep(0.1)  # Short delay to ensure smooth turn transitions
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouseX, mouseY = event.pos
                        clicked_row = mouseY // GRID_SIZE
                        clicked_col = mouseX // GRID_SIZE

                        if board[clicked_row][clicked_col] == "" and not game_over:
                            place_sound.play()
                            board[clicked_row][clicked_col] = player_choice
                            winner = check_winner()
                            if winner:
                                game_over = True
                                if winner == player_choice:
                                    player_score += 1
                                    display_message(f"Player {player_choice} Wins!")
                                else:
                                    ai_score += 1
                                    display_message(f"Player {winner} Wins!")
                                if (player_score >= 2 or ai_score >= 2) and round_count < 3:
                                    display_message(f"Game Over! Final Score - Player X: {player_score}, Player O: {ai_score}")
                                    pygame.time.wait(2000)
                                    show_end_screen()
                                    return
                                elif round_count < 3:
                                    round_count += 1
                                    reset_board()
                                    continue
                            elif not any("" in row for row in board):
                                game_over = True
                                display_message("It's a Draw!")
                            else:
                                player_turn = not player_turn

    show_menu()

def show_end_screen():
    end_screen_running = True
    while end_screen_running:
        screen.blit(background, (0, 0))
        end_message = "Game Over! Winner is: "
        winner = "Player X" if player_score >= 2 else "Player O"
        end_message += winner
        end_text = font.render(end_message, True, BLACK)
        end_rect = end_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(end_text, end_rect)
        
        restart_text = font.render("Restart", True, BLACK)
        menu_text = font.render("Menu", True, BLACK)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))

        screen.blit(restart_text, restart_rect)
        screen.blit(menu_text, menu_rect)

        pygame.draw.rect(screen, WHITE, restart_rect.inflate(20, 20))
        pygame.draw.rect(screen, WHITE, menu_rect.inflate(20, 20))

        screen.blit(button_img, restart_rect.topleft)
        screen.blit(button_img, menu_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    click_sound.play()
                    end_screen_running = False
                    main()
                elif menu_rect.collidepoint(event.pos):
                    click_sound.play()
                    end_screen_running = False
                    show_menu()

        pygame.display.update()

def show_settings():
    settings_running = True
    while settings_running:
        screen.blit(background, (0, 0))
        theme_text = font.render("Change Theme", True, BLACK)
        default_theme_text = font.render("Default", True, BLACK)
        classic_theme_text = font.render("Classic", True, BLACK)
        retro_theme_text = font.render("Retro", True, BLACK)
        back_text = font.render("Back", True, BLACK)

        theme_rect = theme_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        default_rect = default_theme_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        classic_rect = classic_theme_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        retro_rect = retro_theme_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))

        screen.blit(theme_text, theme_rect)
        screen.blit(default_theme_text, default_rect)
        screen.blit(classic_theme_text, classic_rect)
        screen.blit(retro_theme_text, retro_rect)
        screen.blit(back_text, back_rect)

        screen.blit(button_img, default_rect.topleft)
        screen.blit(button_img, classic_rect.topleft)
        screen.blit(button_img, retro_rect.topleft)
        screen.blit(button_img, back_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if default_rect.collidepoint(event.pos):
                    click_sound.play()
                    change_theme("default")
                elif classic_rect.collidepoint(event.pos):
                    click_sound.play()
                    change_theme("classic")
                elif retro_rect.collidepoint(event.pos):
                    click_sound.play()
                    change_theme("retro")
                elif back_rect.collidepoint(event.pos):
                    click_sound.play()
                    settings_running = False

        pygame.display.update()

def change_theme(theme):
    global selected_theme, theme_path, background, grid_img, x_img, o_img
    selected_theme = theme
    theme_path = themes[selected_theme]
    BACKGROUND_IMG = theme_path + "background.png"
    GRID_IMG = theme_path + "grid.png"
    X_IMG = theme_path + "x.png"
    O_IMG = theme_path + "o.png"
    BUTTON_IMG = theme_path + "button.png"

    background = pygame.image.load(BACKGROUND_IMG)
    grid_img = pygame.image.load(GRID_IMG)
    x_img = pygame.image.load(X_IMG)
    o_img = pygame.image.load(O_IMG)
    button_img = pygame.image.load(BUTTON_IMG)

    # Scale images again with the new theme
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    grid_img = pygame.transform.scale(grid_img, (GRID_SIZE * 3, GRID_SIZE * 3))
    x_img = pygame.transform.scale(x_img, (GRID_SIZE - 20, GRID_SIZE - 20))
    o_img = pygame.transform.scale(o_img, (GRID_SIZE - 20, GRID_SIZE - 20))
    button_img = pygame.transform.scale(button_img, (200, 50))

    # Refresh the display to show new theme
    screen.blit(background, (0, 0))
    pygame.display.update()

def main():
    show_menu()

if __name__ == "__main__":
    main()
