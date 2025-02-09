import pygame
import sys
import random
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
GREEN = (50, 205, 50)
RED = (255, 99, 71)
BLUE = (30, 144, 255)
PURPLE = (147, 112, 219)

class MathQuiz:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Math Quiz Game')
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.question_font = pygame.font.Font(None, 48)
        self.input_font = pygame.font.Font(None, 36)
        
        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.total_questions = 0
        self.user_input = ""
        self.feedback = ""
        self.feedback_color = WHITE
        self.feedback_timer = 0
        self.generate_question()
        self.game_state = "playing"  # playing, game_over
        self.background_color = BLUE

    def generate_question(self):
        # Generate random numbers and operation
        self.num1 = random.randint(1, 20)
        self.num2 = random.randint(1, 20)
        self.operation = random.choice(['+', '-', '*'])
        
        # Ensure subtraction doesn't give negative results
        if self.operation == '-' and self.num1 < self.num2:
            self.num1, self.num2 = self.num2, self.num1
        
        # Calculate correct answer
        if self.operation == '+':
            self.correct_answer = self.num1 + self.num2
        elif self.operation == '-':
            self.correct_answer = self.num1 - self.num2
        else:  # multiplication
            self.correct_answer = self.num1 * self.num2

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                if self.game_state == "game_over":
                    if event.key == K_r:
                        self.reset_game()
                else:
                    if event.key == K_RETURN and self.user_input:
                        self.check_answer()
                    elif event.key == K_BACKSPACE:
                        self.user_input = self.user_input[:-1]
                    elif event.unicode.isnumeric() or event.unicode == '-':
                        self.user_input += event.unicode

    def check_answer(self):
        try:
            user_answer = int(self.user_input)
            if user_answer == self.correct_answer:
                self.feedback = "Correct!"
                self.feedback_color = GREEN
                self.score += 1
                self.background_color = GREEN
            else:
                self.feedback = f"Wrong! Answer was {self.correct_answer}"
                self.feedback_color = RED
                self.background_color = RED
            
            self.total_questions += 1
            self.feedback_timer = 60  # Show feedback for 1 second
            self.user_input = ""
            
            if self.total_questions >= 10:  # End game after 10 questions
                self.game_state = "game_over"
            else:
                self.generate_question()
                
        except ValueError:
            self.feedback = "Please enter a valid number"
            self.feedback_color = RED
            self.background_color = RED
            self.feedback_timer = 60

    def update(self):
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
            if self.feedback_timer == 0:
                self.feedback = ""
                self.background_color = BLUE

    def draw(self):
        self.screen.fill(self.background_color)

        if self.game_state == "playing":
            # Draw question
            question_text = f"What is {self.num1} {self.operation} {self.num2}?"
            question_surface = self.question_font.render(question_text, True, WHITE)
            question_rect = question_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//3))
            self.screen.blit(question_surface, question_rect)

            # Draw user input
            input_text = f"Your answer: {self.user_input}"
            input_surface = self.input_font.render(input_text, True, WHITE)
            input_rect = input_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(input_surface, input_rect)

            # Draw feedback
            if self.feedback:
                feedback_surface = self.input_font.render(self.feedback, True, self.feedback_color)
                feedback_rect = feedback_surface.get_rect(center=(WINDOW_WIDTH//2, 2*WINDOW_HEIGHT//3))
                self.screen.blit(feedback_surface, feedback_rect)

            # Draw score
            score_text = f"Score: {self.score}/{self.total_questions}"
            score_surface = self.input_font.render(score_text, True, WHITE)
            self.screen.blit(score_surface, (10, 10))

        else:  # Game Over screen
            # Draw final score
            game_over_text = "Game Over!"
            game_over_surface = self.title_font.render(game_over_text, True, WHITE)
            game_over_rect = game_over_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//3))
            self.screen.blit(game_over_surface, game_over_rect)

            final_score = f"Final Score: {self.score}/10"
            score_surface = self.question_font.render(final_score, True, WHITE)
            score_rect = score_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(score_surface, score_rect)

            restart_text = "Press R to restart"
            restart_surface = self.input_font.render(restart_text, True, WHITE)
            restart_rect = restart_surface.get_rect(center=(WINDOW_WIDTH//2, 2*WINDOW_HEIGHT//3))
            self.screen.blit(restart_surface, restart_rect)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = MathQuiz()
    game.run()