from sys import exit
from random import randint
from textwrap import dedent

# Base class for all scenes
class Scene(object):
    def enter(self):
        # Abstract method, to be implemented by subclasses
        print("This scene is not yet configured.")
        exit(1)

# Game engine to manage the flow of the game
class Engine(object):
    def __init__(self, scene_map):
        self.scene_map = scene_map

    def play(self):
        current_scene = self.scene_map.opening_scene()
        last_scene = self.scene_map.next_scene('finished')

        while current_scene != last_scene:
            next_scene_name = current_scene.enter()
            current_scene = self.scene_map.next_scene(next_scene_name)

        # Ensure the last scene is entered
        current_scene.enter()

# Example subclass representing a failure/death scene
class Death(Scene):
    quips = [
        # List of possible death messages
    ]

    def enter(self):
        # Print a random death message and exit
        print(Death.quips[randint(0, len(self.quips) - 1)])
        exit(1)

# Example of a more complex scene with decision branches
class CentralCorridor(Scene):
    def enter(self):
        # Print the scene description
        print(dedent("""
            # Scene setup
        """))

        # Player's action choice
        action = input("> ")

        # Different outcomes based on the player's action
        if action == "shoot!":
            return 'death'
        elif action == "dodge!":
            return 'death'
        elif action == "tell a joke":
            return 'laser_weapon_armory'
        else:
            print("DOES NOT COMPUTE!")
            return 'central_corridor'

# Example of a puzzle/logic-based scene
class LaserWeaponArmory(Scene):
    def enter(self):
        # Scene description
        print(dedent("""
            # Puzzle description
        """))

        # Example code logic
        code = f"{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}"
        guess = input("[keypad]> ")
        guesses = 0

        # Loop for multiple guesses
        while guess != code and guesses < 10:
            guesses += 1
            guess = input("[keypad]> ")

        if guess == code:
            return 'the_bridge'
        else:
            return 'death'

# Placeholder for additional complex scenes
class TheBridge(Scene):
    def enter(self):
        # Scene logic
        pass

class EscapePod(Scene):
    def enter(self):
        # Scene logic
        pass

class Finished(Scene):
    def enter(self):
        print("You won! Good job.")
        return 'finished'

# Map class to manage scene transitions
class Map(object):
    scenes = {
        'central_corridor': CentralCorridor(),
        'laser_weapon_armory': LaserWeaponArmory(),
        'the_bridge': TheBridge(),
        'escape_pod': EscapePod(),
        'death': Death(),
        'finished': Finished(),
    }

    def __init__(self, start_scene):
        self.start_scene = start_scene

    def next_scene(self, scene_name):
        return Map.scenes.get(scene_name)
    
    def opening_scene(self):
        return self.next_scene(self.start_scene)

# Start the game
a_map = Map('central_corridor')
a_game = Engine(a_map)
a_game.play()
