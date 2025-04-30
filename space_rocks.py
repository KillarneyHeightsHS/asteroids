import pygame
from util import load_sprite
from models import Spaceship, GameObject

class Asteroids:

    def __init__(self) -> None:
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.spaceship = None
        self.bullets = []
        self._setup()
    
    def main_loop(self) -> None:
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()
    
    def _init_pygame(self) -> None:
        pygame.init()
        pygame.display.set_caption("Asteroids")

    def _setup(self) -> None:
        self.spaceship = Spaceship((400, 300), self.bullets.append)

    def _handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_r):
                self._setup()

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            elif is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
            elif is_key_pressed[pygame.K_DOWN]:
                self.spaceship.decelerate()

    def _process_game_logic(self) -> None:
        for game_object in self._get_game_objects():
            game_object.move(self.screen)
            
    def _get_game_objects(self) -> list[GameObject]:
        game_objects = []
        if self.spaceship:
            game_objects.append(self.spaceship)
        return game_objects
    
    def _draw(self) -> None:
        self.screen.blit(self.background, (0, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
            
        pygame.display.flip()
        self.clock.tick(60)

