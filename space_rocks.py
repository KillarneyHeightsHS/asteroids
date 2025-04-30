import pygame
from util import load_sprite

class Asteroids:

    def __init__(self) -> None:
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
    
    def main_loop(self) -> None:
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()
    
    def _init_pygame(self) -> None:
        pygame.init()
        pygame.display.set_caption("Asteroids")

    def _play_again(self) -> None:
        pass

    def _handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()

    def _process_game_logic(self) -> None:
        pass

    def _draw(self) -> None:
        self.screen.blit(self.background, (0, 0))

        pygame.display.flip()
        self.clock.tick(60)

