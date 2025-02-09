import pygame
import sys
import random
from pygame.locals import *
from collections import deque

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        
        self.reset_game()
        self.font = pygame.font.Font(None, 36)

    def reset_game(self):
        # Initialize snake in the middle of the screen
        self.snake = deque([(GRID_WIDTH // 2, GRID_HEIGHT // 2)])
        self.direction = (1, 0)  # Start moving right
        self.new_direction = self.direction
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.game_started = False

    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1),
                   random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food

    def handle_input(self):
        # Store the current direction to check for invalid moves
        current_direction = self.direction

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                if not self.game_started and event.key == K_SPACE:
                    self.game_started = True
                elif self.game_over and event.key == K_r:
                    self.reset_game()
                elif event.key == K_UP and current_direction[1] != 1:
                    self.new_direction = (0, -1)
                elif event.key == K_DOWN and current_direction[1] != -1:
                    self.new_direction = (0, 1)
                elif event.key == K_LEFT and current_direction[0] != 1:
                    self.new_direction = (-1, 0)
                elif event.key == K_RIGHT and current_direction[0] != -1:
                    self.new_direction = (1, 0)

    def update(self):
        if not self.game_started or self.game_over:
            return

        # Update direction
        self.direction = self.new_direction

        # Get the current head position
        head_x, head_y = self.snake[0]
        
        # Calculate new head position
        new_head = (
            (head_x + self.direction[0]) % GRID_WIDTH,
            (head_y + self.direction[1]) % GRID_HEIGHT
        )

        # Check for collision with self
        if new_head in self.snake:
            self.game_over = True
            return

        # Add new head
        self.snake.appendleft(new_head)

        # Check if food is eaten
        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (WINDOW_WIDTH, y))

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()

        # Draw snake
        for i, segment in enumerate(self.snake):
            color = GREEN if i == 0 else DARK_GREEN  # Head is lighter green
            pygame.draw.rect(self.screen, color, (
                segment[0] * GRID_SIZE,
                segment[1] * GRID_SIZE,
                GRID_SIZE - 1,
                GRID_SIZE - 1
            ))

        # Draw food
        pygame.draw.rect(self.screen, RED, (
            self.food[0] * GRID_SIZE,
            self.food[1] * GRID_SIZE,
            GRID_SIZE - 1,
            GRID_SIZE - 1
        ))

        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Draw start or game over message
        if not self.game_started:
            start_text = self.font.render('Press SPACE to start', True, WHITE)
            text_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(start_text, text_rect)
        elif self.game_over:
            game_over_text = self.font.render('Game Over! Press R to restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = SnakeGame()
    game.run()