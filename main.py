import pygame, sys, random

def draw_floor():
    SCREEN.blit(FLOOR, (floor_pos_x, 650))
    SCREEN.blit(FLOOR, (floor_pos_x + WIDTH, 650))

def create_pipes():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = PIPE.get_rect(midtop = (WIDTH+30, random_pipe_pos))
    top_pipe = PIPE.get_rect(midbottom = (WIDTH+30, random_pipe_pos - 200))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.x -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT:
            SCREEN.blit(PIPE, pipe)
        else:
            flip_pipe = pygame.transform.flip(PIPE, False, True)
            SCREEN.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top >= -50 and bird_rect.bottom >= 650:  
        return False
   
    return True

def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(f'Score: {int(score)}', True, (0, 0, 0))
        score_rect = score_surface.get_rect(center = (WIDTH//2, 50))
        SCREEN.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(
            f'Score: {int(score)}', True, (0, 0, 0))  #string , antialiasing, color
        score_rect = score_surface.get_rect(center = (WIDTH//2, 50))
        SCREEN.blit(score_surface, score_rect)

        high_score_surface = game_font.render(
            f'High Score: {int(high_score)}', True, (0, 0, 0))
        high_score_rect = high_score_surface.get_rect(center=(WIDTH//2, HEIGHT - 150))
        SCREEN.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency = 44100, size = 16, channels =1, buffer = 512)
pygame.font.init()
pygame.init()
WIDTH, HEIGHT = 400, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
game_font = pygame.font.SysFont("comicsans", 40)

# BASE
FLOOR_IMAGE_FILENAME = pygame.image.load("base.png")
FLOOR = pygame.transform.scale(FLOOR_IMAGE_FILENAME, (WIDTH, 50))
floor_pos_x = 0

# BIRD
BIRD_IMAGE_FILENAME = pygame.image.load("flappy2.png")
BIRD = pygame.transform.scale(BIRD_IMAGE_FILENAME, (50,40))
bird_rect = BIRD.get_rect(center = (100,200))  # get the rectangle around the image

# PIPE
PIPE_IMAGE_FILENAME = pygame.image.load("pipe-green.png")
PIPE = pygame.transform.scale(PIPE_IMAGE_FILENAME, (50,450))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)  # 1200 milliseconds or 1.2 seconds - spawn pipes after 1.2s
pipe_height = [250, 370, 400]

# GAME VARIABLES
gravity = 0.25
bird_vel = 0
game_active = True
score = 0
high_score = 0

# SOUNDS
death_sound = pygame.mixer.Sound("sfx_hit.wav")
score_sound = pygame.mixer.Sound("sfx_point.wav")
score_sound_countdown = 100

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_vel = 0
                bird_vel -= 5
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,200)
                bird_vel = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipes())

    
    SCREEN.fill((244,244,244))

    if game_active:
        # bird
        SCREEN.blit(BIRD, bird_rect)  # bird image, rectangle of the bird
        bird_vel += gravity
        bird_rect.centery += bird_vel
        game_active = check_collision(pipe_list)

        # pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display("main_game")
        score_sound_countdown -= 1
        if score_sound_countdown <= 1:
            score_sound.play()
            score_sound_countdown = 100
    else:
        high_score = update_score(score, high_score)
        score_display("game_over")

    # floor
    draw_floor()
    floor_pos_x -= 1
    if floor_pos_x <= -WIDTH:
        floor_pos_x = 0
    pygame.display.update()
