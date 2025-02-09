import pygame
import sys
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
COLORS = [(255, 99, 71), (255, 165, 0), (255, 215, 0), (50, 205, 50), (30, 144, 255)]

# Paddle settings
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_SPEED = 8

# Ball settings
BALL_SIZE = 10
BALL_SPEED = 5

# Brick settings
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLS = 8
BRICK_PADDING = 2

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Brick Breaker')
        self.clock = pygame.time.Clock()
        
        self.paddle = pygame.Rect(
            WINDOW_WIDTH // 2 - PADDLE_WIDTH // 2,
            WINDOW_HEIGHT - 40,
            PADDLE_WIDTH,
            PADDLE_HEIGHT
        )
        
        self.ball = pygame.Rect(
            WINDOW_WIDTH // 2 - BALL_SIZE // 2,
            WINDOW_HEIGHT - 60,
            BALL_SIZE,
            BALL_SIZE
        )
        
        self.ball_dx = BALL_SPEED
        self.ball_dy = -BALL_SPEED
        self.game_started = False
        
        # Create bricks
        self.bricks = []
        self.create_bricks()
        
        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def create_bricks(self):
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                brick = pygame.Rect(
                    col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING,
                    row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_PADDING + 50,
                    BRICK_WIDTH,
                    BRICK_HEIGHT
                )
                self.bricks.append({"rect": brick, "color": COLORS[row % len(COLORS)]})

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.paddle.left > 0:
            self.paddle.x -= PADDLE_SPEED
        if keys[K_RIGHT] and self.paddle.right < WINDOW_WIDTH:
            self.paddle.x += PADDLE_SPEED
        if keys[K_SPACE] and not self.game_started:
            self.game_started = True

    def update_ball(self):
        if not self.game_started:
            self.ball.centerx = self.paddle.centerx
            self.ball.bottom = self.paddle.top
            return

        self.ball.x += self.ball_dx
        self.ball.y += self.ball_dy

        # Wall collisions
        if self.ball.left <= 0 or self.ball.right >= WINDOW_WIDTH:
            self.ball_dx *= -1
        if self.ball.top <= 0:
            self.ball_dy *= -1

        # Paddle collision
        if self.ball.colliderect(self.paddle):
            self.ball_dy = -abs(self.ball_dy)  # Always bounce up
            # Add some randomness to the x direction
            self.ball_dx += random.uniform(-0.5, 0.5)
            # Keep the speed in check
            speed = (self.ball_dx ** 2 + self.ball_dy ** 2) ** 0.5
            self.ball_dx = self.ball_dx / speed * BALL_SPEED
            self.ball_dy = self.ball_dy / speed * BALL_SPEED

        # Brick collisions
        for brick in self.bricks[:]:
            if self.ball.colliderect(brick["rect"]):
                self.bricks.remove(brick)
                self.ball_dy *= -1
                self.score += 10

        # Ball out of bounds
        if self.ball.top >= WINDOW_HEIGHT:
            self.game_started = False
            self.ball_dx = BALL_SPEED
            self.ball_dy = -BALL_SPEED
            self.score = 0
            self.bricks.clear()
            self.create_bricks()

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw paddle
        pygame.draw.rect(self.screen, BLUE, self.paddle)
        
        # Draw ball
        pygame.draw.circle(self.screen, WHITE, self.ball.center, BALL_SIZE // 2)
        
        # Draw bricks
        for brick in self.bricks:
            pygame.draw.rect(self.screen, brick["color"], brick["rect"])
        
        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw start message
        if not self.game_started:
            start_text = self.font.render('Press SPACE to start', True, WHITE)
            text_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(start_text, text_rect)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.handle_input()
            self.update_ball()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()