import pygame
import time
import random

# Inicializa o Pygame
pygame.init()

# Definindo as cores
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
yellow = (255, 255, 0)  # Cor da comida
red_obstacle = (255, 0, 0)  # Cor dos obstáculos

# Definindo as dimensões da tela
dis_width = 800
dis_height = 600

# Cria a tela do jogo
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Jogo da Cobrinha')

# Configura o relógio do jogo
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

# Fonte para o texto
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)
timer_font = pygame.font.SysFont(None, 30)

def mensagem(msg, cor):
    mesg = font_style.render(msg, True, cor)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def score(score):
    value = score_font.render("Pontuação: " + str(score), True, black)
    dis.blit(value, [0, 0])

def timer(time_left):
    value = timer_font.render("Tempo: " + str(int(time_left)), True, black)
    dis.blit(value, [dis_width - 150, 0])

def nosso_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def criar_obstaculos(num_obstaculos):
    obstaculos = []
    for _ in range(num_obstaculos):
        obst_largura = random.randint(3, 6) * snake_block
        obst_altura = random.randint(3, 6) * snake_block
        obst_x = round(random.randrange(0, dis_width - obst_largura) / snake_block) * snake_block
        obst_y = round(random.randrange(0, dis_height - obst_altura) / snake_block) * snake_block
        obstaculos.append([obst_x, obst_y, obst_largura, obst_altura])
    return obstaculos

def desenhar_obstaculos(obstaculos):
    for obst in obstaculos:
        pygame.draw.rect(dis, red_obstacle, [obst[0], obst[1], obst[2], obst[3]])

def verificar_colisao_obstaculo(x1, y1, obstaculos):
    for obst in obstaculos:
        if obst[0] <= x1 < obst[0] + obst[2] and obst[1] <= y1 < obst[1] + obst[3]:
            return True
    return False

def gameLoop():
    fase = 1
    tempo_fase = 30  # Tempo de cada fase em segundos
    num_obstaculos = 3  # Número inicial de obstáculos

    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    obstaculos = criar_obstaculos(num_obstaculos)
    tempo_inicio = time.time()
    score_count = 0

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            mensagem("Você Perdeu! Pressione C para continuar ou Q para sair", red)
            score(score_count)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, yellow, [foodx, foody, snake_block, snake_block])  # Cor da comida
        desenhar_obstaculos(obstaculos)
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        nosso_snake(snake_block, snake_List)
        score(score_count)

        tempo_decorrido = time.time() - tempo_inicio
        tempo_restante = max(0, tempo_fase - int(tempo_decorrido))
        timer(tempo_restante)

        if tempo_restante == 0:
            fase += 1
            tempo_fase = max(10, tempo_fase - 5)  # Reduz o tempo de cada fase
            num_obstaculos += 2  # Adiciona mais obstáculos
            obstaculos = criar_obstaculos(num_obstaculos)
            tempo_inicio = time.time()

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score_count += 1

        if verificar_colisao_obstaculo(x1, y1, obstaculos):
            game_close = True

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
