import pygame
from pathlib import Path
from .player import Player
from .obstacle import Obstacle


# Game Engine

WHITE = (255, 255, 255)
BROWN = (120, 80, 40)
DARK_GREEN = (30, 100, 30)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ground_y = height - 40

        self.player = Player(80, self.ground_y)

        # Difficulty settings
        self.difficulties = {
            "easy": {
                "speed": 4,
                "spawn_interval": 90,
                "max_speed": 10
            },
            "medium": {
                "speed": 6,
                "spawn_interval": 70,
                "max_speed": 12
            },
            "hard": {
                "speed": 8,
                "spawn_interval": 50,
                "max_speed": 14
            }
        }

        self.difficulty = "medium"

        self.speed = self.difficulties[self.difficulty]["speed"]
        self.speed_increase_per_frame = 0.003
        self.max_speed = self.difficulties[self.difficulty]["max_speed"]

        self.spawn_interval = self.difficulties[self.difficulty]["spawn_interval"]
        self._spawn_timer = 0
        self.obstacles = []

        self.distance = 0
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        # ---------------------------------------------------------
        # Sound setup
        # ---------------------------------------------------------

        self.sounds_enabled = False
        self.jump_sound = None
        self.score_sound = None
        self.game_over_sound = None

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            # Project root / assets / sounds
            sound_dir = (
                Path(__file__).resolve().parent.parent
                / "assets"
                / "sounds"
            )

            self.jump_sound = pygame.mixer.Sound(
                str(sound_dir / "jump.wav")
            )

            self.score_sound = pygame.mixer.Sound(
                str(sound_dir / "score.wav")
            )

            self.game_over_sound = pygame.mixer.Sound(
                str(sound_dir / "game_over.wav")
            )

            self.sounds_enabled = True

        except (pygame.error, OSError) as e:
            print("Warning: Sound disabled:", e)

        self.game_over = False

    def play_sound(self, sound):
        """
        Play a sound only if sound loading was successful.
        """
        if self.sounds_enabled and sound is not None:
            sound.play()

    def handle_event(self, event):
        # ---------------------------------------------------------
        # Game Over / difficulty selection menu
        # ---------------------------------------------------------

        if self.game_over:
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:

                # Easy
                if event.key == pygame.K_1:
                    self.reset_game("easy")

                # Medium
                elif event.key == pygame.K_2:
                    self.reset_game("medium")

                # Hard
                elif event.key == pygame.K_3:
                    self.reset_game("hard")

                # Exit
                elif event.key == pygame.K_4:
                    pygame.quit()
                    raise SystemExit

            return

        # ---------------------------------------------------------
        # Normal gameplay input
        # ---------------------------------------------------------

        if event.type == pygame.KEYDOWN and event.key in (
            pygame.K_SPACE,
            pygame.K_UP,
            pygame.K_w
        ):
            self.player.jump()

            # Task 4: jump sound
            self.play_sound(self.jump_sound)

    def handle_input(self):
        # Reserved for continuously-held-key input.
        pass

    def reset_game(self, difficulty):
        """
        Completely reset the game using the selected difficulty.
        """

        self.difficulty = difficulty

        settings = self.difficulties[difficulty]

        # Reset player position and velocity
        self.player = Player(80, self.ground_y)

        # Reset obstacles
        self.obstacles = []

        # Reset difficulty-related variables
        self.speed = settings["speed"]
        self.max_speed = settings["max_speed"]
        self.spawn_interval = settings["spawn_interval"]

        # Reset timers and game state
        self._spawn_timer = 0
        self.distance = 0
        self.score = 0
        self.game_over = False

    def update(self):
        if self.game_over:
            return

        # Increase speed, but never exceed the difficulty's
        # maximum speed.
        self.speed = min(
            self.speed + self.speed_increase_per_frame,
            self.max_speed
        )

        self.player.update()

        self._spawn_timer += 1

        if self._spawn_timer >= self.spawn_interval:
            self._spawn_timer = 0

            self.obstacles.append(
                Obstacle(
                    self.width,
                    self.ground_y,
                    self.speed
                )
            )

        # ---------------------------------------------------------
        # Store previous positions before moving obstacles.
        # This is part of the Task 1 collision fix.
        # ---------------------------------------------------------

        previous_x = {}

        for obstacle in self.obstacles:
            previous_x[id(obstacle)] = obstacle.x

            obstacle.move()
            obstacle.speed = self.speed

        # ---------------------------------------------------------
        # Collision detection
        # ---------------------------------------------------------

        player_rect = self.player.rect()

        for obstacle in self.obstacles:

            current_rect = obstacle.rect()

            # 1. Normal collision check
            if current_rect.colliderect(player_rect):
                self.game_over = True

                # Task 4: Game Over sound
                self.play_sound(self.game_over_sound)

                return

            # 2. Swept collision check
            #
            # Detect if the obstacle crossed through the player's
            # hitbox between the previous and current frame.
            old_x = previous_x[id(obstacle)]
            new_x = obstacle.x

            # Obstacles move from right to left.
            if new_x < old_x:

                old_left = old_x
                old_right = old_x + obstacle.width

                new_left = new_x
                new_right = new_x + obstacle.width

                # Player's horizontal range
                player_left = player_rect.left
                player_right = player_rect.right

                # Check whether obstacle crossed the player's
                # horizontal range.
                crossed_horizontally = (
                    old_right >= player_left
                    and new_left <= player_right
                )

                # Check vertical overlap.
                crossed_vertically = (
                    current_rect.bottom >= player_rect.top
                    and current_rect.top <= player_rect.bottom
                )

                if crossed_horizontally and crossed_vertically:
                    self.game_over = True

                    # Task 4: Game Over sound
                    self.play_sound(self.game_over_sound)

                    return

        # ---------------------------------------------------------
        # Scoring
        # ---------------------------------------------------------

        for obstacle in self.obstacles:
            if (
                not obstacle.scored
                and obstacle.x + obstacle.width < self.player.x
            ):
                obstacle.scored = True
                self.score += 1

                # Task 4: score sound
                self.play_sound(self.score_sound)

        # ---------------------------------------------------------
        # Remove obstacles that have gone off screen.
        # ---------------------------------------------------------

        self.obstacles = [
            obstacle
            for obstacle in self.obstacles
            if not obstacle.off_screen()
        ]

        self.distance += self.speed

    def render(self, screen):
        # ---------------------------------------------------------
        # Normal game rendering
        # ---------------------------------------------------------

        pygame.draw.line(
            screen,
            BROWN,
            (0, self.ground_y),
            (self.width, self.ground_y),
            4
        )

        pygame.draw.rect(
            screen,
            WHITE,
            self.player.rect()
        )

        for obstacle in self.obstacles:
            pygame.draw.rect(
                screen,
                DARK_GREEN,
                obstacle.rect()
            )

        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            (0, 0, 0)
        )

        screen.blit(score_text, (10, 10))

        # ---------------------------------------------------------
        # Game Over / Difficulty Selection screen
        # ---------------------------------------------------------

        if self.game_over:

            game_over_font = pygame.font.SysFont(
                "Arial",
                60
            )

            menu_font = pygame.font.SysFont(
                "Arial",
                30
            )

            small_font = pygame.font.SysFont(
                "Arial",
                24
            )

            game_over_text = game_over_font.render(
                "GAME OVER",
                True,
                (200, 0, 0)
            )

            final_score_text = menu_font.render(
                f"Final Score: {self.score}",
                True,
                (0, 0, 0)
            )

            select_text = menu_font.render(
                "Select Difficulty",
                True,
                (0, 0, 0)
            )

            easy_text = menu_font.render(
                "1 - Easy",
                True,
                (0, 0, 0)
            )

            medium_text = menu_font.render(
                "2 - Medium",
                True,
                (0, 0, 0)
            )

            hard_text = menu_font.render(
                "3 - Hard",
                True,
                (0, 0, 0)
            )

            exit_text = menu_font.render(
                "4 - Exit",
                True,
                (0, 0, 0)
            )

            instruction_text = small_font.render(
                "Press a number key to select",
                True,
                (0, 0, 0)
            )

            # -----------------------------------------------------
            # Center everything on the screen
            # -----------------------------------------------------

            center_x = self.width // 2

            game_over_rect = game_over_text.get_rect(
                center=(center_x, 75)
            )

            final_score_rect = final_score_text.get_rect(
                center=(center_x, 135)
            )

            select_rect = select_text.get_rect(
                center=(center_x, 180)
            )

            easy_rect = easy_text.get_rect(
                center=(center_x, 225)
            )

            medium_rect = medium_text.get_rect(
                center=(center_x, 265)
            )

            hard_rect = hard_text.get_rect(
                center=(center_x, 305)
            )

            exit_rect = exit_text.get_rect(
                center=(center_x, 345)
            )

            instruction_rect = instruction_text.get_rect(
                center=(center_x, 390)
            )

            screen.blit(
                game_over_text,
                game_over_rect
            )

            screen.blit(
                final_score_text,
                final_score_rect
            )

            screen.blit(
                select_text,
                select_rect
            )

            screen.blit(
                easy_text,
                easy_rect
            )

            screen.blit(
                medium_text,
                medium_rect
            )

            screen.blit(
                hard_text,
                hard_rect
            )

            screen.blit(
                exit_text,
                exit_rect
            )

            screen.blit(
                instruction_text,
                instruction_rect
            )