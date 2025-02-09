import pygame
import random
import time
from pygame.locals import *

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
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class ReactionTester:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Reaction Time Tester')
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.main_font = pygame.font.Font(None, 48)
        self.info_font = pygame.font.Font(None, 36)
        
        self.reset_game()
        self.load_high_score()

    def load_high_score(self):
        try:
            with open('reaction_high_score.txt', 'r') as f:
                self.best_time = float(f.read())
        except:
            self.best_time = float('inf')

    def save_high_score(self):
        if self.reaction_time < self.best_time:
            self.best_time = self.reaction_time
            with open('reaction_high_score.txt', 'w') as f:
                f.write(str(self.best_time))

    def reset_game(self):
        self.state = "waiting"  # waiting, ready, testing, result
        self.start_time = 0
        self.reaction_time = 0
        self.times = []  # Store last 5 attempts
        self.color_options = [RED, GREEN, BLUE, YELLOW]
        self.current_color = BLACK
        self.false_start = False
        self.wait_start_time = time.time()
        self.wait_duration = random.uniform(2, 5)  # Random wait between 2-5 seconds

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.handle_space_press()
                elif event.key == K_r and self.state == "result":
                    self.reset_game()

    def handle_space_press(self):
        if self.state == "waiting":
            self.state = "ready"
            self.false_start = False
            self.wait_start_time = time.time()
            self.wait_duration = random.uniform(2, 5)
        
        elif self.state == "ready":
            # False start!
            self.false_start = True
            self.state = "result"
        
        elif self.state == "testing":
            # Calculate reaction time
            self.reaction_time = (time.time() - self.start_time) * 1000  # Convert to milliseconds
            self.times.append(self.reaction_time)
            if len(self.times) > 5:
                self.times.pop(0)
            self.save_high_score()
            self.state = "result"

    def update(self):
        if self.state == "ready":
            if time.time() - self.wait_start_time >= self.wait_duration:
                self.state = "testing"
                self.start_time = time.time()
                self.current_color = random.choice(self.color_options)

    def draw(self):
        if self.state == "waiting":
            self.screen.fill(BLACK)
            text = "Press SPACE to start"
            text_surface = self.title_font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(text_surface, text_rect)

            if self.times:  # Show previous results
                avg_time = sum(self.times) / len(self.times)
                avg_text = f"Average (last {len(self.times)}): {avg_time:.1f}ms"
                avg_surface = self.info_font.render(avg_text, True, WHITE)
                self.screen.blit(avg_surface, (10, 10))

                best_text = f"Best: {self.best_time:.1f}ms"
                best_surface = self.info_font.render(best_text, True, WHITE)
                self.screen.blit(best_surface, (10, 50))

        elif self.state == "ready":
            self.screen.fill(BLACK)
            text = "Wait for the color..."
            text_surface = self.title_font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(text_surface, text_rect)

        elif self.state == "testing":
            self.screen.fill(self.current_color)
            text = "PRESS SPACE!"
            text_surface = self.title_font.render(text, True, BLACK)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(text_surface, text_rect)

        elif self.state == "result":
            self.screen.fill(BLACK)
            
            if self.false_start:
                text = "False Start!"
                result_text = "Press R to try again"
            else:
                text = f"Reaction Time: {self.reaction_time:.1f}ms"
                if self.reaction_time == self.best_time:
                    result_text = "New Best Time! Press R to try again"
                else:
                    result_text = "Press R to try again"

            text_surface = self.title_font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(text_surface, text_rect)

            result_surface = self.main_font.render(result_text, True, WHITE)
            result_rect = result_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 60))
            self.screen.blit(result_surface, result_rect)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = ReactionTester()
    game.run()