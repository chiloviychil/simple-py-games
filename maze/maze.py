import pygame
import random
import sys

# Screen dimensions and colors
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
MAZE_COLOR1 = (40, 44, 52)
MAZE_COLOR2 = (0, 0, 128)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_RED = (255, 100, 100)

class MazeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Maze Navigation Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.level = 1
        self.time_limit = 60
        self.generate_new_maze()
        self.start_screen = True

    def generate_new_maze(self):
        size = 15 + (self.level * 2)  # Gradually increase maze size
        size = min(size, 31)  # Limit size to prevent extreme scaling issues
        self.maze, self.start_pos, self.end_pos = self.generate_maze(size, size)
        self.player_pos = list(self.start_pos)
        self.start_time = pygame.time.get_ticks()

    def generate_maze(self, width, height):
        """ Generates a perfect maze using randomized DFS. """
        maze = [[1 for _ in range(width)] for _ in range(height)]

        def is_valid(x, y):
            return 0 < x < width-1 and 0 < y < height-1

        def carve_path(x, y):
            maze[y][x] = 0
            directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if is_valid(nx, ny) and maze[ny][nx] == 1:
                    maze[y + dy//2][x + dx//2] = 0
                    carve_path(nx, ny)

        # Start maze generation
        carve_path(1, 1)

        # Ensure start and end positions
        start_pos = (1, 1)
        end_pos = (width-2, height-2)
        maze[start_pos[1]][start_pos[0]] = 2  # Start
        maze[end_pos[1]][end_pos[0]] = 3  # End

        # Ensure the maze is solvable
        if not self.is_path_exists(maze, *start_pos, *end_pos):
            return self.generate_maze(width, height)  # Regenerate if unsolvable

        return maze, start_pos, end_pos

    def is_path_exists(self, maze, sx, sy, ex, ey):
        """ Checks if a path exists using DFS. """
        height, width = len(maze), len(maze[0])
        visited = [[False for _ in range(width)] for _ in range(height)]

        def dfs(x, y):
            if (x, y) == (ex, ey):
                return True
            if not (0 <= x < width and 0 <= y < height) or maze[y][x] == 1 or visited[y][x]:
                return False
            visited[y][x] = True
            return any(dfs(x+dx, y+dy) for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)])

        return dfs(sx, sy)

    def draw_maze(self):
        cell_width = SCREEN_WIDTH // len(self.maze[0])
        cell_height = SCREEN_HEIGHT // len(self.maze)
        
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
                if cell == 1:  # Wall
                    pygame.draw.rect(self.screen, MAZE_COLOR1 if (x+y)%2==0 else MAZE_COLOR2, rect)
                elif cell == 2:  # Start
                    pygame.draw.rect(self.screen, GREEN, rect)
                elif cell == 3:  # End
                    pygame.draw.rect(self.screen, RED, rect)

    def draw_player(self):
        cell_width = SCREEN_WIDTH // len(self.maze[0])
        cell_height = SCREEN_HEIGHT // len(self.maze)
        player_rect = pygame.Rect(self.player_pos[0] * cell_width, self.player_pos[1] * cell_height, cell_width, cell_height)
        pygame.draw.circle(self.screen, LIGHT_RED, player_rect.center, cell_width//3)

    def draw_start_screen(self):
        self.screen.fill(BLACK)
        title = self.font.render("Maze Navigation Game", True, WHITE)
        start_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 50)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//2 - 100))
        pygame.draw.rect(self.screen, GREEN, start_button)
        start_text = self.font.render("START", True, BLACK)
        self.screen.blit(start_text, (start_button.x + 60, start_button.y + 10))
        return start_button

    def move_player(self, dx, dy):
        new_x, new_y = self.player_pos[0] + dx, self.player_pos[1] + dy
        if (0 <= new_x < len(self.maze[0]) and 0 <= new_y < len(self.maze) and self.maze[new_y][new_x] != 1):
            self.player_pos = [new_x, new_y]
            if self.maze[new_y][new_x] == 3:  # If reached the end
                self.level_up()

    def level_up(self):
        self.level += 1
        self.time_limit += 15
        self.generate_new_maze()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.start_screen:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.draw_start_screen().collidepoint(mouse_pos):
                            self.start_screen = False
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.move_player(-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            self.move_player(1, 0)
                        elif event.key == pygame.K_UP:
                            self.move_player(0, -1)
                        elif event.key == pygame.K_DOWN:
                            self.move_player(0, 1)
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

            self.screen.fill(BLACK)
            if self.start_screen:
                self.draw_start_screen()
            else:
                current_time = pygame.time.get_ticks()
                elapsed_time = (current_time - self.start_time) / 1000
                remaining_time = max(0, self.time_limit - elapsed_time)

                self.draw_maze()
                self.draw_player()
                timer_text = self.font.render(f"Time: {int(remaining_time)}s | Level: {self.level}", True, WHITE)
                self.screen.blit(timer_text, (10, 10))

                if remaining_time <= 0:
                    game_over_text = self.font.render("Game Over! Time's Up", True, WHITE)
                    self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    self.reset_game()

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = MazeGame()
    game.run()
