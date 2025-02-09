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

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = random.uniform(-5, 5)
        self.dy = random.uniform(-5, 5)
        self.color = self.random_color()
        self.mass = radius * radius  # Mass proportional to area

    def random_color(self):
        return (random.randint(50, 255),
                random.randint(50, 255),
                random.randint(50, 255))

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Add slight gravity effect
        self.dy += 0.1

        # Add slight energy loss
        self.dx *= 0.999
        self.dy *= 0.999

    def check_wall_collision(self):
        collision = False
        
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.dx = abs(self.dx)
            collision = True
        elif self.x + self.radius >= WINDOW_WIDTH:
            self.x = WINDOW_WIDTH - self.radius
            self.dx = -abs(self.dx)
            collision = True

        if self.y - self.radius <= 0:
            self.y = self.radius
            self.dy = abs(self.dy)
            collision = True
        elif self.y + self.radius >= WINDOW_HEIGHT:
            self.y = WINDOW_HEIGHT - self.radius
            self.dy = -abs(self.dy)
            collision = True

        if collision:
            self.color = self.random_color()

class BallSimulation:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Bouncing Balls Simulation')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.balls = []
        self.spawn_initial_balls()
        
        # Trail effect
        self.previous_frames = []
        self.max_trail_length = 5

    def spawn_initial_balls(self):
        for _ in range(10):
            while True:
                radius = random.randint(10, 30)
                x = random.randint(radius, WINDOW_WIDTH - radius)
                y = random.randint(radius, WINDOW_HEIGHT - radius)
                
                # Check if new ball overlaps with existing balls
                overlap = False
                for ball in self.balls:
                    dx = x - ball.x
                    dy = y - ball.y
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance < radius + ball.radius:
                        overlap = True
                        break
                
                if not overlap:
                    self.balls.append(Ball(x, y, radius))
                    break

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            if event.type == MOUSEBUTTONDOWN:
                # Add new ball at mouse position
                x, y = pygame.mouse.get_pos()
                radius = random.randint(10, 30)
                self.balls.append(Ball(x, y, radius))

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    # Clear all balls
                    self.balls.clear()
                elif event.key == K_r:
                    # Reset simulation
                    self.balls.clear()
                    self.spawn_initial_balls()

    def check_ball_collision(self, b1, b2):
        dx = b2.x - b1.x
        dy = b2.y - b1.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < b1.radius + b2.radius:
            # Collision detected - calculate new velocities
            # Normal vector
            nx = dx / distance
            ny = dy / distance
            
            # Relative velocity
            rx = b2.dx - b1.dx
            ry = b2.dy - b1.dy
            
            # Velocity along normal
            velocity_along_normal = rx * nx + ry * ny
            
            # Don't collide if balls are moving apart
            if velocity_along_normal > 0:
                return
            
            # Collision response
            restitution = 0.9  # Bouncing factor
            
            # Calculate impulse
            j = -(1 + restitution) * velocity_along_normal
            j /= 1/b1.mass + 1/b2.mass
            
            # Apply impulse
            b1.dx -= (j * nx) / b1.mass
            b1.dy -= (j * ny) / b1.mass
            b2.dx += (j * nx) / b2.mass
            b2.dy += (j * ny) / b2.mass
            
            # Change colors
            b1.color = b1.random_color()
            b2.color = b2.random_color()
            
            # Separate balls to prevent sticking
            overlap = (b1.radius + b2.radius - distance) / 2
            b1.x -= overlap * nx
            b1.y -= overlap * ny
            b2.x += overlap * nx
            b2.y += overlap * ny

    def update(self):
        # Store current frame for trail effect
        current_frame = [(ball.x, ball.y, ball.radius, ball.color) for ball in self.balls]
        self.previous_frames.append(current_frame)
        if len(self.previous_frames) > self.max_trail_length:
            self.previous_frames.pop(0)

        # Update ball positions
        for ball in self.balls:
            ball.move()
            ball.check_wall_collision()

        # Check ball collisions
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                self.check_ball_collision(self.balls[i], self.balls[j])

    def draw(self):
        self.screen.fill(BLACK)

        # Draw trails
        for i, frame in enumerate(self.previous_frames[:-1]):
            alpha = (i + 1) * (255 // len(self.previous_frames))
            surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            for x, y, radius, color in frame:
                pygame.draw.circle(surface, (*color, alpha), (int(x), int(y)), radius)
            self.screen.blit(surface, (0, 0))

        # Draw current balls
        for ball in self.balls:
            pygame.draw.circle(self.screen, ball.color, 
                             (int(ball.x), int(ball.y)), 
                             ball.radius)

        # Draw instructions
        instructions = [
            "Click to add balls",
            "SPACE to clear",
            "R to reset",
            f"Balls: {len(self.balls)}"
        ]
        
        for i, text in enumerate(instructions):
            surface = self.font.render(text, True, WHITE)
            self.screen.blit(surface, (10, 10 + i * 30))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == '__main__':
    simulation = BallSimulation()
    simulation.run()