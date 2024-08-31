import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
LINE_WIDTH = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Fonts
font = pygame.font.Font(None, 60)

# Game variables
board = [["", "", ""], ["", "", ""], ["", "", ""]]
player_turn = "X"
game_over = False

def draw_board():
    screen.fill(WHITE)
    # Draw vertical lines
    pygame.draw.line(screen, BLACK, (SCREEN_WIDTH//3, 0), (SCREEN_WIDTH//3, SCREEN_HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (2*SCREEN_WIDTH//3, 0), (2*SCREEN_WIDTH//3, SCREEN_HEIGHT), LINE_WIDTH)
    # Draw horizontal lines
    pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT//3), (SCREEN_WIDTH, SCREEN_HEIGHT//3), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (0, 2*SCREEN_HEIGHT//3), (SCREEN_WIDTH, 2*SCREEN_HEIGHT//3), LINE_WIDTH)
    # Draw the markers (X and O)
    for row in range(3):
        for col in range(3):
            if board[row][col] == "X":
                draw_x(row, col)
            elif board[row][col] == "O":
                draw_o(row, col)

def draw_x(row, col):
    start_x = col * SCREEN_WIDTH // 3 + 20
    start_y = row * SCREEN_HEIGHT // 3 + 20
    end_x = start_x + SCREEN_WIDTH // 3 - 40
    end_y = start_y + SCREEN_HEIGHT // 3 - 40
    pygame.draw.line(screen, RED, (start_x, start_y), (end_x, end_y), LINE_WIDTH)
    pygame.draw.line(screen, RED, (start_x, end_y), (end_x, start_y), LINE_WIDTH)

def draw_o(row, col):
    center_x = col * SCREEN_WIDTH // 3 + SCREEN_WIDTH // 6
    center_y = row * SCREEN_HEIGHT // 3 + SCREEN_HEIGHT // 6
    radius = SCREEN_WIDTH // 6 - 40
    pygame.draw.circle(screen, GREEN, (center_x, center_y), radius, LINE_WIDTH)

def check_winner():
    global game_over
    # Check rows, columns, and diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            pygame.draw.line(screen, BLACK, (0, i * SCREEN_HEIGHT // 3 + SCREEN_HEIGHT // 6),
                             (SCREEN_WIDTH, i * SCREEN_HEIGHT // 3 + SCREEN_HEIGHT // 6), LINE_WIDTH)
            game_over = True
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            pygame.draw.line(screen, BLACK, (i * SCREEN_WIDTH // 3 + SCREEN_WIDTH // 6, 0),
                             (i * SCREEN_WIDTH // 3 + SCREEN_WIDTH // 6, SCREEN_HEIGHT), LINE_WIDTH)
            game_over = True
            return board[0][i]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != "":
        pygame.draw.line(screen, BLACK, (20, 20), (SCREEN_WIDTH-20, SCREEN_HEIGHT-20), LINE_WIDTH)
        game_over = True
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        pygame.draw.line(screen, BLACK, (SCREEN_WIDTH-20, 20), (20, SCREEN_HEIGHT-20), LINE_WIDTH)
        game_over = True
        return board[0][2]
    
    # Check for a draw
    if all([board[row][col] != "" for row in range(3) for col in range(3)]):
        game_over = True
        return "Draw"
    
    return None

def game_loop():
    global player_turn, game_over
    draw_board()
    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked_row = mouse_y // (SCREEN_HEIGHT // 3)
                clicked_col = mouse_x // (SCREEN_WIDTH // 3)

                if board[clicked_row][clicked_col] == "":
                    board[clicked_row][clicked_col] = player_turn
                    if player_turn == "X":
                        player_turn = "O"
                    else:
                        player_turn = "X"
                    
                    draw_board()
                    winner = check_winner()
                    if winner:
                        show_winner(winner)

                    pygame.display.update()

def show_winner(winner):
    text = font.render(f"{winner} Wins!" if winner != "Draw" else "It's a Draw!", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)

def reset_game():
    global board, player_turn, game_over
    board = [["", "", ""], ["", "", ""], ["", "", ""]]
    player_turn = "X"
    game_over = False
    game_loop()

# Run the game loop
reset_game()
