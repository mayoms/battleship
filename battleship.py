from random import randrange

def force_int(n):
    try:
        return int(n)
    except ValueError:
        return force_int(input("Sorry, not a number. Try again:"))

def excluderand(excluded):
    coordinates = None
    while coordinates in excluded or coordinates is None:
        coordinates = randrange(0, my_board.board_size - 1)
    return coordinates


class Board(object):
    def __init__(self):
        self.board_size = 0
        self.ship_count = 0
        self.board = []
        self.ships = []
        self.occupied = {"x":[], "y":[]}

    def build_board(self):
        self.board = []
        self.board_size = force_int(input("How big would you like the board to be?"))
        if self.board_size < 5:
            print("The minimum size is 5x5")
            self.board_size = 5
        for column in range(self.board_size):
            self.board.append(["O"] * self.board_size)

    def print_board(self):
        for row in self.board:
            print(" ".join(row))

    def populate(self):
        self.ships = []
        self.ship_count = force_int(input("How many ships would you like?"))
        while self.ship_count > self.board_size // 2:
            print("That's a few too many for your board size, try between 1 and %s" % (self.board_size // 2))
            self.ship_count = force_int(input("How many ships would you like?"))
        else:
            for each in range(self.ship_count):
                newship = Ship()
                newship.orient_ship()
                if newship.orientation == "vertical":
                    newship.vlocation()
                else:
                    newship.hlocation()
                self.ships.append(newship)
                print (self.ships[each].x, self.ships[each].y)

    def update_board(self, x, y, result):
        if result == "hit":
            self.board[x][y] = "!"
        else:
            self.board[x][y] = "X"

class Ship(object):
    def __init__(self):
        self.x = []
        self.y = []
        self.orientation = ""
        self.hits = 0

    def orient_ship(self):
        if randrange(0,2) == 1:
            self.orientation = "vertical"
        else:
            self.orientation = "horizontal"

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

    def vlocation(self):
        self.x.append(int(excluderand(my_board.occupied["x"])))
        my_board.occupied["x"].append(self.x[0])
        self.y.append(int(excluderand(my_board.occupied["y"])))
        my_board.occupied["y"].append(self.y[0])
        if self.y[0] == my_board.board_size:
            self.y.append(my_board.board_size -1)
            my_board.occupied["y"].append(self.y[1])
        else:
            self.y.append(self.y[0] + 1)
            my_board.occupied["y"].append(self.y[1])

class Player(object):
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.tries = 0

    def calculate_stats(self):
        pass

    def print_stats(self):
        print("Stats for %s" % self.name)
        print("Games Played: %s" % self.tries)
        print("Games Won: %s" % self.wins)
        print("Games Lost: %s" % self.losses)
        print("Win Percentage: %s" % (self.wins / self.tries))
    def update_stat_board(self):
        pass

    def print_leaderboard(self):
        pass

class Game(object):
    def __init__(self):
        self.turns = 0
        self.sank = 0
        self.hits = 0
        self.misses = 0

    def play(self):
        self.sank = 0
        self.hits = 0
        print ("Shall we play a game?")
        my_board.build_board()
        my_board.populate()
        self.turns = 3 * my_board.ship_count
        current_player.tries += 1
        while self.sank < my_board.ship_count:
            if self.turns > 0:
                print ("%s turns left" % self.turns)
                my_board.print_board()
                guess_x = force_int(input("Guess Row: "))
                guess_y = force_int(input("Guess Column: "))
                if guess_x > my_board.board_size or guess_y > my_board.board_size:
                    print ("That's not even on the map!")
                    self.turns -=1
                elif my_board.board[guess_x][guess_y] == "X" or my_board.board[guess_x][guess_y] == "!":
                    print ("You already guessed there!")
                    self.turns -=1
                elif self.assault(guess_x,guess_y) is True:
                    print ("You got a hit!")
                    my_board.update_board(guess_x,guess_y,"hit")
                    self.hits +=1
                else:
                    print ("Miss!")
                    my_board.update_board(guess_x,guess_y,"miss")
                    self.misses +=1
                    self.turns -=1
            else:
                print ("Sorry, out of turns.")
                current_player.losses += 1
                self.play_again(input("Would you like to play again?"))
                break
        else:
            print ("You won!")
            current_player.wins += 1
            self.play_again(input("Would you like to play again?"))

    def assault(self,x,y):
        for each in range(my_board.ship_count):
            print (each)
            print (my_board.ships[each].x, my_board.ships[each].y)
            if x in my_board.ships[each].x and y in my_board.ships[each].y:
                my_board.ships[each].hits +=1
                self.hits +=1
                if my_board.ships[each].hits == 2:
                    print("You sank a ship!")
                    self.sank +=1
                return True
        return False

    def play_again(self,answer):
        if answer.lower() == "y":
            my_game.play()
        elif answer.lower() == "n":
            current_player.print_stats()
        else:
            print("Sorry, please enter 'y' for yes or 'n' for no")
            self.play_again(input("Play again?"))




my_board = Board()
my_game = Game()
current_player = Player(input("What's your name, player?"))
my_game.play()







