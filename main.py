from pprint import pprint
import time
import random


def start_game(grid, player):

    print("\nWelcome to Pokemon!\n")

    # Display the list of Pokemon, along with their pokemon ids to the user to show them options for
    # their starter pokemon
    print("Below is the list of Pokemon from which you can select one as your starter pokemon: ")

    starter_pokemons = {1: pokemon_dict[1], 2: pokemon_dict[2], 3: pokemon_dict[3]}
    for key, value in starter_pokemons.items():
        print(f"{key}: {value.name}  ", end=" ")

    # Make player choose a starter pokemon
    while True:
        selected_pokemon_id = int(input("\nEnter the number of the pokemon you wish to choose: "))
        if 1 <= selected_pokemon_id <= 3:  # breaks only if user enters valid input, or keep asking for same input
            player.pokemon_selected = starter_pokemons[selected_pokemon_id]
            player.pokemon_list.append(player.pokemon_selected)  # add the chosen pokemon to player's pokemon list
            break
    print(f"You've chosen {starter_pokemons[selected_pokemon_id]}!\n")

    #Display the map to the player if user hits ENTER
    enter_map = input("Hit ENTER to enter the map")
    if enter_map == '':
        print("Your position on the map is marked by \U0000274C")
        print("To move throughout the map, use [W] for up, [S] for down, [A] for left and [D] for right." )
        # Prompt user for direction to move throughout the grid
        # grid.enter_grid()
        # grid.print_grid()
        grid.navigate_grid()
    else:
        exit() #exit game if user doesn't want to enter the map



class Grid:
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols

        self.player_number = 7
        self.player_current_pos = [0, 0]  # initialized to [0,0]

        # Add empty squares to the grid.
        self.grid_with_squares = [[Square() for j in range(num_cols)] for i in
                                  range(num_rows)]  # creates a 2D grid filled with objects of class Square



    def __repr__(self):
        rep = f"Grid({self.num_rows}, {self.num_cols})"
        return rep

    def __str__(self):
        return f"The size of your grid is {self.num_rows}x{self.num_cols}"

    # def add_square_types(self):
    #     square_types = [0, 1, 2, 3, 4, 5]
    #     for row in range(self.num_rows):
    #         for col in range(self.num_cols):
    #             square = self.grid_with_squares[row][col]
    #             square.square_type = random.choice(square_types)

    # def enter_grid(self):
    #     player_start_pos = self.player_current_pos  # starting position
    #     player_curr_square = self.grid_with_squares[player_start_pos[0]][player_start_pos[1]] #[0][0]
    #     player_curr_square.player_present = True #mark the player's current square as player present

    def navigate_grid(self):
        player_start_pos = self.player_current_pos  # starting position
        player_curr_square = self.grid_with_squares[player_start_pos[0]][player_start_pos[1]] #[0][0]
        player_curr_square.player_present = True #mark the player's current square as player present
        self.print_grid()

        while True:
            player_curr_row, player_curr_col = self.player_current_pos[0], self.player_current_pos[1]
            direction = input("Enter [W][S][A][D] for direction:")
            direction = direction.lower()
            valid_entries = ['w', 's', 'a', 'd', 'exit']
            while direction not in valid_entries:  # keeps prompting for direction until valid direction is provided
                direction = input("Invalid key.\nEnter [W][S][A][D] for direction and 'exit' to end the game: ")

            if direction == 'w':  # one row up
                potential_new_row = player_curr_row - 1
                if potential_new_row < 0 or potential_new_row >= self.num_rows:
                    print("Out of bounds. Enter a different direction.\n")
                else:  # in bounds
                    player_new_pos = [potential_new_row, player_curr_col]  # curr is now the new position
                    player_curr_square.player_present = False
                    player_new_square = self.grid_with_squares[player_new_pos[0]][player_new_pos[1]]
                    player_new_square.player_present = True
                    self.player_current_pos = player_new_pos
                    player_curr_square = player_new_square
                    self.print_grid()
            elif direction == 's':  # one row down
                potential_new_row = player_curr_row + 1
                if potential_new_row < 0 or potential_new_row >= self.num_rows:
                    print("Out of bounds. Enter a different direction.\n")
                else:  # in bounds
                    player_new_pos = [potential_new_row, player_curr_col]  # curr is now the new position
                    player_curr_square.player_present = False
                    player_new_square = self.grid_with_squares[player_new_pos[0]][player_new_pos[1]]
                    player_new_square.player_present = True
                    self.player_current_pos = player_new_pos
                    player_curr_square = player_new_square

                    self.print_grid()
            elif direction == 'a':
                potential_new_col = player_curr_col - 1
                if potential_new_col < 0 or potential_new_col >= self.num_cols:
                    print("Out of bounds. Enter a different direction.\n")
                else:  # in bounds
                    player_new_pos = [player_curr_row, potential_new_col]  # curr is now the new position
                    player_curr_square.player_present = False
                    player_new_square = self.grid_with_squares[player_new_pos[0]][player_new_pos[1]]
                    player_new_square.player_present = True
                    self.player_current_pos = player_new_pos
                    player_curr_square = player_new_square
                    self.print_grid()
            elif direction == 'd':
                potential_new_col = player_curr_col + 1
                if potential_new_col < 0 or potential_new_col >= self.num_cols:
                    print("Out of bounds. Enter a different direction.\n")
                else:  # in bounds
                    player_new_pos = [player_curr_row, potential_new_col]  # curr is now the new position
                    player_curr_square.player_present = False
                    player_new_square = self.grid_with_squares[player_new_pos[0]][player_new_pos[1]]
                    player_new_square.player_present = True
                    self.player_current_pos = player_new_pos
                    player_curr_square = player_new_square
                    self.print_grid()
            elif direction == 'exit':
                print("Thanks for playing")
                break

    def print_grid(self):
        print() #print extraline before grid
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                square = self.grid_with_squares[i][j]
                if square.player_present is False:
                    if square.square_type == 0:
                        print("\U0001f335", end=" ")  # cactus emoji to represent inaccessible empty square
                    elif square.square_type == 1:  # yellow square emoji to represent accessible empty squares
                        print("\U0001F7E8", end=" ")  # empty space
                    elif square.square_type == 2:
                        print("\U0001F9B9", end=" ")  # trainer
                    elif square.square_type == 3:
                        print("\U0001F409", end=" ")  # dragon emoji to represent Pokemons
                    elif square.square_type == 4:
                        print("\U0001F534", end=" ")  # Ball
                else:
                    print("\U0000274C", end=" ")
            print()
        print() #extra line after the grid
        print("\n")
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                square = self.grid_with_squares[i][j]
                if square.player_present is False:
                    print(f'[{square.square_type}]', end="")
                else:
                    print(f'[{self.player_number}]', end="")
            print()


class Square:

    def __init__(self, square_type: int = 0, player_present: bool = False, thing_present=None):
        # square_type will be an integer that represent what kind of square it is or what is on the square:
        # 0 represents an inaccessible spot, 1 an accesible spot, 2 an item, 3 a Pokemon, 4 a Pokeball and a 5 a CPU-trainer.
        # Any integer that is not 0-5 will represent the square where the player currently is at.
        self.square_type = square_type
        self.player_present = player_present
        self.thing_present = thing_present

    def __repr__(self):
        rep = f"Square({self.square_type})"
        return rep

    def __str__(self):
        return f"{self.square_type}"


class Player:
    def __init__(self, pokemon_selected=None, pokemon_list=[], money=0.00):
        self.pokemon_selected = pokemon_selected
        self.pokemon_list = pokemon_list
        self.money = money


class Pokemon:
    square_type = 3
    def __init__(self, pokemon_id, name, health_points, attack_power):
        self.pokemon_id = pokemon_id
        self.name = name
        self.health_points = health_points
        self.attack_power = attack_power
        # self.moves_list = moves_list

    def __repr__(self):
        return f"Pokemon({self.pokemon_id}, {self.name}, {self.health_points}, {self.attack_power})"

    def __str__(self):
        return self.name


class Trainer:
    square_type = 2
    def __init__(self, name, pokemon_selected, pokemon_owned, money, fun_fact=""):
        self.name = name
        self.pokemon_selected = pokemon_selected
        self.pokemon_owned = pokemon_owned
        self.money = money
        self.fun_fact = fun_fact


class Pokeball:
    square_type = 4
    def __init__(self, pokemon_inside):
        self.pokemon_inside = pokemon_inside


# This function creates and returns a dict of 12 Pokemons
def create_pokemons():
    pokemon1 = Pokemon(1, "Eevee", health_points=55, attack_power=55)
    pokemon2 = Pokemon(2, "Charizard", health_points=78, attack_power=84)
    pokemon3 = Pokemon(3, "Pidgey", health_points=40, attack_power=45)
    pokemon4 = Pokemon(4, "Meowth", health_points=40, attack_power=45)  # jessie
    pokemon5 = Pokemon(5, "Seviper", health_points=73, attack_power=100) #jessie
    pokemon6 = Pokemon(6, "Jigglypuff", health_points=115, attack_power=45) #ash
    pokemon7 = Pokemon(7, "Bulbasaur", health_points=45, attack_power=49) # ash
    pokemon8 = Pokemon(8, "Pikachu", health_points=35, attack_power=55) #ash
    pokemon9 = Pokemon(9, "Ditto", health_points=48, attack_power=48) #pokeball
    pokemon10 = Pokemon(10, "Squirtle", health_points=44, attack_power=48) #pokeball
    pokemon11 = Pokemon(11, "Snorlax", health_points=160, attack_power=110) #pokeball
    pokemon12 = Pokemon(12, "Ninetales", health_points=73, attack_power=76) #pokeball

    pokemon_dict = {pokemon1.pokemon_id: pokemon1, pokemon2.pokemon_id: pokemon2, pokemon3.pokemon_id: pokemon3,
                    pokemon4.pokemon_id: pokemon4, pokemon5.pokemon_id: pokemon5, pokemon6.pokemon_id: pokemon6,
                    pokemon7.pokemon_id: pokemon7, pokemon8.pokemon_id: pokemon8, pokemon9.pokemon_id: pokemon9,
                    pokemon10.pokemon_id: pokemon10, pokemon11.pokemon_id: pokemon11, pokemon12.pokemon_id: pokemon12}
    return pokemon_dict


if __name__ == '__main__':
    # Build a 5x5 grid for the game
    grid = Grid(5, 5)

    # Create a player
    player = Player()

    # Create 10 Pokemon for the game
    pokemon_dict = create_pokemons() #returns a dict with 10 different Pokemon

    #Create 4 Pokeballs for the game
    pokeball1 = Pokeball(pokemon_dict[9]) #Ditto
    pokeball2 = Pokeball(pokemon_dict[10]) #Squirtle
    pokeball3 = Pokeball(pokemon_dict[11]) #Snorlax
    pokeball4 = Pokeball(pokemon_dict[12]) #Ninetails

    #Create trainers for the game
    trainer1_description = "Ash is generally kind, brave, enthusiastic, passionate and adventurous."
    trainer1 = Trainer("Ash", pokemon_dict[7], [pokemon_dict[7], pokemon_dict[6], pokemon_dict[8]], 300, trainer1_description)

    trainer2_description = "Jessie's goal is to capture Pokémon and use them to rule the world."
    trainer2 = Trainer("Jessie", pokemon_dict[4], [pokemon_dict[4], pokemon_dict[5]], 100, trainer2_description)

    things_to_add_to_grid = [pokeball1, pokeball2, pokeball3, pokeball4, trainer1, trainer2]

    while len(things_to_add_to_grid) != 0:
        row = random.randrange(grid.num_rows) #random number from 0 to num_rows-1
        col = random.randrange(grid.num_cols) #random number from 0 to num_rows-1

        square = grid.grid_with_squares[row][col]  # square references the grid square at [row][col]
        if row == 0 and col == 0:
            # since [0,0] is the player's starting position,
            # we want it to be an accessible square with just the player.
            square.square_type = 1
        else:  # assign square type 0 or 1 to each square randomly
            square.thing_present = things_to_add_to_grid.pop()
            square.square_type = square.thing_present.square_type


    for row in range(grid.num_rows):
        for col in range(grid.num_cols):
            square = grid.grid_with_squares[row][col]  # square references the grid square at [row][col]
            if row == 0 and col == 0:
                square.square_type = 1
            elif square.square_type == 0 or square.square_type == 1: # assign square type 0 or 1 to each square randomly
                square.square_type = random.choices(population=[0, 1], weights=[0.3, 0.7])[0]
            else: #if square type is 2-4, then skip
                pass



    start = input("Hit ENTER to start the game")
    if start == '':
        start_game(grid, player)
    else:
        exit()

