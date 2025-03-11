import pygame
import random
import time
import mariadb
import os

# Globální proměnné
user_id = 0
highest_score = 0
user_table_name = "snk_users"
score_table_name = "snk_scores"

# Databázové proměnné
connection = None
cursor = None

# Připojení k databázi
def databse_connect():
    try:
        conn = mariadb.connect(
            user="student16",
            password="spsnet",
            host="dbs.spskladno.cz",
            port=3306,
            database="vyuka16"
      )
        global cursor
        cursor = conn.cursor()
        cursor.execute(f'CREATE TABLE IF NOT EXISTS `{user_table_name}` (user_id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(255))')
        cursor.execute(f'CREATE TABLE IF NOT EXISTS `{score_table_name}` (user_id INT PRIMARY KEY, score INT, time INT, FOREIGN KEY (user_id) REFERENCES `{user_table_name}`(user_id) ON DELETE CASCADE ON UPDATE CASCADE)')
        conn.commit()
        global connection
        connection = conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")


# Získání cesty ke složce se skriptem
script_dir = os.path.dirname(os.path.abspath(__file__))

# Načtení obrázku
def load_image(image_name, size=None):
    path = os.path.join(script_dir, "sprites", image_name)
    img = pygame.image.load(path)
    if size:
        img = pygame.transform.scale(img, size)
    return img

# Hlavní loop hry
def game_loop(player_name, difficulty):
    pygame.init()
    WIDTH, HEIGHT = 600, 400
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Had")
    
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    
    speed_dict = {'lehka': 12, 'stredni': 15, 'tezka': 19}
    speed = speed_dict[difficulty]
    
    poison_apple_limit = 5
    clock = pygame.time.Clock()
    block_size = 25
    block_size2 = 15
    snake_pos = [[WIDTH // 2, HEIGHT // 2]] 
    snake_dir = 'RIGHT'

    apple_png = load_image("apple.png", (block_size, block_size))
    apple_png = pygame.transform.scale(apple_png, (block_size, block_size))
    poison_apple_png = load_image("poison_apple.png", (block_size, block_size))
    poison_apple_png = pygame.transform.scale(poison_apple_png, (block_size, block_size))

    snake_head = {
        'UP': load_image("head_up.png"),
        'DOWN': load_image("head_down.png"),
        'LEFT': load_image("head_left.png"),
        'RIGHT': load_image("head_right.png")
    }
    snake_body = {
        'HORIZONTAL': load_image("body_horizontal.png"),
        'VERTICAL': load_image("body_vertical.png")
    }
    snake_turn = {
        ('UP', 'LEFT'): load_image("turn_up_left.png"),
        ('UP', 'RIGHT'): load_image("turn_up_right.png"),
        ('DOWN', 'LEFT'): load_image("turn_down_left.png"),
        ('DOWN', 'RIGHT'): load_image("turn_down_right.png"),
        ('LEFT', 'UP'): load_image("turn_left_up.png"),
        ('LEFT', 'DOWN'): load_image("turn_left_down.png"),
        ('RIGHT', 'UP'): load_image("turn_right_up.png"),
        ('RIGHT', 'DOWN'): load_image("turn_right_down.png")
    }

    snake_tail = {
        'UP': load_image("tail_up.png"),
        'DOWN': load_image("tail_down.png"),
        'LEFT': load_image("tail_left.png"),
        'RIGHT': load_image("tail_right.png")
    }
    
    # Funkce pro vytvoření nového jablka
    def spawn_apple(existing_apples, existing_poisons):
        while True:
            pos = [random.randrange(0, WIDTH - 40, block_size), random.randrange(0, HEIGHT - 40, block_size)]
            if pos not in snake_pos and pos not in existing_apples and pos not in existing_poisons:
                return pos

    apple_pos = spawn_apple([], [])
    poison_apples = []
    score = 0
    start_time = time.time()
    
    running = True
    while running:
        SCREEN.fill(GREEN)
        for i, pos in enumerate(snake_pos):
            if i == 0:
                SCREEN.blit(snake_head[snake_dir], (pos[0], pos[1]))
            elif i == len(snake_pos) - 1:
                tail_dir = 'UP' if snake_pos[i - 1][1] > pos[1] else 'DOWN' if snake_pos[i - 1][1] < pos[1] else 'LEFT' if snake_pos[i - 1][0] > pos[0] else 'RIGHT'
                SCREEN.blit(snake_tail[tail_dir], (pos[0], pos[1]))
            else:
                prev_dir = 'UP' if snake_pos[i - 1][1] > pos[1] else 'DOWN' if snake_pos[i - 1][1] < pos[1] else 'LEFT' if snake_pos[i - 1][0] > pos[0] else 'RIGHT'
                next_dir = 'UP' if snake_pos[i + 1][1] > pos[1] else 'DOWN' if snake_pos[i + 1][1] < pos[1] else 'LEFT' if snake_pos[i + 1][0] > pos[0] else 'RIGHT'
                if (prev_dir, next_dir) in snake_turn:
                    SCREEN.blit(snake_turn[(prev_dir, next_dir)], (pos[0], pos[1]))
                else:
                    body_type = 'HORIZONTAL' if prev_dir in ['LEFT', 'RIGHT'] else 'VERTICAL'
                    SCREEN.blit(snake_body[body_type], (pos[0], pos[1]))
        
        for pos in poison_apples:
            SCREEN.blit(poison_apple_png, (pos[0], pos[1]))
        
        SCREEN.blit(apple_png, (apple_pos[0], apple_pos[1]))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if show_confirmation_dialog(SCREEN):
                    running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and snake_dir != 'DOWN':
                    snake_dir = 'UP'
                elif event.key == pygame.K_s and snake_dir != 'UP':
                    snake_dir = 'DOWN'
                elif event.key == pygame.K_a and snake_dir != 'RIGHT':
                    snake_dir = 'LEFT'
                elif event.key == pygame.K_d and snake_dir != 'LEFT':
                    snake_dir = 'RIGHT'
        
        if snake_dir == 'UP':
            snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1] - block_size2])
        elif snake_dir == 'DOWN':
            snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1] + block_size2])
        elif snake_dir == 'LEFT':
            snake_pos.insert(0, [snake_pos[0][0] - block_size2, snake_pos[0][1]])
        elif snake_dir == 'RIGHT':
            snake_pos.insert(0, [snake_pos[0][0] + block_size2, snake_pos[0][1]])
        
        if snake_pos[0] in snake_pos[1:] or snake_pos[0][0] < 0 or snake_pos[0][0] >= WIDTH or snake_pos[0][1] < 0 or snake_pos[0][1] >= HEIGHT:
            game_over(player_name, score, time.time() - start_time)
            return
        
        if pygame.Rect(snake_pos[0][0], snake_pos[0][1], block_size, block_size).colliderect(pygame.Rect(apple_pos[0], apple_pos[1], block_size, block_size)):
            score += 1
            apple_pos = spawn_apple([], poison_apples)
            if len(poison_apples) < poison_apple_limit:
                poison_apples.append(spawn_apple([apple_pos], poison_apples))
        else:
            snake_pos.pop()
        
        for pos in poison_apples:
            if pygame.Rect(snake_pos[0][0], snake_pos[0][1], block_size, block_size).colliderect(pygame.Rect(pos[0], pos[1], block_size, block_size)):
                poison_apples.remove(pos)
                if len(snake_pos) < 3:
                    game_over(player_name, score, time.time() - start_time)
                    return
                snake_pos = snake_pos[:-2]
        
        clock.tick(speed)

# Zobrazí dialogové okno s potvrzením o ukončení hry
def show_confirmation_dialog(SCREEN):
    font = pygame.font.SysFont("Arial", 30)
    dialog_surface = pygame.Surface((400, 200))
    dialog_surface.fill((255, 255, 255))
    pygame.draw.rect(dialog_surface, (0, 0, 0), (0, 0, 400, 200), 5)

    message = font.render("Ukončit hru?", True, (0, 0, 0))
    yes_text = font.render("Ano", True, (255, 0, 0))
    no_text = font.render("Ne", True, (255, 0, 0))

    SCREEN.blit(dialog_surface, (100, 100))
    SCREEN.blit(message, (120, 160))
    SCREEN.blit(yes_text, (150, 210))
    SCREEN.blit(no_text, (300, 210))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 150 <= mouse_x <= 200 and 210 <= mouse_y <= 240:
                    quit()
                    return True
                elif 300 <= mouse_x <= 350 and 210 <= mouse_y <= 240:
                    return False

        pygame.time.delay(10)

# Zobrazí obrazovku s konečným skóre
def game_over(player_name, score, elapsed_time):
    pygame.init()
    WIDTH, HEIGHT = 600, 400
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Over")
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    font = pygame.font.SysFont("arial", 30)
    
    SCREEN.fill(BLACK)
    text1 = font.render(f"Hráč: {player_name}", True, WHITE)
    text2 = font.render(f"Tvoje skóre: {score}", True, WHITE)
    text3 = font.render(f"Čas: {int(elapsed_time)} sekund", True, WHITE)
    text4 = font.render("Stiskni mezerník pro návrat do menu", True, WHITE)
    SCREEN.blit(text1, (WIDTH // 4, HEIGHT // 4))
    SCREEN.blit(text2, (WIDTH // 4, HEIGHT // 3))
    SCREEN.blit(text3, (WIDTH // 4, HEIGHT // 2))
    SCREEN.blit(text4, (WIDTH // 4, HEIGHT // 1.5))
    pygame.display.update()

    set_database_score(score, elapsed_time)
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
    main_menu()

# Zobrazí hlavní menu
def main_menu():
    pygame.init()
    WIDTH, HEIGHT = 600, 400
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Had - Hlavní menu")
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    font = pygame.font.SysFont("arial", 30)
    
    player_name = ""
    input_active = True
    while input_active:
        SCREEN.fill(BLACK)
        title = font.render("Zadej své jméno:", True, WHITE)
        SCREEN.blit(title, (WIDTH // 4, HEIGHT // 4))
        name_text = font.render(player_name, True, WHITE)
        SCREEN.blit(name_text, (WIDTH // 4, HEIGHT // 2))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if show_confirmation_dialog(SCREEN):
                    pygame.quit()
                    quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_name:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode
    

    save_latest_username(player_name)
    update_user_id(player_name)

    while True:
        SCREEN.fill(BLACK)
        title = font.render("Vyber obtížnost:", True, WHITE)
        SCREEN.blit(title, (WIDTH // 4, HEIGHT // 4))
        easy = font.render("1 - Lehká", True, WHITE)
        medium = font.render("2 - Střední", True, WHITE)
        hard = font.render("3 - Těžká", True, WHITE)
        SCREEN.blit(easy, (WIDTH // 4, HEIGHT // 2 - 40))
        SCREEN.blit(medium, (WIDTH // 4, HEIGHT // 2))
        SCREEN.blit(hard, (WIDTH // 4, HEIGHT // 2 + 40))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_loop(player_name, 'lehka')
                elif event.key == pygame.K_2:
                    game_loop(player_name, 'stredni')
                elif event.key == pygame.K_3:
                    game_loop(player_name, 'tezka')

# Získá uživatelské ID z databáze
def update_user_id(username):
    cursor.execute(f'SELECT user_id FROM `{user_table_name}` WHERE username = ?', (username,))
    connection.commit()
    result = cursor.fetchone()
    if result is None:
        # Uživatel neexistuje, vytvořit nového
        cursor.execute(f'INSERT INTO `{user_table_name}` (username) VALUES (?)', (username,))
        connection.commit()
        update_user_id(username)
    else:
        global userID
        userID = result[0]
        update_highest_score()

# Získá nejvyšší skóre uživatele z databáze
def update_highest_score():
    cursor.execute(f'SELECT score FROM `{score_table_name}` WHERE user_id = ?', (userID,))
    connection.commit()
    score = cursor.fetchone()
    if score is not None:
        global highest_score
        highest_score = score[0]

# Uloží poslední použité uživatelské jméno do souboru
def save_latest_username(username):
    with open("latest_username.txt", "w") as file:
        file.write(f"{username}")

# Získá poslední použité uživatelské jméno ze souboru
# def get_latest_username():
#     try:
#         with open("latest_username.txt", "r") as file:
#             return file.readline()
#     except FileNotFoundError:
#         return ""

# Nastaví skóre uživatele v databázi
def set_database_score(score, time):
    if (score < highest_score):
        return
    cursor.execute(f'INSERT INTO `{score_table_name}` (user_id, score, time) VALUES (?, ?, ?) ON DUPLICATE KEY UPDATE score = ?', (userID, score, time, score))
    connection.commit()

# Spustit hru
# 1. připojit se k databázi
# 2. zobrazit hlavní menu
databse_connect()
main_menu()
