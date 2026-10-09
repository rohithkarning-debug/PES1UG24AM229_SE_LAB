import pygame
import random
from .target import Target
from .sounds import Sounds

# Game Engine

WHITE = (255, 255, 255)
RED = (220, 60, 60)
LIGHT_GRAY = (180, 180, 190)
OVERLAY = (0, 0, 0, 180)

# Target settings per difficulty. Medium matches the original game.
DIFFICULTIES = {
    "Easy":   {"base_radius": 50, "min_radius": 20, "lifespan_frames": 150},
    "Medium": {"base_radius": 40, "min_radius": 12, "lifespan_frames": 90},
    "Hard":   {"base_radius": 30, "min_radius": 8,  "lifespan_frames": 60},
}

# Keys that start a new round from the Game Over screen.
DIFFICULTY_KEYS = {
    pygame.K_1: "Easy",   pygame.K_e: "Easy",
    pygame.K_2: "Medium", pygame.K_m: "Medium",
    pygame.K_3: "Hard",   pygame.K_h: "Hard",
}

class GameEngine:
    def __init__(self, width, height, difficulty="Medium"):
        self.width = width
        self.height = height

        self.margin = 60
        self.hud_height = 60
        self.round_seconds = 30

        self.font = pygame.font.SysFont("Arial", 26)
        self.big_font = pygame.font.SysFont("Arial", 56, bold=True)
        self.quit_requested = False  # set on the Game Over screen; main.py exits
        self.sounds = Sounds()

        self.reset(difficulty)

    def reset(self, difficulty):
        # Start a fresh round at the chosen difficulty.
        self.difficulty = difficulty
        self.target = self._spawn_target()
        self.time_left_frames = self.round_seconds * 60

        self.hits = 0
        self.misses = 0
        self.score = 0
        self.game_over = False

    def _spawn_target(self):
        x = random.randint(self.margin, self.width - self.margin)
        y = random.randint(self.margin + self.hud_height, self.height - self.margin)
        return Target(x, y, **DIFFICULTIES[self.difficulty])

    def handle_event(self, event):
        if self.game_over:
            # Wait on the Game Over screen; clicks are ignored.
            if event.type == pygame.KEYDOWN:
                if event.key in DIFFICULTY_KEYS:
                    self.reset(DIFFICULTY_KEYS[event.key])
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    self.quit_requested = True
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_click(event.pos)

    def _handle_click(self, pos):
        x, y = pos
        if self.target.contains_point(x, y):
            self.hits += 1
            self.score += 1
            self.target = self._spawn_target()
            self.sounds.play("hit")
        else:
            self.misses += 1
            self.sounds.play("miss")

    def handle_input(self):
        # Reserved for continuously-held-key input; this game is
        # entirely mouse-driven, so there's nothing to poll here.
        pass

    def update(self):
        if self.game_over:
            return

        self.time_left_frames -= 1
        if self.time_left_frames <= 0:
            self.game_over = True
            self.sounds.play("round_end")
            return

        self.target.update()
        if self.target.expired():
            self.misses += 1  # letting a target time out counts as a miss too
            self.target = self._spawn_target()
            self.sounds.play("miss")

    def accuracy(self):
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return round(100 * self.hits / total, 1)

    def render(self, screen):
        if not self.game_over:
            r = self.target.drawn_radius()
            pygame.draw.circle(screen, RED, (self.target.x, self.target.y), r)
            pygame.draw.circle(screen, WHITE, (self.target.x, self.target.y), r, 2)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        seconds_left = max(0, self.time_left_frames // 60)
        timer_text = self.font.render(f"Time: {seconds_left}s", True, WHITE)
        screen.blit(timer_text, (self.width - 140, 10))

        acc_text = self.font.render(f"Accuracy: {self.accuracy()}%", True, WHITE)
        screen.blit(acc_text, (self.width // 2 - 90, 10))

        if self.game_over:
            self._render_game_over(screen)

    def _render_game_over(self, screen):
        # Dim the playfield, then show the final results centered on screen.
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill(OVERLAY)
        screen.blit(overlay, (0, 0))

        lines = [
            (self.big_font, "Time's Up!", WHITE),
            (self.font, f"Final Score: {self.score}", WHITE),
            (self.font, f"Accuracy: {self.accuracy()}%", WHITE),
            (self.font, f"Hits: {self.hits}   Misses: {self.misses}   ({self.difficulty})", LIGHT_GRAY),
            (self.font, "Play again:  1 Easy   2 Medium   3 Hard", WHITE),
            (self.font, "Press Q or Esc to quit", LIGHT_GRAY),
        ]
        y = self.height // 2 - 150
        for font, text, color in lines:
            surf = font.render(text, True, color)
            screen.blit(surf, surf.get_rect(midtop=(self.width // 2, y)))
            y += surf.get_height() + 16
