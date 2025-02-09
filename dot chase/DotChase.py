import pygame
import random
import sys

pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
DARK_GREEN_BG = (0, 70, 0)
PLAYER_YELLOW = (255, 250, 205)
ENEMY_BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN_BUTTON = (0, 200, 0)
RED_BUTTON = (200, 0, 0)

class DotChaseGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dot Chase Survival")
        self.clock = pygame.time.Clock()

        # Slightly larger enemy size
        self.object_size = 25
        
        # Start player at bottom
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT - self.object_size * 2
        self.player_speed = 5

        self.enemies = []
        self.enemy_speed = 3
        self.spawn_enemies()

        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def spawn_enemies(self):
        for _ in range(5):
            enemy = {
                'x': random.randint(0, SCREEN_WIDTH - self.object_size),
                # Start enemies from top
                'y': random.randint(0, SCREEN_HEIGHT // 3),
                'speed_x': random.choice([-1, 1]) * self.enemy_speed,
                'speed_y': random.choice([-1, 1]) * self.enemy_speed
            }
            self.enemies.append(enemy)

    def move_enemies(self):
        for enemy in self.enemies:
            enemy['x'] += enemy['speed_x']
            enemy['y'] += enemy['speed_y']

            # Bounce off screen edges
            if enemy['x'] <= 0 or enemy['x'] >= SCREEN_WIDTH - self.object_size:
                enemy['speed_x'] *= -1
            if enemy['y'] <= 0 or enemy['y'] >= SCREEN_HEIGHT - self.object_size:
                enemy['speed_y'] *= -1

    def check_collision(self):
        for enemy in self.enemies:
            distance = ((self.player_x - enemy['x']) ** 2 + 
                        (self.player_y - enemy['y']) ** 2) ** 0.5
            if distance < self.object_size:
                return True
        return False

    def draw_start_screen(self):
        self.screen.fill(DARK_GREEN_BG)
        
        start_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 50)
        pygame.draw.rect(self.screen, GREEN_BUTTON, start_button)
        
        start_text = self.font.render("START GAME", True, WHITE)
        text_rect = start_text.get_rect(center=start_button.center)
        self.screen.blit(start_text, text_rect)
        
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button.collidepoint(mouse_pos):
                        waiting = False

    def draw_game_over_screen(self):
        self.screen.fill(DARK_GREEN_BG)
        
        game_over_text = self.font.render(f"Game Over! Score: {self.score}", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        restart_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 50)
        pygame.draw.rect(self.screen, GREEN_BUTTON, restart_button)
        restart_text = self.font.render("RESTART", True, WHITE)
        text_rect = restart_text.get_rect(center=restart_button.center)
        self.screen.blit(restart_text, text_rect)
        
        exit_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 100, 200, 50)
        pygame.draw.rect(self.screen, RED_BUTTON, exit_button)
        exit_text = self.font.render("EXIT", True, WHITE)
        exit_rect = exit_text.get_rect(center=exit_button.center)
        self.screen.blit(exit_text, exit_rect)
        
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_button.collidepoint(mouse_pos):
                        return True
                    if exit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

    def run(self):
        self.draw_start_screen()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player_x -= self.player_speed
            if keys[pygame.K_RIGHT]:
                self.player_x += self.player_speed
            if keys[pygame.K_UP]:
                self.player_y -= self.player_speed
            if keys[pygame.K_DOWN]:
                self.player_y += self.player_speed

            # Keep player on screen
            self.player_x = max(0, min(self.player_x, SCREEN_WIDTH - self.object_size))
            self.player_y = max(0, min(self.player_y, SCREEN_HEIGHT - self.object_size))

            # Dark green background
            self.screen.fill(DARK_GREEN_BG)

            # Move and Draw Enemies
            self.move_enemies()
            for enemy in self.enemies:
                pygame.draw.rect(self.screen, ENEMY_BLACK, 
                                 (enemy['x'], enemy['y'], self.object_size, self.object_size))

            # Draw Player
            pygame.draw.circle(self.screen, PLAYER_YELLOW, 
                               (int(self.player_x), int(self.player_y)), 
                               self.object_size // 2)

            # Increment Score
            self.score += 1

            # Check Collision
            if self.check_collision():
                if self.draw_game_over_screen():
                    self.__init__()
                    self.run()
                    return

            # Update Display
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

# Run the game
if __name__ == "__main__":
    game = DotChaseGame()
    game.run()