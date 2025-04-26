import random
import time

# Utility Functions
def slow_print(text, delay=0.05):
    """Prints text slowly for dramatic effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def choose_option(options):
    """Allows the player to choose an option from a list."""
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")
    choice = input("Choose an option: ")
    return int(choice) - 1

# Player Class
class Player:
    def __init__(self, name, health=100, inventory=None):
        self.name = name
        self.health = health
        self.inventory = inventory if inventory is not None else []

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            slow_print(f"{self.name} has been defeated...")
        else:
            slow_print(f"{self.name} now has {self.health} health.")

    def add_to_inventory(self, item):
        self.inventory.append(item)
        slow_print(f"{item} has been added to your inventory.")

    def show_inventory(self):
        slow_print(f"{self.name}'s Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}")

# Enemy Class
class Enemy:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage

    def attack(self, player):
        slow_print(f"{self.name} attacks {player.name} for {self.damage} damage!")
        player.take_damage(self.damage)

# Game Functions
def encounter_enemy(player, enemy):
    slow_print(f"A wild {enemy.name} appears!")
    while enemy.health > 0 and player.health > 0:
        options = ["Attack", "Run"]
        choice = choose_option(options)
        if choice == 0:
            damage = random.randint(5, 15)
            slow_print(f"You attack the {enemy.name} for {damage} damage!")
            enemy.health -= damage
            if enemy.health > 0:
                enemy.attack(player)
            else:
                slow_print(f"You have defeated the {enemy.name}!")
                loot = random.choice(["Gold Coin", "Health Potion", "Mysterious Artifact"])
                player.add_to_inventory(loot)
        elif choice == 1:
            slow_print("You run away!")
            break

def find_treasure(player):
    slow_print("You find a treasure chest!")
    options = ["Open it", "Leave it"]
    choice = choose_option(options)
    if choice == 0:
        treasure = random.choice(["Sword", "Shield", "Magic Wand"])
        slow_print(f"You found a {treasure}!")
        player.add_to_inventory(treasure)
    else:
        slow_print("You decide to leave the treasure.")

def main_game():
    slow_print("Welcome to the Adventure Game!")
    player_name = input("Enter your character's name: ")
    player = Player(player_name)
    
    while player.health > 0:
        options = ["Explore the forest", "Rest at camp", "Check inventory"]
        choice = choose_option(options)
        
        if choice == 0:
            encounter = random.choice(["enemy", "treasure", "nothing"])
            if encounter == "enemy":
                enemy = Enemy("Goblin", health=random.randint(20, 40), damage=random.randint(5, 10))
                encounter_enemy(player, enemy)
            elif encounter == "treasure":
                find_treasure(player)
            else:
                slow_print("You explore the forest but find nothing.")
        
        elif choice == 1:
            slow_print("You rest at the camp and recover 20 health.")
            player.health = min(100, player.health + 20)
        
        elif choice == 2:
            player.show_inventory()
    
    slow_print("Game Over. Thank you for playing!")

if __name__ == "__main__":
    main_game()
