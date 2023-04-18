import pygame
import sys
import random
import time


def draw_title_screen():
    # Draws all objects
    global difficulty, title_screen
    font = pygame.font.Font('freesansbold.ttf', 28)
    screen.fill('grey12')
    pygame.draw.rect(screen, (200, 200, 200), player)
    pygame.draw.rect(screen, (200, 200, 200), opponent)
    title = title_font.render('Pong', False, (200, 200, 200))
    screen.blit(title, (320, 100))
    easy_button = pygame.Rect(320, 300, 160, 60)
    hard_button = pygame.Rect(320, 380, 160, 60)
    pygame.draw.rect(screen, 'grey12', easy_button)
    pygame.draw.rect(screen, 'grey12', hard_button)
    easy = font.render('Easy', False, (200, 200, 200))
    hard = font.render('Hard', False, (200, 200, 200))
    text_len = easy.get_width()
    screen.blit(easy, (320 + int(160 / 2) - int(text_len / 2), 310))
    screen.blit(hard, (320 + int(160 / 2) - int(text_len / 2), 390))
    pos = pygame.mouse.get_pos()
    pygame.event.get()
    if easy_button.collidepoint(pos):
        if pygame.mouse.get_pressed()[0] == 1:
            difficulty = 'easy'
            title_screen = False
    elif hard_button.collidepoint(pos):
        if pygame.mouse.get_pressed()[0] == 1:
            difficulty = 'hard'
            title_screen = False


class Game:
    def __init__(self, screen_width=800, screen_height=600, player_speed=0, opponent_speed=6,
                 ball_speed_x=random.choice((5, -5)),
                 ball_speed_y=random.choice((5, -5)), player_score=0, opponent_score=0, x_coordinate=0, y_coordinate=0):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_speed = player_speed
        self.opponent_speed = opponent_speed
        self.ball_speed_x = ball_speed_x
        self.ball_speed_y = ball_speed_y
        self.player_score = player_score
        self.opponent_score = opponent_score
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

    def draw_screen(self):
        # Draws all objects
        screen.fill('grey12')
        pygame.draw.rect(screen, (200, 200, 200), player)
        pygame.draw.rect(screen, (200, 200, 200), opponent)
        pygame.draw.ellipse(screen, (200, 200, 200), ball)
        pygame.draw.aaline(screen, (200, 200, 200), (400, 0),
                           (400, self.screen_height))
        # Displays the score
        player_text = basic_font.render(f'{self.player_score}', False, (200, 200, 200))
        screen.blit(player_text, (435, 300))
        opponent_text = basic_font.render(f'{self.opponent_score}', False, (200, 200, 200))
        screen.blit(opponent_text, (350, 300))

    def opponent_ai(self):
        # Algorithm to make the opponent paddle follow the ball
        if opponent.top > ball.top:
            opponent.y -= self.opponent_speed
        if opponent.bottom < ball.bottom:
            opponent.y += self.opponent_speed

        # Collision system
        if opponent.top <= 0:
            opponent.top = 0
        if opponent.bottom >= self.screen_height:
            opponent.bottom = self.screen_height

    def opponent_ai2(self):
        self.opponent_speed = 4
        # Algorithm to make the opponent paddle follow the ball
        if opponent.top > ball.top:
            opponent.top -= self.opponent_speed
        if opponent.bottom < ball.bottom:
            opponent.bottom += self.opponent_speed

        # Collision system
        if opponent.top <= 0:
            opponent.top = 0
        if opponent.bottom >= self.screen_height:
            opponent.bottom = self.screen_height

    def player_movement(self):
        # Changes the position of the paddle
        player.y += game.player_speed

        # Collision system
        if player.top <= 0:
            player.top = 0
        if player.bottom >= self.screen_height:
            player.bottom = self.screen_height

    def ball_movement(self):
        # Changes the position of the ball
        ball.x += self.ball_speed_x
        ball.y += self.ball_speed_y

        # Bouncing and collision system
        if ball.top <= 0 or ball.bottom >= self.screen_height:
            self.x_coordinate = ball.x
            self.ball_speed_y *= -1

        if ball.colliderect(player) or ball.colliderect(opponent):
            self.x_coordinate = ball.x
            self.ball_speed_x *= -1

        # Scoring
        if ball.left <= 0:
            self.player_score += 1
            game.random_restart()

        if ball.right >= self.screen_width:
            self.opponent_score += 1
            game.random_restart()

    def random_restart(self):
        ball.x, ball.y = self.screen_width / 2 - 15, self.screen_height / 2 - 15
        player.x, player.y = game.screen_width - 20, game.screen_height / 2 - 60
        opponent.x, opponent.y = 10, game.screen_height / 2 - 60
        self.ball_speed_x = random.choice((5, -5))
        self.ball_speed_y = random.choice((5, -5))
        game.draw_screen()
        pygame.display.flip()
        time.sleep(1)


# Game setup
pygame.init()
clock = pygame.time.Clock()
game = Game()
pygame.display.set_caption('Pong')
screen = pygame.display.set_mode((game.screen_width, game.screen_height))
player = pygame.Rect(game.screen_width - 20, game.screen_height / 2 - 60, 10, 120)
opponent = pygame.Rect(10, game.screen_height / 2 - 60, 10, 120)
ball = pygame.Rect(game.screen_width / 2 - 15, game.screen_height / 2 - 15, 30, 30)
basic_font = pygame.font.Font('freesansbold.ttf', 32)
title_font = pygame.font.Font('freesansbold.ttf', 64)
difficulty = False


# Title screen
title_screen = True
while title_screen:
    draw_title_screen()
    pygame.display.flip()
time.sleep(1)


# Actual game
while True:
    # Control inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.player_speed = -6
            if event.key == pygame.K_DOWN:
                game.player_speed = 6
        if event.type == pygame.KEYUP:
            game.player_speed = 0

    # Updates window
    game.draw_screen()
    game.ball_movement()
    game.player_movement()
    if difficulty == 'hard':
        game.opponent_ai()
    elif difficulty == 'easy':
        game.opponent_ai2()
    pygame.display.flip()
    clock.tick(60)
    # Winning
    if game.opponent_score == 5:
        print('You lost!')
        break
    elif game.player_score == 5:
        print('You win!')
        break
