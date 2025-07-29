import pygame
import random


pygame.init()

# # screen
# screen_width = 800
# screen_height = 600
# screen = pygame.display.set_mode((screen_width, screen_height))

# # caption and icon
# pygame.display.set_caption("Ping Pong")
# icon = pygame.image.load("PingPong_Icon.png")
# pygame.display.set_icon(icon)

# colours
white = (255, 255, 255)
black = (0, 0, 0)

# ball
root2 = 1.414
# ball_radius = 20
# ball_x = screen_width/2 - ball_radius
# ball_y = screen_height/2 - ball_radius
# ball_speed_x = 1/(2*root2)
# ball_speed_y = 1/(2*root2)
# ball_speed = 1/2

# # paddle
# paddle_width = 120
# paddle_height = 20
# player_x = opponent_x = screen_width/2 - paddle_width/2
# player_y = screen_height - 50
# opponent_y = 50 - paddle_height
# player_speed = 0
# opponent_speed = 0

SPEED = 4000

class PongAI:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        # initialize display
        self.display = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Ping Pong")
        icon = pygame.image.load("PingPong_Icon.png")
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # intitialize game state
        self.paddle_width = 120
        self.paddle_height = 20
        self.player_x = self.screen_width/2 - self.paddle_width/2
        self.player_y = self.screen_height - 50
        self.opponent_x = self.screen_width/2 - self.paddle_width/2
        self.opponent_y = 50 - self.paddle_height
        self.player_speed = 0
        self.ball_radius = 20
        self.ball_x = self.screen_width/2 - self.ball_radius
        self.ball_y = self.screen_height/2 - self.ball_radius
        self.ball_speed = 1/2
        self.ball_speed_x = random.uniform(-1/(2*root2), 1/(2*root2))
        self.ball_speed_y = (self.ball_speed**2 - self.ball_speed_x**2) ** 0.5
        self.rally = 0
        self.frame_iteration = 0
        self.reward = 0

    def play_step(self, action):
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # move
        self.move(action)
        
        # check if game over
        # reward = 0
        game_over = False
        if self.ball_y >= self.screen_height - self.ball_radius:
            game_over = True
            self.reward = - abs(self.ball_x - (self.player_x + self.paddle_width/2))/40
            return self.reward, game_over, self.rally
        
        distance_to_ball = abs(self.ball_x - (self.player_x + self.paddle_width/2))
        self.reward += 1 - distance_to_ball/200
        
        # check ball collision with player paddle
        if self.player_y <= self.ball_y + self.ball_radius <= self.player_y + self.paddle_height:
            if self.player_x <= self.ball_x <= self.player_x + self.paddle_width:
                self.ball_y = self.player_y - self.ball_radius
                self.ball_speed_x = random.uniform(-1/(2*root2), 1/(2*root2))
                self.ball_speed_y = - ((self.ball_speed**2 - self.ball_speed_x**2) ** 0.5)
                self.rally += 1
                self.reward += 20

        # update all positions and ui
        self.update_pos()
        self.update_ui()
        self.clock.tick(SPEED)

        return self.reward, game_over, self.rally
    
    def move(self, action):
        # left
        if action == [1, 0, 0]:
            self.player_speed = -1
        # right
        elif action == [0, 0, 1]:
            self.player_speed = 1
        # stay
        elif action == [0, 1, 0]:
            self.player_speed = 0

    def update_pos(self):
        # wall collisions
        if self.ball_x <= 0 + self.ball_radius or self.ball_x >= self.screen_width - self.ball_radius:
            self.ball_speed_x *= -1
        
        # paddle constraints
        if self.player_x <= 0:
            self.player_x = 0
        if self.player_x >= self.screen_width - self.paddle_width:
            self.player_x = self.screen_width - self.paddle_width
        if self.opponent_x <= 0:
            self.opponent_x = 0
        if self.opponent_x >= self.screen_width - self.paddle_width:
            self.opponent_x = self.screen_width - self.paddle_width

        # opponent collision
        if self.opponent_y <= self.ball_y - self.ball_radius <= self.opponent_y + self.paddle_height:
            if self.opponent_x <= self.ball_x <= self.opponent_x + self.paddle_width:
                self.ball_y = self.opponent_y + self.paddle_height + self.ball_radius
                self.ball_speed_x = random.uniform(-1/(2*root2), 1/(2*root2))
                self.ball_speed_y = (self.ball_speed**2 - self.ball_speed_x**2) ** 0.5

        self.ball_speed_x = float(self.ball_speed_x)
        self.ball_speed_y = float(self.ball_speed_y)

        # update ball position
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y

        # update opponent position
        self.opponent_x = self.ball_x - self.paddle_width/2

        # update player position
        self.player_x += self.player_speed
    
    def update_ui(self):
        self.display.fill(black)

        pygame.draw.circle(self.display, white, (self.ball_x, self.ball_y), self.ball_radius)
        pygame.draw.rect(self.display, white, pygame.Rect(self.player_x, self.player_y, self.paddle_width, self.paddle_height))
        pygame.draw.rect(self.display, white, pygame.Rect(self.opponent_x, self.opponent_y, self.paddle_width, self.paddle_height))

        pygame.display.update()
        
    

# # game loop
# running = True
# while running:
#     screen.fill(black)

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_LEFT:
#                 player_speed = -1
#             if event.key == pygame.K_RIGHT:
#                 player_speed = 1
#         if event.type == pygame.KEYUP:
#             player_speed = 0

#     # ball control
#     if ball_x <= 0 + ball_radius or ball_x >= screen_width - ball_radius:
#         ball_speed_x *= -1
#     if ball_y >= screen_height - ball_radius:
#         ball_x, ball_y = screen_width/2 - ball_radius, screen_height/2 - ball_radius
#         ball_speed_x = (ball_speed**2 - ball_speed_y**2) ** 0.5 
#         ball_speed_y *= -1
#     if ball_y <= 0 + ball_radius:
#         ball_x, ball_y = screen_width/2 - ball_radius, screen_height/2 - ball_radius
#         ball_speed_x *= -1
#         ball_speed_y *= -1

#     # paddle control
#     if player_x <= 0:
#         player_x = 0
#     if player_x >= screen_width - paddle_width:
#         player_x = screen_width - paddle_width
#     if opponent_x <= 0:
#         opponent_x = 0
#     if opponent_x >= screen_width - paddle_width:
#         opponent_x = screen_width - paddle_width

#     # collisions
#     # player
#     if player_y <= ball_y + ball_radius <= player_y + paddle_height:
#         if player_x <= ball_x <= player_x + paddle_width:
#             ball_y = player_y - ball_radius
#             ball_speed_x = random.uniform(-1/(2*root2), 1/(2*root2))
#             ball_speed_y = - ((ball_speed**2 - ball_speed_x**2) ** 0.5)

#     # opponent
#     if opponent_y <= ball_y - ball_radius <= opponent_y + paddle_height:
#         if opponent_x <= ball_x <= opponent_x + paddle_width:
#             ball_y = opponent_y + paddle_height + ball_radius
#             ball_speed_x = random.uniform(-1/(2*root2), 1/(2*root2))
#             ball_speed_y = (ball_speed**2 - ball_speed_x**2) ** 0.5
    
#     ball_speed_x = float(ball_speed_x)
#     ball_speed_y = float(ball_speed_y)

#     # movement
#     ball_x += ball_speed_x
#     ball_y += ball_speed_y

#     opponent_x = ball_x - paddle_width/2

#     player_x += player_speed

#     # objects
#     pygame.draw.circle(screen, white, (ball_x, ball_y), ball_radius)
#     pygame.draw.rect(screen, white, pygame.Rect(player_x, player_y, paddle_width, paddle_height))
#     pygame.draw.rect(screen, white, pygame.Rect(opponent_x, opponent_y, paddle_width, paddle_height))

#     pygame.display.update()