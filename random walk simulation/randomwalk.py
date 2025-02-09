import pygame
import random
import colorsys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
PIXEL_SIZE = 2
SPEED = 1

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Random Walk Art")

class Walker:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.hue = 0
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.surface.fill((0, 0, 0))
    
    def get_color(self):
        # Convert HSV to RGB for smooth color transitions
        rgb = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
        return (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
    
    def move(self):
        # Random movement in 8 directions
        dx = random.choice([-SPEED, 0, SPEED])
        dy = random.choice([-SPEED, 0, SPEED])
        
        # Update position with boundary checking
        self.x = max(0, min(WIDTH - PIXEL_SIZE, self.x + dx))
        self.y = max(0, min(HEIGHT - PIXEL_SIZE, self.y + dy))
        
        # Update color (cycle through hue)
        self.hue = (self.hue + 0.001) % 1.0
        
        # Draw on surface
        pygame.draw.rect(self.surface, self.get_color(), 
                        (self.x, self.y, PIXEL_SIZE, PIXEL_SIZE))

def main():
    clock = pygame.time.Clock()
    walker = Walker()
    running = True
    paused = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_c:
                    # Clear screen
                    walker.surface.fill((0, 0, 0))
                elif event.key == pygame.K_r:
                    # Reset walker position
                    walker.x = WIDTH // 2
                    walker.y = HEIGHT // 2
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Move walker to click position
                walker.x, walker.y = pygame.mouse.get_pos()
        
        if not paused:
            # Update multiple times per frame for denser patterns
            for _ in range(50):
                walker.move()
        
        # Draw the accumulated pattern
        screen.blit(walker.surface, (0, 0))
        
        # Draw current walker position
        pygame.draw.circle(screen, (255, 255, 255), 
                         (int(walker.x), int(walker.y)), 2)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()