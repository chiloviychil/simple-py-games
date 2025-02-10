import pygame
import random
import math
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
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game settings
PLAYER_RADIUS = 10
ENEMY_RADIUS = 8
PLAYER_SPEED = 5
ENEMY_SPEED = 3
INITIAL_ENEMIES = 3
ENEMY_SPAWN_TIME = 5  # New enemy every 5 seconds

class DotChase:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Dot Chase')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.reset_game()

    def reset_game(self):
        # Player initialization
        self.player_pos = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]
        self.player_velocity = [0, 0]
        
        # Enemy initialization
        self.enemies = []
        for _ in range(INITIAL_ENEMIES):
            self.spawn_enemy()
            
        # Game state
        self.game_over = False
        self.start_time = pygame.time.get_ticks()
        self.last_spawn_time = self.start_time
        self.score = 0
        self.high_score = self.load_high_score()

    def load_high_score(self):
        try:
            with open('dot_chase_high_score.txt', 'r') as f:
                return float(f.read())
        except:
            return 0.0

    def save_high_score(self):
        with open('dot_chase_high_score.txt', 'w') as f:
            f.write(str(self.high_score))

    def spawn_enemy(self):
        # Spawn enemy at random edge of screen
        side = random.randint(0, 3)
        if side == 0:  # Top
            x = random.randint(0, WINDOW_WIDTH)
            y = -ENEMY_RADIUS
        elif side == 1:  # Right
            x = WINDOW_WIDTH + ENEMY_RADIUS
            y = random.randint(0, WINDOW_HEIGHT)
        elif side == 2:  # Bottom
            x = random.randint(0, WINDOW_WIDTH)
            y = WINDOW_HEIGHT + ENEMY_RADIUS
        else:  # Left
            x = -ENEMY_RADIUS
            y = random.randint(0, WINDOW_HEIGHT)
            
        self.enemies.append([x, y])

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            if event.type == KEYDOWN and self.game_over:
                if event.key == K_r:
                    self.reset_game()

        if not self.game_over:
            # Smooth movement with acceleration
            keys = pygame.key.get_pressed()
            acceleration = 0.5
            friction = 0.1

            if keys[K_LEFT] or keys[K_a]:
                self.player_velocity[0] -= acceleration
            if keys[K_RIGHT] or keys[K_d]:
                self.player_velocity[0] += acceleration
            if keys[K_UP] or keys[K_w]:
                self.player_velocity[1] -= acceleration
            if keys[K_DOWN] or keys[K_s]:
                self.player_velocity[1] += acceleration

            # Apply friction
            self.player_velocity[0] *= (1 - friction)
            self.player_velocity[1] *= (1 - friction)

            # Limit speed
            speed = math.sqrt(self.player_velocity[0]**2 + self.player_velocity[1]**2)
            if speed > PLAYER_SPEED:
                self.player_velocity[0] = (self.player_velocity[0] / speed) * PLAYER_SPEED
                self.player_velocity[1] = (self.player_velocity[1] / speed) * PLAYER_SPEED

    def update(self):
        if self.game_over:
            return

        # Update player position
        self.player_pos[0] += self.player_velocity[0]
        self.player_pos[1] += self.player_velocity[1]

        # Keep player in bounds
        self.player_pos[0] = max(PLAYER_RADIUS, min(WINDOW_WIDTH - PLAYER_RADIUS, self.player_pos[0]))
        self.player_pos[1] = max(PLAYER_RADIUS, min(WINDOW_HEIGHT - PLAYER_RADIUS, self.player_pos[1]))

        # Update enemy positions
        for enemy in self.enemies:
            # Calculate direction to player
            dx = self.player_pos[0] - enemy[0]
            dy = self.player_pos[1] - enemy[1]
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance != 0:
                # Normalize and apply speed
                enemy[0] += (dx/distance) * ENEMY_SPEED
                enemy[1] += (dy/distance) * ENEMY_SPEED

            # Check collision
            if distance < PLAYER_RADIUS + ENEMY_RADIUS:
                self.game_over = True
                self.score = (pygame.time.get_ticks() - self.start_time) / 1000
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()

        # Spawn new enemy every ENEMY_SPAWN_TIME seconds
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > ENEMY_SPAWN_TIME * 1000:
            self.spawn_enemy()
            self.last_spawn_time = current_time

    def draw(self):
        self.screen.fill(BLACK)

        # Draw player
        pygame.draw.circle(self.screen, BLUE, 
                         (int(self.player_pos[0]), int(self.player_pos[1])), 
                         PLAYER_RADIUS)

        # Draw enemies
        for enemy in self.enemies:
            pygame.draw.circle(self.screen, RED, 
                             (int(enemy[0]), int(enemy[1])), 
                             ENEMY_RADIUS)

        # Draw survival time
        current_time = (pygame.time.get_ticks() - self.start_time) / 1000
        time_text = f'Time: {current_time:.1f}s'
        time_surface = self.font.render(time_text, True, WHITE)
        self.screen.blit(time_surface, (10, 10))

        # Draw high score
        high_score_text = f'Best: {self.high_score:.1f}s'
        high_score_surface = self.font.render(high_score_text, True, WHITE)
        self.screen.blit(high_score_surface, (10, 50))

        # Draw game over screen
        if self.game_over:
            game_over_text = f'Game Over! Survived: {self.score:.1f}s'
            game_over_surface = self.font.render(game_over_text, True, YELLOW)
            restart_text = 'Press R to restart'
            restart_surface = self.font.render(restart_text, True, YELLOW)
            
            text_rect = game_over_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            restart_rect = restart_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 40))
            
            self.screen.blit(game_over_surface, text_rect)
            self.screen.blit(restart_surface, restart_rect)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = DotChase()
    game.run()