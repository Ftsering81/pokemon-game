# Name: Fnu Tsering
# CSCI 39538: Homework 1: Pokemon Spec

class Grid:
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.player_number = 7
        self.player_current_pos = [0, 0]  # initialized to [0,0]

        #  A 2D grid filled with objects of class Square
        self.squares = [[Square() for j in range(num_cols)] for i in range(num_rows)]

    def __repr__(self):
        rep = f"Grid({self.num_rows}, {self.num_cols})"
        return rep

    def __str__(self):
        return f"The size of your grid is {self.num_rows}x{self.num_cols}"


class Square:

    def __init__(self, square_type: int = 1, player_present: bool = False, thing_present=None):
        # square_type will represent what kind of square it is or what is on the square:
        # 0 = inaccessible spot, 1 = accessible spot, 2 = item, 3 = Pokemon, 4 = Pokeball, 5 = CPU-trainer
        # Any integer that is not 0-5 will represent the square where the player currently is at.
        self.square_type = square_type
        self.player_present = player_present
        self.thing_present = thing_present

    def __repr__(self):
        rep = f"Square({self.square_type})"
        return rep

    def __str__(self):
        return f"{self.square_type}"


class Pokemon:
    square_type = 3

    def __init__(self, pokemon_id, name, health_points, attack_power, moves=[], wild=False):
        self.pokemon_id = pokemon_id
        self.name = name
        self.health_points = health_points
        self.attack_power = attack_power
        self.moves = moves
        self.wild = wild
        self.base_hp = health_points

    def __repr__(self):
        return f"Pokemon({self.pokemon_id}, {self.name}, {self.health_points}, {self.attack_power})"

    def __str__(self):
        return self.name

    def restore_hp(self):
        self.health_points = self.base_hp

    def attack(self, enemy_pokemon, move_selected):
        enemy_pokemon.health_points = enemy_pokemon.health_points - move_selected.attack_power
        if enemy_pokemon.health_points <= 0:
            enemy_pokemon.health_points = 0  # make sure HP value is not negative


class Trainer:
    square_type = 2

    def __init__(self, name=None, pokemon_selected=None, pokemon_awake=[], money=0.00, fun_fact="", bag=[]):
        self.name = name
        self.pokemon_selected = pokemon_selected
        self.pokemon_awake = pokemon_awake
        self.money = money
        self.fun_fact = fun_fact
        self.bag = bag
        self.pokemon_fainted = []

    def __repr__(self):
        return f"Trainer({self.name}, {self.pokemon_selected}, {self.pokemon_awake}, {self.money}, {self.fun_fact}, {self.bag}) "

    def __str__(self):
        return self.name

    def change_pokemon(self, pokemon_selected):
        self.pokemon_selected = pokemon_selected


class Player(Trainer):
    square_type = None

    def __repr__(self):
        return f"Player({self.name}, {self.pokemon_selected}, {self.pokemon_awake}, {self.money}, {self.fun_fact}, {self.bag}) "

    def __str__(self):
        return self.name

    # Adds a new captured pokemon to player's pokemon collection
    def capture_pokemon(self, pokemon):
        pokemon.restore_hp() #restore pokemon being captured's HP
        self.pokemon_awake.append(pokemon)


class Pokeball:
    square_type = 4

    def __init__(self, pokemon_inside):
        self.pokemon_inside = pokemon_inside


class Move:
    def __init__(self, move_id, move_name, attack_power, move_description=""):
        self.move_id = move_id
        self.move_name = move_name
        self.attack_power = attack_power
        self.move_description = move_description

    def __repr__(self):
        return f"Move({self.move_id}, {self.move_name}, {self.attack_power}, {self.move_description})"

    def __str__(self):
        return f"{self.move_name}"


class HealingItem:
    square_type = 5

    def __init__(self, name, restore_amount):
        self.name = name
        self.restore_amount = restore_amount

    def __repr__(self):
        return f"Move({self.name}, {self.restore_amount})"

    def __str__(self):
        return f"{self.name}"



