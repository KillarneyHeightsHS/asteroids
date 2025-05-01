# asteroids
Modified version of the asteroid program tutorial from Real Python to fit into a single lesson

## Step 0
Clone the repository on github using GitHub Desktop and open the project using vscode. This repository is `KillarneyHeightsHS\asteroids`

Remember in vscode you can have a terminal window with a command line open by pressing ``Ctrl+` ``
## Step 1
Ensure Python is installed
windows: `py.exe --version`
or
mac: `python3 --version`

If you have installed Python previously but it will not run from the command line, try reinstalling it and ensure that you check the option to include Python in your `PATH`.

## Step 2
Ensure pip is installed. 

Pip is a package manager for Python. It helps you add and manage third-party libraries that you can use for coding.

windows: `py.exe -m ensurepip`
or
mac: `python3 -m ensurepip`

If pip is installed you should see something similar to the following:
```
PS C:\Users\mrbev\Documents\GitHub\asteroids> py.exe -m ensurepip
Looking in links: c:\Users\mrbev\AppData\Local\Temp\tmpox97ui65
Requirement already satisfied: pip in c:\users\mrbev\appdata\local\programs\python\python313\lib\site-packages (25.0.1)
```

## Step 3
Create a virtual environment. This will allow us to run our code in its own space and help ensure that all commands work without changing the overall computer setup.

`py.exe -m venv .venv`
or 
`python3 -m venv .venv`

To confirm this has worked and start the virtual environment type the following:
windows: `.\.venv\Scripts\Activate.bat`
or 
mac: `source .venv/bin/activate`

If this is successful your terminal should look something like:
- windows:
```
(.venv) PS C:\Users\mrbev\Documents\GitHub\asteroids\.venv\Scripts>
```
- mac:
```
(.venv) mrbev@Mac asteroids %
```

## Step 4
Install the required libraries using pip
`pip install -r requirements.txt`

## Step 5
In github desktop:
1. Set the current repository to `asteroids`
2. Set the current branch to `0-basecode`

_or_

From the commandline run the command
`git checkout 0-basecode`
to switch to the base code branch. 

## Step 6
Run the code to check that everything is working.
`python.exe main.py`
or
`python3 main.py`

Key things to note:
- `models.py` contains the game objects and their behaviours
- `util.py` contains utility functions for loading assets, etc.
- `main.py` is the entry point of the game.
- `space_rocks.py` is where the game loop is defined.

## Step 7 - Adding the Spaceship

We need to modify `space_rocks.py` to load the spaceship sprite and add it to the game.

1. import the Spaceship and GameObject classes from models at the top of the file

```python
from models import Spaceship, GameObject
```

2. Update the constructor with the spaceship, bullets which we will get to but needed for now. We also call `_setup` to setup the game.

```python
    def __init__(self) -> None:
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.spaceship = None
        self.bullets = []
        self._setup()
```

3. Define `_setup` method to create the spaceship object as it will allow us to reset the game in a later step. The coordinates used will place the spaceship in the centre of the screen.

```python
    def _setup(self) -> None:
        self.spaceship = Spaceship((400, 300), self.bullets.append)
```

4. Create a way to manage all of the game objects by creating a `_get_game_objects` method that returns a list of game objects.

```python
    def _get_game_objects(self) -> list[GameObject]:
        game_objects = []
        if self.spaceship:
            game_objects.append(self.spaceship)
        return game_objects
```

5. Update the `draw()` method to display all game objects on the screen. In this case the newly added spaceship.

```python
    def _draw(self) -> None:
        self.screen.blit(self.background, (0, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
            
        pygame.display.flip()
        self.clock.tick(60)
```

## Step 8 - Ship movement

1. Add in support for key presses to enable movement

```python
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
```

2. Ensure that any movement is display on screen

```python
    def _process_game_logic(self) -> None:
        for game_object in self._get_game_objects():
            game_object.move(self.screen)
```

## Step 9 - Bullets
Lets make the ship fire bullets when the space bar is pressed.

1. Ensure that the screen is cleared of existing bullets when restarting

```python
    def _setup(self) -> None:
        self.bullets.clear()    # <--- New code
        self.spaceship = Spaceship((400, 300), self.bullets.append)
```

2. Make the spaceship shoot bullets and play a sound when shooting

```python
    def _handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
            # Shoot bullets when the spacebar is pressed
            elif (self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                self.spaceship.shoot()                
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
```

3. Don't allow bullets to wrap around the screen. Instead, remove them when they go off-screen.

```python
    def _process_game_logic(self) -> None:
        for game_object in self._get_game_objects():
            game_object.move(self.screen)
        
        # remove the bullets when they go off the screen
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)
```

4. Make sure the bullets are drawing on the screen
```python
    def _get_game_objects(self) -> list[GameObject]:
        # Include the bullets in the list of game objects
        game_objects = [*self.bullets] 
        if self.spaceship:
            game_objects.append(self.spaceship)
        return game_objects
```

## Step 10 - Asteroids
Lets add some asteroids for us to destroy.

1. Update the imports to include the `Asteroid` class and random placement of the asteroids.

```python
from util import load_sprite, get_random_position
from models import Asteroid, Spaceship, GameObject
```

2. Create a minimum distance for the asteroids to be from the spaceship.
```python
class Asteroids:
    MIN_ASTEROID_DISTANCE = 250
```

3. Create a list of asteroids
```python
    def __init__(self) -> None:
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.spaceship = None
        self.bullets = []
        self.asteroids = []    # <-- new code
        self._setup()
```

4. Add asteroids to the game loop.
```python
    def _setup(self) -> None:
        self.bullets.clear()
        self.asteroids.clear()
        self.spaceship = Spaceship((400, 300), self.bullets.append)

        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE):
                    break            

            self.asteroids.append(Asteroid(position, self.asteroids.append))
```

5. Ensure the asteroids are draw on the screen
```python
    def _get_game_objects(self) -> list[GameObject]:
        game_objects = [*self.asteroids, *self.bullets]
        if self.spaceship:
            game_objects.append(self.spaceship)
        return game_objects
```

## Step 11 - Collisions
The game is kind of boring without collisions. Both of asteroids with the spaceship and bullets with asteroids should be handled.

*Existing code*
```python
    def _process_game_logic(self) -> None:
        for game_object in self._get_game_objects():
            game_object.move(self.screen)
            
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)
```

1. Add to `_process_game_logic` checks to see if an asteroid collides with the spaceship to destroy the spaceship
```python

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship.destroy()
                    self.spaceship = None
                    self.message = "You lost!"
                    break
```

2. Add to `_process_game_logic` checks to see if a bullet hits an asteroid, destroying both the bullet and splitting the asteroid into smaller pieces.
```python
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break
```

## Step 12 - Game Over
We want to inform the player if they have won the game or lost.

1. Import a helper function `print_text` to display messages
```python
import pygame
from models import Asteroid, Spaceship, GameObject
from util import get_random_position, load_sprite, print_text
```

2. Initialise the message and a font to use.
```python
    def __init__(self) -> None:
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)  # <--  New code
        self.message = ""                       # <--  New code
        self.asteroids = []  
        self.bullets = []
        self._play_again()
```

3. Clear the message on restart.
```python
    def _setup(self) -> None:
        self.message = ""
        self.bullets.clear()
        self.asteroids.clear()
        self.spaceship = Spaceship((400, 300), self.bullets.append)

        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE):
                    break            

            self.asteroids.append(Asteroid(position, self.asteroids.append))
```

4. Add in text for winning and losing.
```python
    def _process_game_logic(self) -> None:
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship.destroy()
                    self.spaceship = None
                    self.message = "You lost!"  # <-- new code
                    break

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        if not self.asteroids and self.spaceship:
            self.message = "You won!"  # <-- new code
```

5. Ensure the message is displayed on the screen.
```python
    def _draw(self) -> None:
        self.screen.blit(self.background, (0, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        
        # display any message on the screen
        if self.message:
            print_text(self.screen, self.message, self.font)

        pygame.display.flip()
        self.clock.tick(60)
```

## Extensions
- Add in a scoring and a scoreboard
- Add in power-ups that can be collected by the spaceship
- Add in different levels with increasing difficulty
- Support for multiple players
