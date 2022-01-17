# By submitting this assignment, I agree to the following:
#  �Aggies do not lie, cheat, or steal, or tolerate those who do�
#  �I have not given or received any unauthorized aid on this assignment�
#
# Name:         Tom Saunders, Hailie Connell, Nick Johannesen, Christina Ojeas
# Team:         11
# Section:      201
# Assignment:   lab13
# Date:         11-6-20

#Single-Player
#import statements
import csv
import random
import pygame
from time import sleep
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
#initialize pygame mixer with sounds
pygame.mixer.init()
battle_sound=pygame.mixer.Sound("battle_sound.mp3")
victory_sound=pygame.mixer.Sound('victory_sound.mp3')
background=pygame.mixer.Sound('background.mp3')
pygame.mixer.quit()



def rand_pokemon():
    ''' (Tom) reads the given list of pokemon in a csv file and stores as a list of lists, then generates a
    random number between 0 and 150- inclusive- and returns the list at that index in the list of lists.
    Each list in the list of lists has an '''
    with open('PokeList_v2.csv', 'r') as csvfile:
        names_list_reader=csv.reader(csvfile, delimiter=',')
        row_num=int(random.randrange(1, 151))
        names=[]
        level=int(random.randrange(1, 25))
        for p in names_list_reader:
            for x in range(150):
                pokemon=csvfile.readline().split(',')
                names.append(pokemon)
        for i in names:
            index=int(i[0])
            if index==row_num:
                i.append(level)
                i[3]=i[3][:-2]
                return i


def update_bag(list):
    ''' (Christina) This function opens the CSV file for player 1 bag and writes in the parameter list'''
    with open('player1bag.csv', 'a') as bag:
        names_list_writer = csv.writer(bag, delimiter=',')
        names_list_writer.writerow(list)


def select_pokemon():
    ''' (Christina) This function reads what is in the player1bag.csv and returns a list
    containing 'index', 'name', 'minCP', 'maxCP', 'current_level' of the Pokemon selected'''
    names_list_reader = csv.reader(open('player1bag.csv'))
    pokemon = list(names_list_reader)
    show_bag()
    try_again=0
    while try_again==0:
        select=str(input("\nEnter the name of the pokemon you wish to select(exactly as it appears in the bag above): "))
        index=int(0)
        for i in pokemon:
            if len(i)>2:
                if str(i[1])==select:
                    index=pokemon.index(i)
                    return list(pokemon[index])


def returnCP(selected_pokemon):
    ''' (Tom) Uses the given formula for calculating a pokemons CP to calculate the CP from the
    level (index 4) of the list passed to the function'''
    if len(selected_pokemon)==5:
        level=int(selected_pokemon[4])
    else:
        level=int(selected_pokemon[3])
    if level<=int(30):
        cp=(0.0094/(0.095*((level)**(1/2))))
        if cp>int(selected_pokemon[3]):
            cp=int(selected_pokemon[3])
        elif cp<int(selected_pokemon[2]):
            cp=int(selected_pokemon[2])
    else:
        cp=(0.0045 / (0.095 * ((level) ** (1 / 2))))
    return cp

def use_candy():
    ''' (Christina) Uses number of candies to level up a Pokemon and updates the file player1bag.csv'''
    global player1candies
    names_list_reader = csv.reader(open('player1bag.csv'))
    pokemon = list(names_list_reader)
    selected_pokemon = select_pokemon()
    if len(selected_pokemon)==5:
        level=int(selected_pokemon[4])
    else:
        level=int(selected_pokemon[3])
    if player1candies>=1:
        if level<30:
            level+=1
            print(selected_pokemon[1], "grew by 1 level, 1 candy was used...")
            if player1candies>0:
                player1candies-=1
        elif level>=30:
            if level<40:
                level+=1
                print(selected_pokemon[1], "grew by 1 level, 2 candies were used...")
                if player1candies>1:
                    player1candies-=2
    else:
        print("No candies to use")
    if len(selected_pokemon)==5:
        selected_pokemon[4]=str(int(selected_pokemon[4])+1)
    else:
        selected_pokemon[3]=str(int(selected_pokemon[3])+1)
    with open('player1bag.csv', 'r') as bag:
        names_list_reader = csv.reader(bag, delimiter=',')
        x=0
        backpack = list(names_list_reader)
        for i in backpack:
            if len(i)==5:
                if i[1]==selected_pokemon[1]:
                    if len(selected_pokemon)==5:
                        i[4]=selected_pokemon[4]
                    else:
                        i[3]=selected_pokemon[3]
    with open('player1bag.csv', 'w') as bag:
        names_list_writer = csv.writer(bag, delimiter=',')
        for i in backpack:
            names_list_writer.writerow(i)


def show_bag():
    '''(Christina) Shows the list of Pokemons available with their 'index', 'name', 'minCP', 'maxCP', 'current_level'
    in the file player1bag.csv'''
    global player1candies
    print("\n----------------------\033[0;31m [Player 1 Bag] \033[0m-----------------------".center(10))
    with open('player1bag.csv', 'r') as bag:
        names_list_reader = list(csv.reader(bag, delimiter=','))
        for i in names_list_reader:
            if len(i)==5:
                if i[1]!='name':
                    print('\n', i[1], '\b, Level:', i[4])
            else:
                bag.readline()
    print("\n\033[0;31m Player 1 candies: \033[0m", player1candies, "\n----------------------")


def main_menu():
    ''' (Tom) Prints the menu for the user-options'''
    print("\nEnter 1 to catch more pokemon, Enter 2 to view your bag, Enter 3 to Battle, Enter 4 to use candies, Enter 5 to switch players: \n")


def menu_selection():
    ''' (Christina) Displays the menu for user selection'''
    global current_p
    global change
    det=0
    inputs=['QUIT', '1', '2', '3', '4', '5']
    while det==0:
        main_menu()
        s=input("Enter your selection('QUIT'to quit): ")
        if s in inputs:
            det=1
    if s == 'QUIT':
        return s
    else:
        s=int(s)
    if s==1:
        caught_pokemon=catch_pokemon()
        if caught_pokemon[0]!='1':
            update_bag(caught_pokemon)
    elif s==2:
        show_bag()
    elif s==3:
        battle()
    elif s==4:
        use_candy()
    elif s==5:
        current_p=int(input('\nEnter the number of the player you wish to play as: '))
        change=True


def guessing_game(level):
    ''' (Tom) Generates random integer in a range (determined by level) and assigns it to num_catch.
    Then, asks the user to enter a number(int) in that range and returns True if the correct integer is guessed, otherwise False.'''
    determine=0
    while determine==0:
        print("Enter the correct integer to catch it")
        if level>=30:
            num_catch=int(random.randrange(1, 10))
            num=int(input("Enter an integer 1-10: \n"))
            if num==num_catch:
                return True
            else:
                return False
        elif 20<=level<30:
            num_catch = int(random.randrange(1, 7))
            num=int(input("Enter an integer 1-7: \n"))
            if num == num_catch:
                return True
            else:
                return False
        elif 10<=level<20:
            num_catch = int(random.randrange(1, 5))
            num=int(input("Enter an integer 1-5: \n"))
            if num == num_catch:
                return True
            else:
                return False
        elif 0<level<10:
            num_catch = int(random.randrange(1, 3))
            num=int(input("Enter an integer 1-3: \n"))
            if num == num_catch:
                play_sound('victory_sound.mp3', 4)
                return True
            else:
                return False
        else:
            return False



def catch_pokemon():
    ''' (Christina) Randomly selects and Pokemon to catch
    Get guess from player to determine if the Pokemon was caught
    Returns a list with 'index', 'name', 'minCP', 'maxCP', 'current_level' of the Pokemon caught
    And if no Pokemon caught returns '1' '''
    global player1candies
    global player1_num_pokemon
    enemy=rand_pokemon()
    level=enemy[4]
    print('\nA wild lvl.', level, enemy[1], 'appears...\n')
    if guessing_game(level) is True:
        play_sound('victory_sound.mp3', 3)
        sleep(0.75)
        print("lvl.", level, enemy[1], 'was caught!')
        candy=int(random.randrange(1, 4, 1))
        if candy==1:
            player1candies+=3
        elif candy==2:
            player1candies+=5
        else:
            player1candies+=10
        player1_num_pokemon+=1
        return enemy
    else:
        print('\n', enemy[1], 'escaped...')
        return '1'


def battle_screen(player1pokemon, enemy): #parameters=str()
    ''' (Christina) Pop up the battle screen to indicate that a battle is occuring
    the Pokemon the user picked vs. the enemy'''
    #create plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    #title plot "Pokemon 202 Maroon Edition
    fig.suptitle('Pokemon 2020 Maroon Edition', fontsize=20, fontweight='bold', color='maroon', alpha=1.0)
    #fill background red and hid axis'
    ax.text(4, 0, '_', color='black', alpha=0.0, fontsize=125, bbox={'facecolor': 'black', 'alpha': 0.95, 'pad': 190})
    ax.text(4, 0, '_', color='black', alpha=0.0, fontsize=125, bbox={'facecolor': 'maroon', 'alpha': 0.9, 'pad': 190})
    #plot("BATTLE!") bbox={'facecolor': 'red', 'alpha': 0.85, 'pad': 70}
    ax.text(0.25, 5, 'BATTLE!', style='italic', color='black', fontsize=85)
    #plot("player")
    ax.text(1.95, 1.9, r'(Player)', fontsize=10, fontweight='bold')
    #plot("opponent')
    ax.text(6.3, 1.9, r'(Opponent)', fontsize=10, fontweight='bold')
    #plot pokemon(player) vs. pokemon(opponent)
    ax.text(1, 3, player1pokemon, color='grey', alpha=1.0, fontsize=17, fontweight='bold', bbox={'facecolor': 'black', 'alpha': 0.85, 'pad': 10})
    ax.text(6.5, 3, enemy, color='grey', alpha=1.0, fontsize=17, fontweight='bold', bbox={'facecolor': 'black', 'alpha': 0.85, 'pad': 10})
    ax.text(4.35, 3, r'VS.', fontsize=16.5, fontweight='bold', bbox={'facecolor': 'grey', 'alpha': 0.5, 'pad': 5})
    #show screen for 5 seconds and
    ax.axis([0, 10, 0, 10])
    plt.show()
    play_sound('battle_sound.mp3', 5)
    plt.close()

def play_sound(file, time):
    ''' (Tom) uses the pygame module to play sound, utilizing the mixer function'''
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    sleep(time)
    pygame.mixer.music.stop()


def battle():
    ''' (Christina) Asks the user to select the player they want to battle. Both users pick
    the Pokemon they want to play as, or you could battle a random Pokemon
    The Power Level of each Pokemon in the battle is displayed.
    Updates the number of candies for both Pokemons according to who wins
    or loses the battle'''
    global player1_num_pokemon
    global player1candies
    num = int(input("\nEnter the number of the player you want to battle, Enter '0' to battle a random pokemon: "))
    if num == 1:
        opponent = select_pokemon()
    elif num == 2:
        opponent = select_pokemon2()
    elif num == 3:
        opponent = select_pokemon3()
    elif num == 0:
        opponent = rand_pokemon()
    selected_pokemon = select_pokemon()
    battle_screen(selected_pokemon[1], opponent[1])
    player_battle = random.randrange(returnCP(selected_pokemon))
    opponent_battle = random.randrange(returnCP(opponent))
    print(selected_pokemon[1], "\b's Power Level:", player_battle)
    print(opponent[1], "\b's Power Level:", opponent_battle)
    print("\nIt's not about the size of the dog in the fight, it's about the size of the fight in the dog...")
    player_var = random.randrange(750, 1000)
    opponent_var = random.randrange(750, 1000)
    candy = int(random.randrange(1, 4, 1))
    if player_battle + player_var > opponent_battle + opponent_var and candy > 1:
        print(opponent[1], 'fainted...\n', selected_pokemon[1], 'found', candy, 'candies in the opponents bag')
        player1candies += candy
        play_sound('victory_sound.mp3', 5)
    elif player_battle + player_var > opponent_battle + opponent_var:
        print(opponent[1], 'fainted...\n', selected_pokemon[1], 'found', candy, 'candy in the opponents bag')
        player1candies += candy
        play_sound('victory_sound.mp3', 5)
    if opponent_battle + opponent_var > player_battle + player_var and candy > 1:
        print(selected_pokemon[1], 'fainted...\n', opponent[1], 'found', candy, 'candies in your bag')
        if player1candies >= candy:
            player1candies -= candy
    elif opponent_battle + opponent_var > player_battle + player_var:
        print(selected_pokemon[1], 'fainted...\n', opponent[1], 'found', candy, 'candy in your bag')
        if player1candies >= candy:
            player1candies -= candy





def start_game():
    ''' (Christina) Determines whether to start or quit the game'''
    global player1_num_pokemon
    global change
    global current_p
    change=False
    play_sound('background.mp3', 6)
    x=str(0)
    while x != 'QUIT' and change==False:
        if change==False and current_p==1:
            x = menu_selection()
            sleep(1.25)
        elif change==True:
            break

#----------------------------------------------------------------------------------------------------------------------
#Player 2



def update_bag2(list):
    ''' (Hailie) This function opens a CSV file for player two and writes the parameter to the file'''
    with open('player2bag.csv', 'a') as bag:
        names_list_writer = csv.writer(bag, delimiter=',')
        names_list_writer.writerow(list)

def select_pokemon2():
    ''' (Hailie) This function gets the list of pokemon, calls the show_bag2() function, and allows the player to select a pokemon from their bag'''
    names_list_reader = csv.reader(open('player2bag.csv'))
    pokemon = list(names_list_reader)
    show_bag2()
    try_again = 0
    while try_again == 0:
        select = str(
            input("\nEnter the name of the pokemon you wish to select(exactly as it appears in the bag above): "))
        index = int(0)
        for i in pokemon:
            if len(i) > 2:
                if str(i[1]) == select:
                    index = pokemon.index(i)
                    return list(pokemon[index])

def use_candy2():
    ''' (Hailie) This function takes the pokemon selected in select_pokemon2() and determines the level of the pokemon.
    Next, it takes the number of candies the second player has to determine whether or not the pokemon can level up, and then
    however many candies it will take to level up. The pokemon is leveled up, and then it is written into the bag.'''
    global player2candies
    names_list_reader = csv.reader(open('player2bag.csv'))
    pokemon = list(names_list_reader)
    selected_pokemon = select_pokemon2()
    if len(selected_pokemon) == 5:
        level = int(selected_pokemon[4])
    else:
        level = int(selected_pokemon[3])
    if player2candies >= 1:
        if level < 30:
            level += 1
            print(selected_pokemon[1], "grew by 1 level, 1 candy was used...")
            if player2candies > 0:
                player2candies -= 1
        elif 30 <= level:
            if level < 40:
                level += 1
                print(selected_pokemon[1], "grew by 1 level, 2 candies were used...")
                if player2candies > 1:
                    player2candies -= 2
    else:
        print("No candies to use")
    if len(selected_pokemon) == 5:
        selected_pokemon[4] = str(int(selected_pokemon[4]) + 1)
    else:
        selected_pokemon[3] = str(int(selected_pokemon[3]) + 1)
    with open('player2bag.csv', 'r') as bag:
        names_list_reader = csv.reader(bag, delimiter=',')
        backpack = list(names_list_reader)
        x = 0
        for i in backpack:
            if len(i) == 5:
                if i[1] == selected_pokemon[1]:
                    if len(selected_pokemon) == 5:
                        i[4] = selected_pokemon[4]
                    else:
                        i[3] = selected_pokemon[3]
    with open('player2bag.csv', 'w') as bag:
        names_list_writer = csv.writer(bag, delimiter=',')
        for i in backpack:
            names_list_writer.writerow(i)


def show_bag2():
    ''' (Hailie) This function opens the second player’s bag and shows the pokemon'''
    global player2candies
    print("\n----------------------\033[0;34m [Player 2 Bag] \033[0m-----------------------".center(10))
    with open('player2bag.csv', 'r') as bag:
        names_list_reader = list(csv.reader(bag, delimiter=','))
        for i in names_list_reader:
            if len(i) == 5 and i[0]!='1':
                if i[1]!='name':
                    print('\n', i[1], '\b, Level:', i[4])
            else:
                bag.readline()
        '''
        for i in names_list_reader:
            if len(i) == 5:
                if i[1]!='name':
                    print('\n', i[1], '\b, Level:', i[4])
            else:
                print('\n', i[0], '\b, Level:', i[3])'''
    print("\n\033[0;34m Player 2 candies: \033[0m", player2candies, "\n----------------------")


def catch_pokemon2():
    ''' (Hailie) This function calls first rand_pokemon() to determine a pokemon the player could catch.
    Next, the function calls guessing_game() to see if the player wins the mini game. If the player wins,
    they win the pokemon and get a certain number of candies'''
    global player2candies
    global player2_num_pokemon
    enemy = rand_pokemon()
    level = enemy[4]
    print('\nA wild lvl.', level, enemy[1], 'appears...\n')
    if guessing_game(level) is True:
        play_sound('victory_sound.mp3', 3)
        sleep(0.75)
        print("lvl.", level, enemy[1], 'was caught!')
        candy = int(random.randrange(1, 4, 1))
        if candy == 1:
            player2candies += 3
        elif candy == 2:
            player2candies += 5
        else:
            player2candies += 10
        player2_num_pokemon += 1
        return enemy
    else:
        print('\n', enemy[1], 'escaped...')
        return ['1']


def battle_screen2(player1pokemon, player2pokemon): #parameters=str()
    ''' (Hailie) This function creates a plot that serves as the screen during a battle'''
    #create plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    #title plot "Pokemon 202 Maroon Edition
    fig.suptitle('Pokemon 2020 Maroon Edition', fontsize=20, fontweight='bold', color='maroon', alpha=1.0)
    #fill background red and hid axis'
    ax.text(4, 0, '_', color='black', alpha=0.0, fontsize=125, bbox={'facecolor': 'black', 'alpha': 0.95, 'pad': 190})
    ax.text(4, 0, '_', color='black', alpha=0.0, fontsize=125, bbox={'facecolor': 'maroon', 'alpha': 0.9, 'pad': 190})
    #plot("BATTLE!") bbox={'facecolor': 'red', 'alpha': 0.85, 'pad': 70}
    ax.text(0.25, 5, 'BATTLE!', style='italic', color='black', fontsize=85)
    #plot("player")
    ax.text(1.95, 1.9, r'(Player)', fontsize=10, fontweight='bold')
    #plot("opponent')
    ax.text(6.3, 1.9, r'(Opponent)', fontsize=10, fontweight='bold')
    #plot pokemon(player) vs. pokemon(opponent)
    ax.text(1, 3, player1pokemon, color='grey', alpha=1.0, fontsize=17, fontweight='bold', bbox={'facecolor': 'black', 'alpha': 0.85, 'pad': 10})
    ax.text(6.5, 3, player2pokemon, color='grey', alpha=1.0, fontsize=17, fontweight='bold', bbox={'facecolor': 'black', 'alpha': 0.85, 'pad': 10})
    ax.text(4.35, 3, r'VS.', fontsize=16.5, fontweight='bold', bbox={'facecolor': 'grey', 'alpha': 0.5, 'pad': 5})
    #show screen for 5 seconds and
    ax.axis([0, 10, 0, 10])
    plt.show()
    play_sound('battle_sound.mp3', 5)
    plt.close()


def battle2():
    ''' (Hailie) This function asks which player the user wants to battle.
    Calls select_pokemon2() function to get the selected pokemon.
    Determines which player wins the battle based on the CP and another number.
    Whoever wins the battle wins candy, whoever loses the battle loses candy.'''
    global player2_num_pokemon
    global player2candies
    num=int(input("\nEnter the number of the player you want to battle, Enter '0' to battle a random pokemon: "))
    if num==1:
        opponent = select_pokemon()
    elif num==2:
        opponent = select_pokemon2()
    elif num==3:
        opponent = select_pokemon3()
    elif num==0:
        opponent = rand_pokemon()
    selected_pokemon = select_pokemon2()
    battle_screen(selected_pokemon[1], opponent[1])
    player_battle = random.randrange(returnCP(selected_pokemon))
    opponent_battle = random.randrange(returnCP(opponent))
    print(selected_pokemon[1], "\b's Power Level:", player_battle)
    print(opponent[1], "\b's Power Level:", opponent_battle)
    print("\nIt's not about the size of the dog in the fight, it's about the size of the fight in the dog...")
    player_var = random.randrange(750, 1000)
    opponent_var = random.randrange(750, 1000)
    candy = int(random.randrange(1, 4, 1))
    if player_battle + player_var > opponent_battle + opponent_var and candy > 1:
        print(opponent[1], 'fainted...\n', selected_pokemon[1], 'found', candy, 'candies in the opponents bag')
        player2candies += candy
        play_sound('victory_sound.mp3', 5)
    elif player_battle + player_var > opponent_battle + opponent_var:
        print(opponent[1], 'fainted...\n', selected_pokemon[1], 'found', candy, 'candy in the opponents bag')
        player2candies += candy
        play_sound('victory_sound.mp3', 5)
    if opponent_battle + opponent_var > player_battle + player_var and candy > 1:
        print(selected_pokemon[1], 'fainted...\n', opponent[1], 'found', candy, 'candies in your bag')
        if player2candies >= candy:
            player2candies -= candy
    elif opponent_battle + opponent_var > player_battle + player_var:
        print(selected_pokemon[1], 'fainted...\n', opponent[1], 'found', candy, 'candy in your bag')
        if player2candies >= candy:
            player2candies -= candy

def menu_selection2():
    ''' (Hailie) This function gives the menu selection again and allows player to choose a selection'''
    global current_p
    global change
    det = 0
    inputs = ['QUIT', '1', '2', '3', '4', '5']
    while det == 0:
        main_menu()
        s=input("Enter your selection('QUIT'to quit): ")
        if s in inputs:
            det=1
    if s == 'QUIT':
        return s
    else:
        s=int(s)
    if s==1:
        caught_pokemon = catch_pokemon2()
        if caught_pokemon[0]!='1':
            update_bag2(caught_pokemon)
    elif s==2:
        show_bag2()
    elif s==3:
        battle2()
    elif s==4:
        use_candy2()
    elif s==5:
        current_p=int(input('Enter the player you wish to play as: '))
        change=True




def start_game2():
    ''' (Hailie) This function starts the game again.
    Plays the music in the background again.'''
    global player2_num_pokemon
    global change
    global current_p
    change=False
    play_sound('background.mp3', 6)
    x=str(0)
    while x != 'QUIT' and change==False:
        if change==False and current_p==2:
            x = menu_selection2()
            sleep(1.25)
        elif change==True:
            break


#-----------------------------------------------------------------------------------------------------------
# Player 3



def update_bag3(list):
    ''' (Nick) Function creates a CSV file of pokemon from the parameter list.'''
    with open('player3bag.csv', 'a') as bag:
        names_list_writer = csv.writer(bag, delimiter=',')
        names_list_writer.writerow(list)


def select_pokemon3():
    ''' (Nick) This function allows the user to input the name of a pokemon it wants to select, and finds the index of the pokemon
    name entered, and returns this pokemon from the list. Uses the show_bag3 function. Returns the name of the pokemon
    selected.'''
    names_list_reader = csv.reader(open('player3bag.csv'))
    pokemon = list(names_list_reader)
    show_bag3()
    try_again = 0
    while try_again == 0:
        select = str(
            input("\nEnter the name of the pokemon you wish to select(exactly as it appears in the bag above): "))
        index = int(0)
        for i in pokemon:
            if len(i) > 2:
                if str(i[1]) == select:
                    index = pokemon.index(i)
                    return list(pokemon[index])


def use_candy3():
    ''' (Nick) Determines the level of a pokemon selected in select_pokemon3. Uses candies to raise the level of
    pokemon selected. Determines the number of candies a player has to use, and adjusts the level
    accordingly. Subtracts number of candies used from the count. Writes the new level into the CSV file.
    Uses global variable player3candies. Calls function select_pokemon3.'''
    global player3candies
    names_list_reader = csv.reader(open('player3bag.csv'))
    pokemon = list(names_list_reader)
    selected_pokemon = select_pokemon3()
    if len(selected_pokemon) == 5:
        level = int(selected_pokemon[4])
    else:
        level = int(selected_pokemon[3])
    if player3candies >= 1:
        if level < 30:
            level += 1
            print(selected_pokemon[1], "grew by 1 level, 1 candy was used...")
            if player3candies > 0:
                player3candies -= 1
        elif 30 <= level:
            if level < 40:
                level += 1
                print(selected_pokemon[1], "grew by 1 level, 2 candies were used...")
                if player3candies > 1:
                    player3candies -= 2
    else:
        print("No candies to use")
    if len(selected_pokemon) == 5:
        selected_pokemon[4] = str(int(selected_pokemon[4]) + 1)
    else:
        selected_pokemon[3] = str(int(selected_pokemon[3]) + 1)
    with open('player3bag.csv', 'r') as bag:
        names_list_reader = csv.reader(bag, delimiter=',')
        backpack = list(names_list_reader)
        x = 0
        for i in backpack:
            if len(i) == 5:
                if i[1] == selected_pokemon[1]:
                    if len(selected_pokemon) == 5:
                        i[4] = selected_pokemon[4]
                    else:
                        i[3] = selected_pokemon[3]
    with open('player3bag.csv', 'w') as bag:
        names_list_writer = csv.writer(bag, delimiter=',')
        for i in backpack:
            names_list_writer.writerow(i)


def show_bag3():
    ''' (Nick) Prints the pokemon and respective level to the console. Prints the number of player candies also.
    Uses global variable player3candies.'''
    global player3candies
    print("\n----------------------\033[0;33m [Player 3 Bag] \033[0m-----------------------".center(10))
    with open('player3bag.csv', 'r') as bag:
        names_list_reader = list(csv.reader(bag, delimiter=','))
        for i in names_list_reader:
            if len(i) == 5:
                if i[1] != 'name':
                    print('\n', i[1], '\b, Level:', i[4])
            else:
                print('\n', i[0], '\b, Level:', i[3])
    print("\n\033[0;33m Player 3 candies: \033[0m", player3candies, "\n----------------------")


def catch_pokemon3():
    ''' (Nick) A random pokemon is selected using the function rand_pokemon. Has a user play a guessing game.
    If the user correctly guesses, the enemy pokemon is caught and an amount of candy is added to variable
    player3candies. Calls function rand_pokemon and guessing game.Uses global variables player3candies
    and player3_num_pokemon. Returns either enemy or 1.'''
    global player3candies
    global player3_num_pokemon
    enemy = rand_pokemon()
    level = enemy[4]
    print('\nA wild lvl.', level, enemy[1], 'appears...\n')
    if guessing_game(level) is True:
        play_sound('victory_sound.mp3', 3)
        sleep(0.75)
        print("lvl.", level, enemy[1], 'was caught!')
        candy = int(random.randrange(1, 4, 1))
        if candy == 1:
            player3candies += 3
        elif candy == 2:
            player3candies += 5
        else:
            player3candies += 10
        player3_num_pokemon += 1
        return enemy
    else:
        print('\n', enemy[1], 'escaped...')
        return ['1']


def battle_screen3(player1pokemon, player2pokemon):  # parameters=str()
    ''' (Nick) Creates a plot of the battle screen. Creates a title plot. Fills the background red. Plots battle
    Player, and opponent, and the player pokemon vs the opponent pokemon.'''
    # create plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    # title plot "Pokemon 202 Maroon Edition
    fig.suptitle('Pokemon 2020 Maroon Edition', fontsize=20, fontweight='bold', color='maroon', alpha=1.0)
    # fill background red and hid axis'
    ax.text(4, 0, '_', color='black', alpha=0.0, fontsize=125,
            bbox={'facecolor': 'black', 'alpha': 0.95, 'pad': 190})
    ax.text(4, 0, '_', color='black', alpha=0.0, fontsize=125,
            bbox={'facecolor': 'maroon', 'alpha': 0.9, 'pad': 190})
    # plot("BATTLE!") bbox={'facecolor': 'red', 'alpha': 0.85, 'pad': 70}
    ax.text(0.25, 5, 'BATTLE!', style='italic', color='black', fontsize=85)
    # plot("player")
    ax.text(1.95, 1.9, r'(Player)', fontsize=10, fontweight='bold')
    # plot("opponent')
    ax.text(6.3, 1.9, r'(Opponent)', fontsize=10, fontweight='bold')
    # plot pokemon(player) vs. pokemon(opponent)
    ax.text(1, 3, player1pokemon, color='grey', alpha=1.0, fontsize=17, fontweight='bold',
            bbox={'facecolor': 'black', 'alpha': 0.85, 'pad': 10})
    ax.text(6.5, 3, player2pokemon, color='grey', alpha=1.0, fontsize=17, fontweight='bold',
            bbox={'facecolor': 'black', 'alpha': 0.85, 'pad': 10})
    ax.text(4.35, 3, r'VS.', fontsize=16.5, fontweight='bold',
            bbox={'facecolor': 'grey', 'alpha': 0.5, 'pad': 5})
    # show screen for 5 seconds and
    ax.axis([0, 10, 0, 10])
    plt.show()
    play_sound('battle_sound.mp3', 5)
    plt.close()


def battle3():
    ''' (Nick) Asks the user to input the number of the player you want to battle. Uses functions select_pokemon,
    select_pokemon2, select_pokemon3,  and rand_pokemon to determine the user pokemon and enemy pokemon.
    Uses random numbers and pokemon level to determine which one wins. Uses global variables
    player3_num_pokemon and player3candies'''
    global player3_num_pokemon
    global player3candies
    num = int(
        input("\nEnter the number of the player you want to battle (They will select first), Enter '0' to battle a random pokemon: "))
    if num == 1:
        opponent = select_pokemon()
    elif num == 2:
        opponent = select_pokemon2()
    elif num == 3:
        opponent = select_pokemon3()
    elif num == 0:
        opponent = rand_pokemon()
    selected_pokemon = select_pokemon3()
    battle_screen(selected_pokemon[1], opponent[1])
    player_battle = random.randrange(returnCP(selected_pokemon))
    opponent_battle = random.randrange(returnCP(opponent))
    print(selected_pokemon[1], "\b's Power Level:", player_battle)
    print(opponent[1], "\b's Power Level:", opponent_battle)
    print("\nIt's not about the size of the dog in the fight, it's about the size of the fight in the dog...")
    player_var = random.randrange(750, 1000)
    opponent_var = random.randrange(750, 1000)
    candy = int(random.randrange(1, 4, 1))
    if player_battle + player_var > opponent_battle + opponent_var and candy > 1:
        print(opponent[1], 'fainted...\n', selected_pokemon[1], 'found', candy, 'candies in the opponents bag')
        player3candies += candy
        play_sound('victory_sound.mp3', 5)
    elif player_battle + player_var > opponent_battle + opponent_var:
        print(opponent[1], 'fainted...\n', selected_pokemon[1], 'found', candy, 'candy in the opponents bag')
        player3candies += candy
        play_sound('victory_sound.mp3', 5)
    if opponent_battle + opponent_var > player_battle + player_var and candy > 1:
        print(selected_pokemon[1], 'fainted...\n', opponent[1], 'found', candy, 'candies in your bag')
        if player3candies >= candy:
            player3candies -= candy
    elif opponent_battle + opponent_var > player_battle + player_var:
        print(selected_pokemon[1], 'fainted...\n', opponent[1], 'found', candy, 'candy in your bag')
        if player3candies >= candy:
            player3candies -= candy


def menu_selection3():
    ''' (Nick) The user inputs their selection for what they want to do. Input leads to other functions being run.
    Uses global variables current_p and change. Uses function main_menu, update_bag3, show_bag3,
    use_candy3, battle_3, and catch_pokemon3.'''
    global current_p
    global change
    det = 0
    inputs = ['QUIT', '1', '2', '3', '4', '5']
    while det == 0:
        main_menu()
        s = input("Enter your selection('QUIT'to quit): ")
        if s in inputs:
            det = 1
    if s == 'QUIT':
        return s
    else:
        s = int(s)
    if s == 1:
        caught_pokemon = catch_pokemon3()
        if caught_pokemon[0] != '1':
            update_bag3(caught_pokemon)
    elif s == 2:
        show_bag3()
    elif s == 3:
        battle3()
    elif s == 4:
        use_candy3()
    elif s == 5:
        current_p = int(input('Enter the player you wish to play as: '))
        change = True


def start_game3():
    ''' (Nick) Starts the game by opening the menu_selection3 while current_p is 3 for the third player.
    Uses global variables player3_num_pokemon, change, and current_p. Uses function menu_selection3.'''
    global player3_num_pokemon
    global change
    global current_p
    change = False
    play_sound('background.mp3', 6)
    x = str(0)
    while x != 'QUIT' and change == False:
        if change == False and current_p == 3:
            x = menu_selection3()
            sleep(1.25)
        elif change == True:
            break

#---------------------------------------------------------------------------------------------------------------------

def est_bags():
    ''' (Tom) establishes bag files for each player and writes in headers'''
    with open('player1bag.csv', 'w') as bag:
        headers = ['index', 'name', 'minCP', 'maxCP', 'current_level']
        names_list_writer = csv.writer(bag, delimiter=',')
        names_list_writer.writerow(headers)
    with open('player2bag.csv', 'w') as bag:
        headers = ['index', 'name', 'minCP', 'maxCP', 'current_level']
        names_list_writer = csv.writer(bag, delimiter=',')
        names_list_writer.writerow(headers)
    with open('player3bag.csv', 'w') as bag:
        headers = ['index', 'name', 'minCP', 'maxCP', 'current_level']
        names_list_writer = csv.writer(bag, delimiter=',')
        names_list_writer.writerow(headers)

#establishes variables for each players candy level, and number of caught Pokémon
global current_p
global change
global player1candies
global player2candies
global player3candies
global player1_num_pokemon
global player2_num_pokemon
global player3_num_pokemon

#establishes variable for switching players
change=False

#clears/reestablishes their bags with 1 Pokémon-using the rand_pokemon() function and resets each player too 0 candies.
est_bags()
update_bag(rand_pokemon())
update_bag2(rand_pokemon())
update_bag3(rand_pokemon())
player1candies=0
player2candies=0
player3candies=0
player1_num_pokemon=1
player2_num_pokemon=1
player3_num_pokemon=1
#asks user which player to begin as
print("\n\033[0;31m Enter '1' to play as player1 \033[0m", "\n\033[0;34m Enter '2' to play as player2 \033[0m", "\n\033[0;33m Enter '3' to play as player3 \033[0m")
current_p=int(input("\nselect (sound will play): "))

#establishes play variable so user can quit the game
play=0

#uses global variable for current player to allow swap between players
while play==0:
    if current_p==1:
        start_game()
    elif current_p==2:
        start_game2()
    elif current_p==3:
        start_game3()
    #allows user to quit or continue with their selection to change players using user input and the play variable
    sure=int(input("\nDo you want to quit? Enter 1 to quit, 0 to swap players: "))
    if sure==1:
        play=1

