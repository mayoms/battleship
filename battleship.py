from random import randrange

# Validation - Forces User to input an integer only.

def force_int(n):
    try:
        return int(n)
    except ValueError:
        return force_int(input("Sorry, not a number. Try again:"))

# Generates a random number, outside of excluded set. This should probably be a method in the Board class. To do.

def excluderand(excluded):
    coordinates = None
    while coordinates in excluded or coordinates is None:
        coordinates = randrange(0, my_board.board_size - 1)
    return coordinates

# Board class - Generates, prints and populates the game board.

class Board(object):
    def __init__(self):
        self.board_size = 0
        self.ship_count = 0
        self.board = []
        self.ships = []
        self.occupied = {"x": [], "y": []} #Dictionary may not be best datatype for this - will review.

    # User can set board size - which is always a square. Minimum size is 5, needs a maximum.

    def build_board(self):
        self.board_size = 0
        self.board = []
        self.board_size = force_int(input("How big would you like the board to be?"))
        if self.board_size < 5:
            print("The minimum size is 5x5")
            self.board_size = 5
        for column in range(self.board_size):
            self.board.append(["O"] * self.board_size)
    #The board is x arrays of x arrays. This prints those arrays in a square, minus all the extra array stuff.

    def print_board(self):
        for row in self.board:
            print(" ".join(row))

    #Populates the game board with user defined instances of the class Ship. There can be up to
    #board_size // 2 ships - to keep from running out of spots to place them.

    def populate(self):
        self.ships = []
        self.ship_count = force_int(input("How many ships would you like?"))
        while self.ship_count > self.board_size // 2:
            print("That's a few too many for your board size, try between 1 and %s" % (self.board_size // 2))
            self.ship_count = force_int(input("How many ships would you like?"))
            continue
        else:
            for each in range(self.ship_count):
                newship = Ship()
                newship.orient_ship()
                if newship.orientation == "vertical":
                    newship.vlocation()
                else:
                    newship.hlocation()
                self.ships.append(newship)

    #If the player gets a hit, that location is updated with a ! (conjures explosion imagery for me). A miss is an X.

    def update_board(self, x, y, result):
        if result == "hit":
            self.board[x][y] = "!"
        else:
            self.board[x][y] = "X"

# Battleships be here.

class Ship(object):
    def __init__(self):
        self.x = []
        self.y = []
        self.orientation = ""
        self.hits = 0

    # Randomly assign whether a ship is vertical or horizontal.

    def orient_ship(self):
        if randrange(0, 2) == 1:
            self.orientation = "vertical"
        else:
            self.orientation = "horizontal"

    # If a ship is horizontal, it gets 2 x and 2 1 coordinates (ships are 1x2 cells). The board occupied dictionary
    # is populated with (you guessed it), occupied coordinates, which is the input for the excluderand function.

    def hlocation(self):
        self.x.append(int(excluderand(my_board.occupied["x"])))
        my_board.occupied["x"].append(self.x[0])
        self.y.append(int(excluderand(my_board.occupied["y"])))
        my_board.occupied["y"].append(self.y[0])
        if self.x[0] == my_board.board_size:
            self.x.append(my_board.board_size - 1)
            my_board.occupied["x"].append(self.x[1])
        else:
            self.x.append(self.x[0] + 1)
            my_board.occupied["x"].append(self.x[1])

    # Vertical ships receive 2 y and 1 x coordinate in a similar manor.

    def vlocation(self):
        self.x.append(int(excluderand(my_board.occupied["x"])))
        my_board.occupied["x"].append(self.x[0])
        self.y.append(int(excluderand(my_board.occupied["y"])))
        my_board.occupied["y"].append(self.y[0])
        if self.y[0] == my_board.board_size:
            self.y.append(my_board.board_size - 1)
            my_board.occupied["y"].append(self.y[1])
        else:
            self.y.append(self.y[0] + 1)
            my_board.occupied["y"].append(self.y[1])

# Play class contains player name and stats for the current session and not much else at this time.

class Player(object):
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.tries = 0

    # Prints stats for the current session.

    def print_stats(self):
        print("Stats for %s" % self.name)
        print("Games Played: %s" % self.tries)
        print("Games Won: %s" % self.wins)
        print("Games Lost: %s" % self.losses)
        print("Win Percentage: %s" % (self.wins / self.tries))

# Stats from players to be saved and printed at the end of each game.

class Stats_Board(object):
    def __init__(self):
        self.player_dict = {}

    # Dump player stats into a text file, comma delimited.

    def write_stats(self):
        with open("stats.txt", 'w') as statsfile:
            for key in self.player_dict:
                statsfile.write(self.stats_dict_convert(key))

    # Converts the contents of each dictionary entry into a writable string. Need to write a method for sorting
    # player stats by highest win percentage and then printing a leaderboard.

    def stats_dict_convert(self, key):
        return (str(key) + ',' + self.player_dict[key][0] + ',' + self.player_dict[key][1]
                + ',' + self.player_dict[key][2] + ',' + self.player_dict[key][3] + '\n')

    # Populates a dictionary with the contents of stats save file.

    def create_stats_dict(self):
        stats = []
        with open("stats.txt", "r") as statsfile:
            for line in statsfile.readlines():
                line = line.rstrip('\n')
                stats = line.split(',')
                self.player_dict[stats[0]] = stats[1:]

    # Checks to see if the current player already has an entry, if so, updates that entry.
    # If not, creates a new one.

    def update_stats_dict(self):
        for key in self.player_dict:
            if current_player.name == key:
                self.player_dict[key][0] = str(int(self.player_dict[key][0]) + current_player.tries)
                self.player_dict[key][1] = str(int(self.player_dict[key][1]) + current_player.losses)
                self.player_dict[key][2] = str(int(self.player_dict[key][2]) + current_player.wins)
                self.player_dict[key][3] = str(float(self.player_dict[key][2]) / float(self.player_dict[key][0]))
                return
        else:
            self.player_dict[current_player.name] = [str(current_player.tries), str(current_player.losses),
                                                     str(current_player.wins),
                                                     str(current_player.tries / current_player.wins)]


# Game class - handles all of the gaming interaction.

class Game(object):
    def __init__(self):
        self.turns = 0
        self.sank = 0
        self.hits = 0
        self.misses = 0

    # Main game engine - builds and populates the game board, queries for input and keeps score.
    # This should probably be split into even smaller pieces.

    def play(self):
        self.sank = 0
        self.hits = 0
        print("Shall we play a game?")
        my_board.build_board()
        my_board.populate()
        self.turns = 3 * my_board.ship_count
        current_player.tries += 1
        while self.sank < my_board.ship_count:
            if self.turns > 0:
                print("%s turns left" % self.turns)
                my_board.print_board()
                guess_x = force_int(input("Guess Row: "))
                guess_y = force_int(input("Guess Column: "))
                if guess_x > my_board.board_size or guess_y > my_board.board_size: # Some bug here - this doesn't always
                    print("That's not even on the map!")                           # Work. To do: fix.
                    self.turns -= 1
                elif my_board.board[guess_x][guess_y] is "X" or my_board.board[guess_x][guess_y] is "!":
                    print("You already guessed there!")
                    self.turns -= 1
                elif self.assault(guess_x, guess_y) is True:
                    print("You got a hit!")
                    my_board.update_board(guess_x, guess_y, "hit")
                    self.hits += 1
                else:
                    print("Miss!")
                    my_board.update_board(guess_x, guess_y, "miss")
                    self.misses += 1
                    self.turns -= 1
            else:
                print("Sorry, out of turns.")
                current_player.losses += 1
                self.play_again(input("Would you like to play again?"))
                break
        else:
            print("You won!")
            current_player.wins += 1
            self.play_again(input("Would you like to play again?"))

    # This is called on by the Game method, and evaluates the user input against ship locations, returns
    # whether or not contact was made.

    def assault(self, x, y):
        for each in range(my_board.ship_count):
            if x in my_board.ships[each].x and y in my_board.ships[each].y:
                my_board.ships[each].hits += 1
                self.hits += 1
                if my_board.ships[each].hits == 2:
                    print("You sank a ship!")
                    self.sank += 1
                return True
        return False

    # Queries the user to play again, if not starts a new instance of game.play(). Otherwise updates and prints stats.

    def play_again(self, answer):
        if answer.lower() == "y":
            my_game.play()
        elif answer.lower() == "n":
            current_player.print_stats()
            game_stats.update_stats_dict()
            print(game_stats.player_dict)
            game_stats.write_stats()
        else:
            print("Sorry, please enter 'y' for yes or 'n' for no")
            self.play_again(input("Play again?"))


my_board = Board()
my_game = Game()
game_stats = Stats_Board()
current_player = Player(input("What's your name, player?"))
game_stats.create_stats_dict()
my_game.play()







