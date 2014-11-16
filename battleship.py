from random import randint
from random import randrange

ships = 0
board = []
BuiltShips = {}
board_size = int(input("How big would you like the board to be?"))
for x in range(board_size):
    board.append(["O"] * board_size)
def print_board(board):
    for row in board:
        print(" ".join(row))


class BattleShip(object):
    def __init__(self, id):
        self.id = id
        self.location = {
            "x": [],
            "y": []
        }
        self.hits = 0
        self.orientation = ""
    x = [] # Keep Track of all X Coordinates
    y = [] # Keep Track of all Y Coordinates
    sank = 0
           # All battleships start with these attributes, hit count, whether or not it is sank, location and orientation
    def ExcludeRand(self,exclude): #this will generate a random number, while excluding coordinates already assigned
        points = None
        while points in exclude or points is None:
            points = randrange(0, len(board)-1)
        return points

    # Battleship, Build Thyself!
    def build(self):
        if randint(0, 1) == 1:  # Flip a coin to determine orientation
            self.orientation = "vertical"
        else:
            self.orientation = "horizontal"

      # If there aren't any ships built yet, we can put it anywhere
        if self.orientation == "horizontal":  #If the coin flipped to horizontal, build it that way
            self.location["x"].append(int(self.ExcludeRand(self.x)))  #Assign Random X Coordinate
            self.x.append(self.location["x"][0])
            print ("X's:", self.x)
            print (self.location)
            self.location["y"].append(int(self.ExcludeRand(self.y)))  #Assign Random Y Coordinate
            self.y.append(self.location["y"][0])
            print (self.location)
            if self.location["x"] == len(board) - 1:
                self.location["x"][0].append(len(board) - 2)
                print (self.location)
            else:
                self.location["x"].append(self.location["x"][0] + 1)
                print (self.location)
            print (self.location)
        else:
            self.location["x"].append(int(self.ExcludeRand(self.x)))  #Random X
            self.x.append(self.location["x"][0])
            print (self.location)
            self.location["y"].append(int(self.ExcludeRand(self.y)))  #Random Y
            self.y.append(self.location["y"][0])
            print ("Y's:",self.y)
            print (self.location)
            if self.location["y"][0] == len(board) - 1:  #Y plus or minus 1
                self.location["y"].append(len(board) - 2)
                print (self.location)
            else:
                self.location["y"].append(self.location["y"][0] + 1)
                print (self.location)

def is_int(n):
    try:
        return int(n)
    except ValueError:
        is_int(input("Sorry, not a number. Try again:"))

ships = is_int(input("How many ships?"))

for each in range(ships):
    BuiltShips["ship" + str(each)] = BattleShip(each)
    BuiltShips["ship" + str(each)].build()
def Assault(x,y):
    for each in BuiltShips:
        if x in BuiltShips[each].location["x"] and y in BuiltShips[each].location["y"]:
            BuiltShips[each].hits += 1
            if BuiltShips[each].hits == 2:
                print ("You sank a ship!")
                BattleShip.sank += 1
            return True
        else:
            print (BuiltShips[each].location)
    return False

turns = 3 * ships
while BattleShip.sank < ships:
    if turns > 0:
        print ("%s turns left" % turns)
        print_board(board)
        guess_x = int(input("Guess Row:"))
        guess_y = int(input("Guess Column:"))
        if board[guess_x][guess_y] == "X" or board[guess_x][guess_y] == "!":
            print ("You already guessed there!")
            turns -= 1
        elif Assault(guess_x,guess_y) == True:
            print ("You got a hit!")
            board[guess_x][guess_y] = "!"
            print_board(board)
            print ("Ships sank:",BattleShip.sank)
        else:
            print ("Miss!")
            board[guess_x][guess_y] = "X"
            turns -= 1
    else:
        print ("Sorry, out of turns.")
        break
else:
    print ("You won.")
