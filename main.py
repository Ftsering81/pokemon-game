# Name: Fnu Tsering

import time
import random
import sys
from termcolor import colored
from classes import Grid, Player, Pokemon, Pokeball, Trainer, Move, HealingItem


def start_game(game_map, player):
    print(colored(f"\nWelcome to Pokemon {player.name}!\n", 'cyan'))

    # Display the list of starter Pokemon to player
    print("Below are the options for your starter pokemon: ")
    pokemon_awake = create_pokemons()
    for key, value in pokemon_awake.items():
        if key <= 3:  # only print the first 3 pokemons from the dict
            print(f"{key}: {value.name}  ", end=" ")
        else:
            break
    print('\n')

    # Make player choose a starter pokemon
    while True:
        selected_pokemon_id = input(colored("Enter the number of the pokemon you wish to choose: ", 'green'))
        if selected_pokemon_id == '1' or selected_pokemon_id == '2' or selected_pokemon_id == '3':
            player.pokemon_selected = pokemon_awake[int(selected_pokemon_id)]
            player.pokemon_awake.append(player.pokemon_selected)  # add the chosen pokemon to player's pokemon list
            break
        else:
            print("Enter a valid number.")

    # Show chosen pokemon to player
    print(colored(f"\nYou've chosen {pokemon_awake[int(selected_pokemon_id)]}!\n", 'cyan'))

    # Display the map to the player if user hits ENTER
    enter_map = input(colored("Hit ENTER to enter the map", 'green'))
    if enter_map == '':
        start_pos = [0, 0]
        game_map.player_current_pos = start_pos
        print("Your position on the map is marked by \U0000274C")
        print("To move throughout the map, use [W] for up, [S] for down, [A] for left and [D] for right.")

        navigate_map(game_map, player, start_pos)  # Let player navigate through the map and play the game
        # If player collects 4 pokemon while navigating throughout the game, they win the game.
        # If all of their pokemon faint while navigating throughout the map, then they lose the game.
    else:
        exit()  # exit game if user doesn't want to enter the map


# This function allows player to navigate throughout the map/grid based on player input
def navigate_map(game_map, player, current_pos):
    while True:
        player_curr_row, player_curr_col = current_pos[0], current_pos[1]
        player_curr_square = game_map.squares[player_curr_row][
            player_curr_col]  # player's initial position is [0,0]
        player_curr_square.player_present = True  # mark the player's current square as player present
        print_grid(game_map)  # display map after each user input for direction

        # Prompt user for direction they want to move to
        direction = input(colored("Enter [W][S][A][D] for direction: ", 'green'))
        direction = direction.lower()
        valid_entries = ['w', 's', 'a', 'd', 'exit']
        while direction not in valid_entries:  # keeps prompting until valid direction is provided
            print("Invalid key.")
            direction = input(colored("Enter [W][S][A][D] for direction and 'exit' to end the game: ", 'green'))

        potential_new_pos = []
        if direction == 'w':  # one row up
            potential_new_pos = [player_curr_row - 1, player_curr_col]
        elif direction == 's':
            potential_new_pos = [player_curr_row + 1, player_curr_col]
        elif direction == 'a':
            potential_new_pos = [player_curr_row, player_curr_col - 1]
        elif direction == 'd':
            potential_new_pos = [player_curr_row, player_curr_col + 1]
        elif direction == "exit":
            print("Thanks for playing!")
            break
        potential_new_row = potential_new_pos[0]
        potential_new_col = potential_new_pos[1]

        if potential_new_row < 0 or potential_new_row >= game_map.num_rows or \
                potential_new_col < 0 or potential_new_col >= game_map.num_cols:
            print("Out of bounds. Enter a different direction.\n")
        else:  # Potential new square is within bounds of the map
            potential_new_square = game_map.squares[potential_new_row][potential_new_col]
            # move_to_new_square returns a boolean value. True if move to potential_new_square is possible. False otherwise
            move_possible = move_to_new_square(potential_new_square, player)
            if move_possible:
                player_curr_square.player_present = False  # set old square's player_present to False since player moved
                current_pos = [potential_new_row, potential_new_col]  # update current position to new position
                # with the next loop, the square at current_pos will be marked as True for player_present
                # and new grid will be printed


# This function determines whether movement to the square player wants to move to is possible or not
# and alerts and provides player with options if there is something at the square.
def move_to_new_square(new_square, player):
    square_type = new_square.square_type
    move_possible = True

    if square_type == 0:
        print()
        print(colored("Inaccessible square!\nGo to a different direction.", 'cyan'))
        return not move_possible

    elif square_type == 1:
        return move_possible

    # either trainer or wild pokemon at square, enter battle sequence. If pl
    elif square_type == 2 or square_type == 3:
        enemy = new_square.thing_present  # trainer or wild pokemon
        player_won_battle = battle_sequence(enemy, square_type, player)  # true if player wins the battle.

        # Check if game is over after each battle aka check if player collected more than 4 pokemon
        # or if all of player's pokemon fainted
        check_if_game_over(player)  # If game over, program terminates here. No move needed.

        # If game is not over: player still in game
        if player_won_battle:  # player won the battle against the trainerr or wild pokemon
            new_square.square_type = 1
            new_square.thing_present = None  # this square is now empty bc player defeated the enemy
            return move_possible  # bc square is now empty
        else:  # player ran away from the battle or lost to the trainer
            return not move_possible  # cannot move to the square since enemy is still there

    elif square_type == 4:  # 4 = pokeballs
        pokeball_found = new_square.thing_present
        pokemon_inside = pokeball_found.pokemon_inside
        player.capture_pokemon(pokemon_inside)  # add new pokemon to player's pokemon list

        # Check if game is over after a new pokemon collected
        check_if_game_over(player)  # If game over, program terminates here

        # If game is not over: player still hasnt collected more than 4 pokemon
        new_square.square_type = 1
        new_square.thing_present = None  # this square is now empty since player took the pokeball

        message = colored(f"\nCongrats, you found a pokeball! \nIt contained a {pokemon_inside}!", 'cyan')
        print_slow(message)
        return move_possible

    elif square_type == 5:  # an item is present at the square
        item_found = new_square.thing_present
        player.bag.append(item_found)  # add item found to player's bag
        print_slow(colored(f"\nCongrats, you found a healing item! \nIt's a {item_found.name}.", 'cyan'))
        print_slow(colored(f"It can restore a pokemon's HP by {item_found.restore_amount}", 'cyan'))
        new_square.square_type = 1
        new_square.thing_present = None  # this square is now empty bc player can move to this square and get the item
        return move_possible


# This function executes the battle sequence between the player and player's enemy (wild pokemon or trainor).
# Returns True only if player wins the battle against the enemy.
# Returns False if player loses the battle (all of player's pokemon faint) or runs away.
def battle_sequence(enemy, enemy_type, player):
    if enemy_type == 2:  # enemy is a trainer
        print_slow(
            colored(f"\n{enemy.name} wants to battle!\nFun fact about {enemy.name}: {enemy.fun_fact}.\n", 'cyan'))
        print_slow(colored(f"{enemy.name} sent out {enemy.pokemon_selected.name.upper()}!", 'magenta'))
    elif enemy_type == 3:  # enemy is a wild pokemon
        print_slow(colored(f"\nA wild {enemy.name.upper()} appeared!", 'cyan'))
    print_slow(colored(f"Your current Pokemon is {player.pokemon_selected.name.upper()}.", 'cyan'))

    # Loops until all of player's Pokemon faint or player chooses to run away from the battle or player wins the battle
    while True:
        print("\nWhat would you like to do?\n1. Run  2. Fight  3. Switch Pokemon  4. Items\n")
        player_choice = input(colored("Enter the number of option you want to choose: ", 'green'))

        # Player chooses to run away
        if player_choice == '1':
            print(colored("\nYou ran away successfully.\nYou're back to your original square.", 'cyan'))
            return False

        # Player chooses to fight and enemy is a wild pokemon
        elif player_choice == '2' and enemy_type == 3:
            player_won_fight = fight_sequence(player, enemy)

            if player_won_fight:
                player.capture_pokemon(enemy)  # player defeated and captured the wild pokemon
                return True  # signal that the player won the battle against the wild pokemon
            else:  # player's pokemon was defeated/fainted
                player.pokemon_fainted.append(player.pokemon_selected)  # add player's pokemon to fainted list
                player.pokemon_awake.remove(player.pokemon_selected)  # remove the pokemon from player's awake list
                if len(player.pokemon_awake) > 0:  # make player change their pokemon_selected to one that is awake
                    print(colored("Choose another pokemon.", 'blue'))
                    switch_pokemon(player)
                    continue  # prints the options again giving player option to run away or keep fighting same pokemon
                else:
                    return False  # player lost battle.

        # Player chooses to fight and enemy is a trainer
        elif player_choice == '2' and enemy_type == 2:
            while True:  # loops until all of trainer's pokemon faints or all of the player's pokemon faint
                player_won_fight = fight_sequence(player, enemy.pokemon_selected)

                if player_won_fight:  # Player's pokemon won the fight
                    enemy.pokemon_fainted.append(enemy.pokemon_selected)
                    enemy.pokemon_awake.remove(enemy.pokemon_selected)
                    if len(enemy.pokemon_awake) > 0:  # if enemy still has awake pokemon left
                        enemy.change_pokemon(enemy.pokemon_awake[0])  # select the next awake pokemon for the enemy
                        print(colored(f"\n{enemy.name} still has {len(enemy.pokemon_awake)} Pokemon to use.", 'cyan'))
                        print(colored(f"{enemy.name} sent out {enemy.pokemon_selected.name.upper()}!", 'magenta'))
                        break  # so player can get options to run away, switch pokemon or fight again

                    else:  # enemy has no more pokemon left
                        print_slow(colored(f"\nCongrats, you won the battle against {enemy.name}!", 'cyan'))
                        print_slow(colored(
                            f"You won ${enemy.money} of {enemy.name}'s money and all of their pokemon you defeated.",
                            'cyan'))
                        for pokemon in enemy.pokemon_fainted:  # capture all of enemy's pokemon and money
                            player.capture_pokemon(pokemon)
                        player.money = player.money + enemy.money
                        enemy.money = 0.00
                        return True  # signal player won battle

                else:  # enemy pokemon won the fight
                    player.pokemon_fainted.append(player.pokemon_selected)  # add player's pokemon to fainted list
                    player.pokemon_awake.remove(player.pokemon_selected)  # remove the pokemon from awake list
                    if len(player.pokemon_awake) > 0:  # player still has awake pokemon left
                        print(colored("Choose another pokemon.", 'blue'))
                        switch_pokemon(player)
                    else:  # player no longer has pokemon left. Player lost battle!
                        return False  # signal player lost battle!

        # Player chooses to switch pokemon
        elif player_choice == '3':
            switch_pokemon(player)

        # Player chooses to open bag and view items
        elif player_choice == '4':
            show_items(player)
            if len(player.bag) == 0:  # Bag has no items
                while True:
                    option = input(colored("Enter [B] to go back to options: ", 'green'))
                    option.lower()
                    if option == 'b':
                        break
                    else:
                        print("Enter a valid input.")
                continue  # go back to options
            else:  # Bag has items that can be used
                while True:
                    option = input(colored("Enter [I] to use an item or [B] to go back to options: ", 'green'))
                    option = option.lower()
                    if option == 'i' or option == 'b':
                        break
                    else:
                        print("Enter a valid input.")

                if option == 'b':
                    continue  # player back to options
                elif option == 'i':  # user wants to use item
                    show_items(player)
                    while True:
                        item_num = int(input(colored("Enter the number of the item you want to use: ", 'green')))
                        if 0 < item_num <= len(player.bag):
                            item_chosen = player.bag[item_num - 1]
                            use_item(item_chosen,
                                     player)  # ask player which one of their pokemon they want to use the item on
                            break
                        else:
                            print("\nEnter a valid choice")

        else:  # Invalid choice value
            print("Please enter a valid input.")

# This function checks if player won or lost by checking if player has collected 4 or more pokemons
# or if all of player's pokemon fainted.
def check_if_game_over(player):
    if len(player.pokemon_awake) >= 5:  # player won the game(collected 4 new pokemon)
        print_slow(colored("\n-------------------- CONGRATULATIONS! YOU WON THE GAME! --------------------", 'blue'))
        print_slow(colored(f"You collected ${player.money} and the following pokemon: ", 'blue'))
        for idx, pokemon in enumerate(player.pokemon_awake):
            print(colored(f"[{idx + 1}] {pokemon}", 'blue'))
        exit()  # exit the game

    elif len(player.pokemon_awake) <= 0:  # player lost the battle bc all of their pokemon fainted
        print_slow(colored("\nAll of your Pokemon fainted!\n", 'red'))
        print_slow(colored("-------------------- You lost! Game Over! --------------------\n", 'red'))
        exit()


# This function executes the fight between player's chosen pokemon and the enemy pokemon.
# Returns True if player's pokemon defeats enemy pokemon. Otherwise, returns False.
def fight_sequence(player, enemy):
    print_slow(colored(f"\nGo! {player.pokemon_selected.name.upper()}!", 'yellow'))
    print_slow(
        f"\n-------------------- {player.pokemon_selected.name.upper()} vs {enemy.name.upper()} --------------------")
    selected_pokemon_moves = player.pokemon_selected.moves

    while True:
        # print health points of both Pokemon
        print(colored(
            f"\n{player.pokemon_selected}'s HP: {player.pokemon_selected.health_points}/{player.pokemon_selected.base_hp}",
            'yellow'), end='')
        print("  |  ", end='')
        print(colored(f"{enemy.name}'s HP: {enemy.health_points}/{enemy.base_hp}\n", 'magenta'))

        # Show the player the moves their pokemon can use and ask them to choose one
        print(f"These are the moves {player.pokemon_selected.name.upper()} can use: ")
        for idx, move in enumerate(selected_pokemon_moves):
            print(f"[{idx + 1}] Name: {move.move_name}, Attack Power: {move.attack_power}")
        while True:  # Get input from player on which move to use for their pokemon
            move_chosen_num = int(input(colored("\nEnter the number of the move you want to use: ", 'green')))
            if move_chosen_num >= 1 and move_chosen_num <= len(selected_pokemon_moves):
                break
            else:
                print("Enter valid input for move.")
        print("-------------------------------------------------------------\n")
        move_selected = selected_pokemon_moves[move_chosen_num - 1]

        # make the enemy pokemon choose a move as well
        wild_pokemon_move = random.choice(enemy.moves)

        # randomly decide who gets to attack first
        random_num = random.randrange(2)
        player_attacked = False
        for i in range(2):
            if random_num == 0 and player_attacked is False:  # player goes first if True
                player.pokemon_selected.attack(enemy, move_selected)
                wild_pokemon_defeated = enemy.health_points == 0
                player_attacked = True
                print_slow(colored(f"{player.pokemon_selected} used {move_selected.move_name}", 'yellow'))
                if wild_pokemon_defeated:
                    print_slow(colored(f"\nEnemy {enemy.name.upper()} fainted!", 'red'))
                    return True  # player defeated enemy pokemon
            else:  # random_num was 1 or player already attacked
                enemy.attack(player.pokemon_selected, wild_pokemon_move)
                player_pokemon_defeated = player.pokemon_selected.health_points == 0
                random_num = 0  # set random_num to 0 so player can go next if wild pokemon went first
                print_slow(colored(f"{enemy.name} used {wild_pokemon_move.move_name}", 'magenta'))
                if player_pokemon_defeated is True:
                    print_slow(colored(f"\nYour {player.pokemon_selected.name.upper()} fainted!", 'red'))
                    return False  # enemy pokemon defeated player


# This function shows player the list of items in their bag
def show_items(player):
    print(f"\nYour Items: ")
    if len(player.bag) == 0:
        print("Your bag is empty!")
    else:
        for idx, item in enumerate(player.bag):
            print(f"[{idx + 1}] Item: {item.name}, Description: Restores a pokemon's health by {item.restore_amount}")
        print()


# This function asks player which pokemon they want to use the healing item on and applies it to that pokemon
def use_item(item, player):
    while True:
        show_pokemons(player)
        while True:
            pokemon_chosen_num = int(input(colored("Enter the number of Pokemon you want to use item on: ", 'green')))
            if pokemon_chosen_num > 0 and pokemon_chosen_num <= len(player.pokemon_awake):
                break
            else:
                print("Enter a valid input.")
        # Use the item on the pokemon. Can only use item on pokemon that haven't fainted
        pokemon = player.pokemon_awake[pokemon_chosen_num - 1]
        if pokemon.health_points == pokemon.base_hp:
            print(colored(f"{pokemon.name.upper()}'s HP is already at max. Cannot use item on this pokemon.", 'cyan'))
            break
        else:
            pokemon.health_points = pokemon.health_points + item.restore_amount
            if pokemon.health_points > pokemon.base_hp:  # dont exceed max health points
                pokemon.health_points = pokemon.base_hp
            player.bag.remove(item)
            print(colored(f"\nYou used {item.name} on {player.pokemon_awake[pokemon_chosen_num - 1]}.", 'cyan'))
            print(colored(f"Your {pokemon.name}'s HP is now {pokemon.health_points}/{pokemon.base_hp}.", 'cyan'))
            return


# This function displays the player's list of pokemon that are awake
def show_pokemons(player):
    print("\nYour Pokemons: ")
    for idx, pokemon in enumerate(player.pokemon_awake):
        print(
            f"[{idx + 1}] Name: {pokemon.name}  HP: {pokemon.health_points}/{pokemon.base_hp}  Attack Power: {pokemon.attack_power}")
    print()


# This function allows user to switch to a different pokemon from their list of awake pokemon
def switch_pokemon(player):
    while True:
        show_pokemons(player)
        while True:
            pokemon_chosen_num = int(input(colored("Enter the number of Pokemon you wish to switch to: ", 'green')))
            if pokemon_chosen_num > 0 and pokemon_chosen_num <= len(player.pokemon_awake):
                break
            else:
                print("Enter a valid input.")

        pokemon_chosen = player.pokemon_awake[pokemon_chosen_num - 1]
        if pokemon_chosen.health_points <= 0:
            print(colored("\nThe pokemon you chose has zero HP. Choose another Pokemon.", 'blue'))
        else:
            player.change_pokemon(pokemon_chosen)
            print(colored(f"\nYou switched to {player.pokemon_selected}!", 'cyan'))
            break


# This function creates and returns a dict of 12 Pokemons along with their moves defined
def create_pokemons():
    eevee_moves = [Move(3, "Dig", 100), Move(4, "Swift", 60)]
    charizard_moves = [Move(5, "Dragon Claw", 70), Move(6, "Fire Blast", 80)]
    pidgey_moves = [Move(7, "Twister", 45), Move(8, "Air Cutter", 60)]
    meowth_moves = [Move(9, "Dark Pulse", 80), Move(10, "Night Slash", 50)]
    seviper_moves = [Move(11, "Wrap", 60), Move(12, "Poison Fang", 35)]
    jigglypuff_moves = [Move(13, "Disarming Voice", 70), Move(14, "Dazzling Gleam", 100)]
    pikachu_moves = [Move(1, "Discharge", 65), Move(2, "thunderbolt", 80)]
    bulbasaur_moves = [Move(15, "Seed Bomb", 55), Move(16, "Power Whip", 90)]
    gengar_moves = [Move(17, "Shadow Ball", 100), Move(18, "Sludge Bomb", 80)]
    squirtle_moves = [Move(19, "Aqua Jet", 45), Move(20, "Water Pulse", 70)]
    snorlax_moves = [Move(21, "Earthquake", 140), Move(22, "Heavy Slam", 70)]
    ninetails_moves = [Move(23, "Heat Wave", 95), Move(24, "Solar Beam", 180)]  # strongest

    pokemon1 = Pokemon(1, "Eevee", health_points=220, attack_power=103, moves=eevee_moves)
    pokemon2 = Pokemon(2, "Charizard", health_points=266, attack_power=155, moves=charizard_moves)
    pokemon3 = Pokemon(3, "Pidgey", health_points=190, attack_power=85, moves=pidgey_moves)
    pokemon4 = Pokemon(4, "Meowth", health_points=190, attack_power=156, moves=meowth_moves)  # jessie
    pokemon5 = Pokemon(5, "Seviper", health_points=256, attack_power=100, moves=seviper_moves)  # jessie
    pokemon6 = Pokemon(6, "Jigglypuff", health_points=340, attack_power=85, moves=jigglypuff_moves)  # ash
    pokemon7 = Pokemon(7, "Pikachu", health_points=180, attack_power=103, moves=pikachu_moves)  # ash
    pokemon8 = Pokemon(8, "Bulbasaur", health_points=200, attack_power=92, moves=bulbasaur_moves)  # pokeball
    pokemon9 = Pokemon(9, "Ninetales", health_points=300, attack_power=200, moves=ninetails_moves)  # pokeball
    pokemon10 = Pokemon(10, "Squirtle", health_points=198, attack_power=90, moves=squirtle_moves,
                        wild=True)  # wild_pokemon
    pokemon11 = Pokemon(11, "Snorlax", health_points=430, attack_power=202, moves=snorlax_moves,
                        wild=True)  # wild pokemon
    pokemon12 = Pokemon(12, "Gengar", health_points=230, attack_power=121, moves=gengar_moves,
                        wild=True)  # wild pokemon

    pokemon_dict = {pokemon1.pokemon_id: pokemon1, pokemon2.pokemon_id: pokemon2, pokemon3.pokemon_id: pokemon3,
                    pokemon4.pokemon_id: pokemon4, pokemon5.pokemon_id: pokemon5, pokemon6.pokemon_id: pokemon6,
                    pokemon7.pokemon_id: pokemon7, pokemon8.pokemon_id: pokemon8, pokemon9.pokemon_id: pokemon9,
                    pokemon10.pokemon_id: pokemon10, pokemon11.pokemon_id: pokemon11, pokemon12.pokemon_id: pokemon12}
    return pokemon_dict


# This function creates the map for the game by adding the pokemon, pokeballs, trainers and items to the grid
# and by defining which squares are accessible and which are not.
def create_map(grid):
    # Create 10 Pokemon for the game
    pokemon_dict = create_pokemons()  # returns a dict with 12 different Pokemon

    # Create 2 Pokeballs for the game
    pokeball1 = Pokeball(pokemon_dict[8])  # Bulbasaur
    pokeball2 = Pokeball(pokemon_dict[9])  # Ninetails

    # Create 2 trainers for the game
    trainer1_description = "Ash is generally kind, brave, enthusiastic, passionate and adventurous."
    trainer1 = Trainer("Ash", pokemon_dict[7], [pokemon_dict[7], pokemon_dict[6]], 300, trainer1_description)
    trainer2_description = "Jessie's goal is to capture Pokémon and use them to rule the world."
    trainer2 = Trainer("Jessie", pokemon_dict[4], [pokemon_dict[4], pokemon_dict[5]], 100, trainer2_description)

    # 3 wild pokemon to add to game
    wild_pokemon1 = pokemon_dict[10]  # Squirtle
    wild_pokemon2 = pokemon_dict[11]  # Snorlax
    wild_pokemon3 = pokemon_dict[12]  # Gengar

    # 4 healing potion items
    item1 = HealingItem("Lemonade", 70)
    item2 = HealingItem("Moo Moo Milk", 100)
    item3 = HealingItem("Super Pop", 60)

    things_to_add_to_grid = [pokeball1, pokeball2, trainer1, trainer2, wild_pokemon1, wild_pokemon2, wild_pokemon3,
                             item1, item2, item3]

    # Defining the inaccessible squares in the 10x10 grid
    for row in range(0, 2):
        for col in range(2, 10):
            if col != 5 and col != 6:
                grid.squares[row][col].square_type = 0

    for row in range(2, 4):
        for col in range(8, 10):
            grid.squares[row][col].square_type = 0

    for row in range(4, 6):
        for col in range(3, 7):
            grid.squares[row][col].square_type = 0

    for col in range(0, 3): # for row 7
        grid.squares[7][col].square_type = 0

    for row in range(8, 10):
        for col in range(10):
            if col <= 2 or col >= 6:
                grid.squares[row][col].square_type = 0

    # Add all the pokeballs, wild pokemon and trainors to random accessible squares of the grid
    while len(things_to_add_to_grid) != 0:
        row = random.randrange(grid.num_rows)  # random number from 0 to num_rows-1
        col = random.randrange(grid.num_cols)  # random number from 0 to num_rows-1

        square = grid.squares[row][col]  # square references the grid square at [row][col]
        if square.square_type != 0 and [row, col] != [0, 0]: #let [0,0] be empty since it's player's start pos
            square.thing_present = things_to_add_to_grid.pop()
            # specify the square_type to represent what type of thing the square has
            square.square_type = square.thing_present.square_type

    return grid  # return the upgraded grid


# Prints the grid with emojis
def print_grid(grid):
    print()
    for i in range(grid.num_rows):
        for j in range(grid.num_cols):
            square = grid.squares[i][j]
            if square.player_present is False:
                if square.square_type == 0:  # tree and blue square emojis to represent inaccessible empty square
                    if (4 <= i <= 5) and (3 <= j <= 6): # blue square to create lake
                        print("\U0001F7E6", end=" ")
                    else:
                        print("\U0001F333", end=" ") # tree
                elif square.square_type == 1: #square emoji to represent accessible empty squares
                    print("\U0001F7E8", end=" ")  # empty space
                elif square.square_type == 2:
                    print("\U0001F9DD", end=" ")  # trainer
                elif square.square_type == 3: #panda for pokemon
                    print("\U0001F43C", end=" ")
                elif square.square_type == 4:
                    print("\U0001F534", end=" ")  # Ball
                elif square.square_type == 5:
                    print("\U0001F95B", end=" ")
            else:
                print("\U0000274C", end=" ")
        print()
    print()  # extra line after the grid



def print_slow(message):
    for letter in message:  # prints the message letter by letter
        sys.stdout.write(letter)
        time.sleep(.03)
    print()  # newline


if __name__ == '__main__':

    # Build a 10x10 grid for the game
    the_grid = Grid(10, 10)

    # add all the pokemons, pokeballs and trainors to the empty grid to make it into a map
    the_map = create_map(the_grid)

    # Create player for user
    player_name = input(colored("Enter your name: ", 'green'))
    the_player = Player(player_name.capitalize())

    start = input(colored("Hit ENTER to start the game ", 'green'))
    if start == '':
        start_game(the_map, the_player)
    else:
        exit()
