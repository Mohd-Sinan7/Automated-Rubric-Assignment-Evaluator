import pygame
from .snake import Snake
from .food import Food
from .sound import SoundManager

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 60, 60)
GRAY = (170, 170, 170)
YELLOW = (255, 220, 90)
OVERLAY = (0, 0, 0, 215)

# (name, snake moves per second); Medium is the original speed.
DIFFICULTIES = [("Easy", 5), ("Medium", 8), ("Hard", 12)]
DEFAULT_DIFFICULTY = 1
# The game-over menu lists every difficulty followed by an Exit entry.
EXIT_OPTION = len(DIFFICULTIES)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 20
        self.grid_width = width // self.cell_size
        self.grid_height = height // self.cell_size

        self.font = pygame.font.SysFont("Arial", 30)
        self.title_font = pygame.font.SysFont("Arial", 64, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 24)
        self.sounds = SoundManager()

        self.reset(DEFAULT_DIFFICULTY)

    def reset(self, difficulty):
        # Start a fresh round at the chosen difficulty.
        self.difficulty = difficulty
        self.moves_per_second = DIFFICULTIES[difficulty][1]
        self._frame_counter = 0

        self.snake = Snake(self.grid_width // 2, self.grid_height // 2, self.cell_size)
        self.food = Food(self.grid_width, self.grid_height, self.cell_size, self.snake.body)
        self.score = 0

        self.game_over = False
        # Pre-select the difficulty just played on the game-over menu.
        self.menu_index = difficulty

    def handle_keydown(self, key):
        if self.game_over:
            self._handle_menu_key(key)
            return

        # Direction changes are queued and applied on the next move(s);
        # the snake rejects reversals into its own body.
        if key in (pygame.K_UP, pygame.K_w):
            self.snake.set_direction(0, -1)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.snake.set_direction(0, 1)
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.snake.set_direction(-1, 0)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.snake.set_direction(1, 0)

    def _handle_menu_key(self, key):
        # The game-over screen waits here until the player picks an option.
        option_count = EXIT_OPTION + 1
        if key in (pygame.K_UP, pygame.K_w):
            self.menu_index = (self.menu_index - 1) % option_count
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.menu_index = (self.menu_index + 1) % option_count
        elif key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            self._choose(self.menu_index)
        elif key in (pygame.K_1, pygame.K_KP1):
            self._choose(0)
        elif key in (pygame.K_2, pygame.K_KP2):
            self._choose(1)
        elif key in (pygame.K_3, pygame.K_KP3):
            self._choose(2)
        elif key in (pygame.K_ESCAPE, pygame.K_q):
            self._choose(EXIT_OPTION)

    def _choose(self, option):
        if option == EXIT_OPTION:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        else:
            self.reset(option)

    def handle_input(self):
        # Reserved for continuously-held-key input (not used for a
        # grid-based snake, but kept here to mirror the engine's shape).
        pass

    def update(self):
        if self.game_over:
            return

        self._frame_counter += 1
        frames_per_move = max(1, 60 // self.moves_per_second)
        if self._frame_counter < frames_per_move:
            return
        self._frame_counter = 0

        # Check the cell the head is about to enter before moving, so the
        # snake stays on screen where it crashed instead of off the grid.
        next_head = self.snake.next_head()
        if self.snake.collides_with_wall(next_head, self.grid_width, self.grid_height):
            self._end_game()
            return

        if self.snake.collides_with_self(next_head):
            self._end_game()
            return

        self.snake.move()

        if self.snake.body[0] == (self.food.x, self.food.y):
            self.snake.grow()
            self.score += 1
            self.sounds.play("eat")
            if not self.food.respawn(self.snake.body):
                # Snake fills the whole board: nothing left to eat.
                self._end_game()

    def _end_game(self):
        self.game_over = True
        self.sounds.play("game_over")

    def render(self, screen):
        # Draw food
        pygame.draw.rect(screen, RED, self.food.rect())

        # Draw snake
        for rect in self.snake.segment_rects():
            pygame.draw.rect(screen, GREEN, rect)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        level_text = self.small_font.render(DIFFICULTIES[self.difficulty][0], True, GRAY)
        screen.blit(level_text, level_text.get_rect(topright=(self.width - 10, 14)))

        if self.game_over:
            self._render_game_over(screen)

    def _render_game_over(self, screen):
        # Dim the final board and show the result on top of it.
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill(OVERLAY)
        screen.blit(overlay, (0, 0))

        self._blit_centered(screen, self.title_font, "GAME OVER", RED, 150)
        self._blit_centered(screen, self.font, f"Final Score: {self.score}", WHITE, 220)
        self._blit_centered(screen, self.small_font, "Play again or exit:", GRAY, 280)

        labels = [f"{i + 1}   {name}" for i, (name, _) in enumerate(DIFFICULTIES)]
        labels.append("Q   Exit")
        for i, label in enumerate(labels):
            selected = i == self.menu_index
            text = f"> {label} <" if selected else label
            color = YELLOW if selected else WHITE
            self._blit_centered(screen, self.font, text, color, 325 + i * 40)

        self._blit_centered(
            screen, self.small_font, "Up/Down + Enter, or press 1-3 / Q", GRAY, 500
        )

    def _blit_centered(self, screen, font, text, color, center_y):
        surface = font.render(text, True, color)
        screen.blit(surface, surface.get_rect(center=(self.width // 2, center_y)))
