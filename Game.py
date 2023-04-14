
#Python FinalProject - Checkers Game
"""Name : Vedant Chidgopkar
   Student ID: 00748701 
Description of the py file : Program for demonstration of checkers game using python programming. This is 2 player game. The user is asked to enter the name.
If the user input is an empty program will keep asking until the users give input. After that program will take the user's permission to start the game. One text file will get created
as soon as the user options to start the game. The name of the file will is "player1name_player2name_date_time.txt". In this file, all record will be kept as
the user plays a move or make a jump. The textual board will display on the screen, it will contain B for blank pieces, 'x' piece for player 1, and 'o' for player 2.
Players will ask to enter the position of a piece that they want to move and the position where they wanted to move alternatively. If the move is legal piece will move
and the updated board will be displayed. If the move is illegal the error message will display and the player will ask to re-enter the position. The player can quit the game by entering
'q' or 'Q' anytime in the middle of a game. The other player will be declared the winner. If the piece gets to the end of the row it will be a king piece and can move forward and
backward. The game will end if one of the players has no move to play or zero pieces left on the board.
"""
#Importing all the required modules
from copy import deepcopy
import datetime
import os

#class tomake a piece aking piece
class King:

    #initiated class variables    
    def __init__(self, board, move=None, parent=None, value=None):
        self.board = board
        self.value = value
        self.move = move
        self.parent = parent
    #method to get the stauts of children pieces
    def get_children(self, minimizing_player, mandatory_jumping):
        #storing the copy of board in variable
        current_state = deepcopy(self.board)
        #initiating the list and string forfurther use
        available_moves = []
        children_states = []
        big_letter = ""
        queen_row = 0
        #checking the stauts of player one and 2 to make the king pieces
        if minimizing_player is True:
            #checking if player 1 is at last roe to make it king piece
            available_moves = Game.find_player1_available_moves(current_state, mandatory_jumping)
            big_letter = "X"
            queen_row = 7
        else:
            #checking if player 2 is at last roe to make it king piece
            available_moves = Game.find_player2_available_moves(current_state, mandatory_jumping)
            big_letter = "O"
            queen_row = 0
            #giving new moves to king pieces
        for i in range(len(available_moves)):
            old_i = available_moves[i][0]
            old_j = available_moves[i][1]
            new_i = available_moves[i][2]
            new_j = available_moves[i][3]
            #checking the current statE of king piece in board
            state = deepcopy(current_state)
            Game.make_a_move(state, old_i, old_j, new_i, new_j, big_letter, queen_row)
            #appending the king pieces
            children_states.append(King(state, [old_i, old_j, new_i, new_j]))
        return children_states
    #method to set value of piece
    def set_value(self, value):
        self.value = value
    #method to get value of piece
    def get_value(self):
        return self.value
    #method to getboard
    def get_board(self):
        return self.board
    #method to get king piece status
    def get_parent(self):
        return self.parent
    #method toset king piece status
    def set_parent(self, parent):
        self.parent = parent



#Initiated Game class which has aal the methods for the borad and player input
class Game:
    #initiated self variables
    def __init__(self):
        self.matrix = [[], [], [], [], [], [], [], []]
        self.arr=['A','B','C','D','E','F','G','H']
        self.num=['1','2','3','4','5','6','7','8']
        self.Player1Name = ''
        self.Player2Name = ''
        self.fileName=""
        self.oldValue=0
        self.newValue=0
        self.player1_turn = True
        self.player2_turn = True
        self.player1_pieces = 12
        self.player2_pieces = 12
        self.available_moves = []
        self.mandatory_jumping = False

        #Printing piecese on the board in required format
        for row in self.matrix:
            for i in range(8):
                if i%2 == 1:
                    row.append("B")
                else:
                    row.append("R")
        self.matrix[3]=['B','R','B','R','B','R','B','R']
        #Initiating position for player
        self.position_player1()
        self.position_player2()

    #Method for position for player 1 for x piece
    def position_player1(self):
        #for first three rows in board
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matrix[i][j] = ("x")
                else:
                    self.matrix[i][j] = ("R")
    
    #Method for position for player 2 for o piece
    def position_player2(self):
        #for lowwer 3 rows of board
        for i in range(5, 8, 1):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matrix[i][j] = ("o")
                else:
                    self.matrix[i][j] = ("R")

    #Method to print 
    def print_board(self):
        print()
        #prints row values from 1 to 7
        for j in range(8):
            if j == 0:
                self.num[j] = "    1"
            print(self.num[j], end=" ")
        print("\n")
        i = 0
        #prints column values for A to H
        for row in self.matrix:
            print(self.arr[i], end="  |")
            i += 1
            for elem in row:
                print(elem, end=" ")
            print()
        print()
    #Method for take input from player 1 for position of piece
    def player1_input(self):
        #cheks if player 1 has any available move
        available_moves = Game.find_player1_available_moves(self.matrix, self.mandatory_jumping)
        if len(available_moves) == 0:
            #if no move is availble prints you lose
            if self.player2_pieces > self.player1_pieces:
                #writes result to file
                print("You have no moves left, and you have fewer pieces than the Player1.YOU LOSE!")
                with open(self.fileName,"a") as fileObject:
                    content=f"\n{self.Player1Name}have no moves left, and you have fewer pieces than {self.Player2Name} \n {self.Player2Name} WINS !!!"
                    fileObject.write(content)
                exit()
            else:
                #prints message no available moves GAME ENDED
                print("You have no available moves.\nGAME ENDED!")
                with open(self.fileName,"a") as fileObject:
                    content=f"\n{self.Player1Name}have no moves left, and you have fewer pieces than {self.Player2Name} \n {self.Player2Name} WINS !!!"
                    fileObject.write(content)
                exit()
        #Sets piecce value to 0
        self.player1_pieces = 0
        self.player2_pieces = 0
        while True:
            #Takes input from user to move piece
            coord1 = input("Please Enter Piece you want to Move in [A,1] Format: ")
            if coord1 == "":
                print("Wrong input!! Please enter again")
            elif coord1 == "q" or coord1=="Q":
                #printing result and writing in log file
                print(f"\n{self.Player1Name} left the game \n {self.Player2Name} WINS !!!\n GAME END")
                with open(self.fileName,"a") as fileObject:
                    content=f"\n{self.Player1Name} left the game \n {self.Player2Name} WINS !!!\n GAME END"
                    fileObject.write(content)
                exit()
            coord2 = input("Please Enter position to Move in [A,1] Format:")
            if coord2 == "":
                #printing result and writing in log file
                print("Wrong input!! Please enter again")
            elif coord2 == "q" or coord2=="Q":
                print(f"\n{self.Player1Name} left the game \n {self.Player2Name} WINS !!!\n GAME END")
                with open(self.fileName,"a") as fileObject:
                    content=f"\n{self.Player1Name} left the game \n {self.Player2Name} WINS !!!\n GAME END"
                    fileObject.write(content)
                exit()
            #spliting the user input from user
            old = coord1.split(",")
            new = coord2.split(",")
            #cheking the length of input
            if len(old) != 2 or len(new) != 2:
                print("Illegal input")
            else:
                #storing user input to variable for further use
                for index, value in enumerate(self.arr):
                    if old[0]==value:
                        self.oldValue=index
                    if new[0]==value:
                        self.newValue=index
                old_i = str(self.oldValue)
                oldValue=int(old[1])
                oldValue=oldValue-1
                oldValue=str(oldValue)
                old_j = oldValue
                new_i = str(self.newValue)
                newValue=int(new[1])
                newValue=newValue-1
                newValue=str(newValue)
                new_j = newValue
                if not old_i.isdigit() or not old_j.isdigit() or not new_i.isdigit() or not new_j.isdigit():
                    print("Illegal input")
                else:
                     #storing user input in the list to make a move
                    move = [int(old_i), int(old_j), int(new_i), int(new_j)]
                    #checking if player has avilbale move if not printing error message
                    if move not in available_moves:
                        print("Illegal move!")
                    else:
                        #printing in log file the user move
                        with open(self.fileName,"a") as fileObject:
                            content=f"\n{self.Player1Name} moved peice from {old[0]},{old[1]} to {new[0]},{new[1]}"
                            finalWrite=content+f"  :  {datetime.datetime.now()}\n"
                            fileObject.write(finalWrite)
                            fileObject.close()
                         #calling move method to make the move      
                        Game.make_a_move(self.matrix, int(old_i), int(old_j), int(new_i), int(new_j), "O", 0)
                        for m in range(8):
                            for n in range(8):
                                #printing the move on the board with the hep of matrix
                                if self.matrix[m][n][0] == "x" or self.matrix[m][n][0] == "X":
                                    self.player2_pieces += 1
                                elif self.matrix[m][n][0] == "o" or self.matrix[m][n][0] == "O":
                                    self.player1_pieces += 1
                        break


    #Method for take input from player 2 for position of piece
    def player2_input(self):
        #cheks if player 2 has any available move
        available_moves = Game.find_player2_available_moves(self.matrix, self.mandatory_jumping)
        if len(available_moves) == 0:
            #if no move is availble prints you lose
            if self.player1_pieces > self.player2_pieces:
                print(f"{self.Player2Name}have no moves left, and you have fewer pieces than the {self.Player1Name}\n{self.Player2Name}LOSE!")
                #writes result to file
                with open(self.fileName,"a") as fileObject:
                    content=f"\n{self.Player2Name}have no moves left, and you have fewer pieces than {self.Player1Name} \n {self.Player1Name} WINS !!!\n GAME END"
                    fileObject.write(content)
                exit()
            else:
                #prints message no available moves GAME ENDED
                print("You have no available moves.\nGAME ENDED!")
                #writes the resultto file
                with open(self.fileName,"a") as fileObject:
                    content=f"\n{self.Player2Name}have no moves left, and you have fewer pieces than {self.Player1Name} \n {self.Player1Name} WINS !!!\n GAME END"
                    fileObject.write(content)
                exit()
        #Sets piecce value to 0
        self.player1_pieces = 0
        self.player2_pieces = 0
        while True:
            #Takes input from user to move piece
            coord1 = input("Please Enter Piece you want to Move in [A,1] Format: ")
            if coord1 == "":
                print("Wrong input!! Please enter again")
            elif coord1 == "q" or coord1=="Q":
                #printing result and writing in log file
                print(f"\n{self.Player2Name} left the game \n {self.Player1Name} WINS !!!\n GAME END")
                with open(self.fileName,"a") as fileObject:
                    content=f"\n{self.Player2Name} left the game \n {self.Player1Name} WINS !!!\n GAME END"
                    fileObject.write(content)
                exit()
            coord2 = input("Please Enter position to Move in [A,1] Format:")
            if coord2 == "":
                #printing result and writing in log file
                print("Wrong input!! Please enter again")
            elif coord2 == "q" or coord2=="Q":
                print(f"\n{self.Player2Name} left the game \n {self.Player1Name} WINS !!!\n GAME END")
                with open(self.fileName,"a") as fileObject:
                    content=f"\n{self.Player2Name} left the game \n {self.Player1Name} WINS !!!\n GAME END"
                    fileObject.write(content)
                exit()
            #spliting the user input from user
            old = coord1.split(",")
            new = coord2.split(",")
            #cheking the length of input
            if len(old) != 2 or len(new) != 2:
                print("Illegal input")
            else:
                #storing user input in variable for further use
                for index, value in enumerate(self.arr):
                    if old[0]==value:
                        self.oldValue=index
                    if new[0]==value:
                        self.newValue=index
                old_i = str(self.oldValue)
                oldValue=int(old[1])
                oldValue=oldValue-1
                oldValue=str(oldValue)
                old_j = oldValue
                new_i = str(self.newValue)
                newValue=int(new[1])
                newValue=newValue-1
                newValue=str(newValue)
                new_j = newValue

                #checking ifthe user has enterd number if not displaying error
                if not old_i.isdigit() or not old_j.isdigit() or not new_i.isdigit() or not new_j.isdigit():
                    print("Illegal input")
                else:
                    #storinguser input in the list to make a move
                    move = [int(old_i), int(old_j), int(new_i), int(new_j)]
                    #checking if player has avilbale move if not printing error message
                    if move not in available_moves:
                        print("Illegal move!")
                    else:
                        #printing in log file the user move 
                        with open(self.fileName,"a") as fileObject:
                            content=f"\n{self.Player2Name} moved peice from {old[0]},{old[1]} to {new[0]},{new[1]}"
                            finalWrite=content+f"  :  {datetime.datetime.now()}\n"
                            fileObject.write(finalWrite)
                            fileObject.close()
                        #calling move method to make the move                        
                        Game.make_a_move(self.matrix, int(old_i), int(old_j), int(new_i), int(new_j), "O", 0)
                        for m in range(8):
                            for n in range(8):
                                #printing the move on the board with the hep of matrix
                                if self.matrix[m][n][0] == "x" or self.matrix[m][n][0] == "X":
                                    self.player2_pieces += 1
                                elif self.matrix[m][n][0] == "o" or self.matrix[m][n][0] == "O":
                                    self.player1_pieces += 1
                        break

    #Defining method to find player 1 available move and jump
    def find_player1_available_moves(board, mandatory_jumping):
        #initiating the lists
        available_moves = []
        available_jumps = []
        
        #checking the position of pices on the board 
        for m in range(8):
            for n in range(8):
                #checking move or jump for normal pieces
                if board[m][n][0] == "x":
                    #cheking move for player 1 at right  diagonal
                    if Game.check_player1_moves(board, m, n, m + 1, n + 1):
                        #checking for available moves
                        available_moves.append([m, n, m + 1, n + 1])
                    #cheking move for player 1 at left  diagonal
                    if Game.check_player1_moves(board, m, n, m + 1, n - 1):
                        #checking for available moves
                        available_moves.append([m, n, m + 1, n - 1])
                    #cheking jump for player 1 at right  diagonal
                    if Game.check_player1_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
                        #checking for available jump
                        available_jumps.append([m, n, m + 2, n - 2])
                    #cheking jump for player 1 at left  diagonal
                    if Game.check_player1_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                        #checking for available jump
                        available_jumps.append([m, n, m + 2, n + 2])
                #checking move or jump for king pieces
                elif board[m][n][0] == "X":
                    #cheking move for player 1 at right  diagonal
                    if Game.check_player1_moves(board, m, n, m + 1, n + 1):
                        #checking for available moves
                        available_moves.append([m, n, m + 1, n + 1])
                    #cheking move for player 1 at left  diagonal
                    if Game.check_player1_moves(board, m, n, m + 1, n - 1):
                        #checking for available move
                        available_moves.append([m, n, m + 1, n - 1])
                    #cheking move for player 1 at back right  diagonal
                    if Game.check_player1_moves(board, m, n, m - 1, n - 1):
                        #checking for available move
                        available_moves.append([m, n, m - 1, n - 1])
                    #cheking move for player 1 at back right  diagonal
                    if Game.check_player1_moves(board, m, n, m - 1, n + 1):
                        #checking for available move
                        available_moves.append([m, n, m - 1, n + 1])
                    #cheking jump for player 1 at left  diagonal
                    if Game.check_player1_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
                        #checking for available jump
                        available_jumps.append([m, n, m + 2, n - 2])
                    #cheking jump for player 1 at right  diagonal
                    if Game.check_player1_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
                         #checking for available jump
                        available_jumps.append([m, n, m - 2, n - 2])
                    #cheking jump for player 1 at back right  diagonal
                    if Game.check_player1_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
                         #checking for available jump
                        available_jumps.append([m, n, m - 2, n + 2])
                    #cheking jump for player 1 at back left  diagonal
                    if Game.check_player1_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                         #checking for available jump
                        available_jumps.append([m, n, m + 2, n + 2])
        #if jump mandatory is false extending the available moves for player 1
        if mandatory_jumping is False:
            available_jumps.extend(available_moves)
            return available_jumps
        #making player 1 jump compulsory
        elif mandatory_jumping is True:
            if len(available_jumps) == 0:
                return available_moves
            else:
                return available_jumps

    #Method to check palyer 1 jumps
    def check_player1_jumps(board, old_i, old_j, via_i, via_j, new_i, new_j):
        #if input is invalid returning false
        if new_i > 7 or new_i < 0:
            return False
         #if input is invalid returning false
        if new_j > 7 or new_j < 0:
            return False
        #cheking if the position is available to make a jump    
        if board[via_i][via_j] == "B":
            return False
        #checking if the pieces is at the position to makejump  
        if board[via_i][via_j][0] == "X" or board[via_i][via_j][0] == "x":
            return False
        if board[new_i][new_j] != "B":
            return False
        if board[old_i][old_j] == "B":
            return False
        if board[old_i][old_j][0] == "o" or board[old_i][old_j][0] == "O":
            return False
        return True

   # Method to check the moves of player 1
    def check_player1_moves(board, old_i, old_j, new_i, new_j):
        #if input is invalid returning false
        if new_i > 7 or new_i < 0:
            return False
        #if input is invalid returning false
        if new_j > 7 or new_j < 0:
            return False
         #cheking if the position is available to make a move
        if board[old_i][old_j] == "B":
            return False
        #cheking if the position is available to make ajump
        if board[new_i][new_j] != "B":
            return False
        #cheking if the position is available to make ajump
        if board[old_i][old_j][0] == "o" or board[old_i][old_j][0] == "O":
            return False
        if board[new_i][new_j] == "B":
            return True


    #Defining method to find player 2 available moves and hump
    def find_player2_available_moves(board, mandatory_jumping):
         #initiating the lists
        available_moves = []
        available_jumps = []
        #checking the position of pices on the board 
        for m in range(8):
            for n in range(8):
                #Checking jump and move is vailble for player 2 or not for normal pices
                if board[m][n][0] == "o":
                    #chekimg available moves 
                    if Game.check_player2_moves(board, m, n, m - 1, n - 1):
                        available_moves.append([m, n, m - 1, n - 1])
                    if Game.check_player2_moves(board, m, n, m - 1, n + 1):
                        available_moves.append([m, n, m - 1, n + 1])
                    #checking available jumps
                    if Game.check_player2_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if Game.check_player2_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                #Checking jump and move is vailble for player 2 or not for king pices
                elif board[m][n][0] == "O":
                    #chekimg available moves 
                    if Game.check_player2_moves(board, m, n, m - 1, n - 1):
                        available_moves.append([m, n, m - 1, n - 1])
                        #chekimg available moves
                    if Game.check_player2_moves(board, m, n, m - 1, n + 1):
                        available_moves.append([m, n, m - 1, n + 1])
                        #checking available jumps
                    if Game.check_player2_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                        #chekimg available jumps
                    if Game.check_player2_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                        #chekimg available moves
                    if Game.check_player2_moves(board, m, n, m + 1, n - 1):
                        available_moves.append([m, n, m + 1, n - 1])
                        #checking available jumps
                    if Game.check_player2_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                        #chekimg available moves
                    if Game.check_player2_moves(board, m, n, m + 1, n + 1):
                        available_moves.append([m, n, m + 1, n + 1])
                        #checking available jumps
                    if Game.check_player2_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
        #if jump mandatory is false extending the available moves for player 1
        if mandatory_jumping is False:
            available_jumps.extend(available_moves)
            return available_jumps
        #making player 1 jump compulsory
        elif mandatory_jumping is True:
            if len(available_jumps) == 0:
                return available_moves
            else:
                return available_jumps

    # Method to check the moves ofplayer 2
    def check_player2_moves(board, old_i, old_j, new_i, new_j):
        #if input is invalid returning false
        if new_i > 7 or new_i < 0:
            return False
        #if input is invalid returning false
        if new_j > 7 or new_j < 0:
            return False
        #cheking if the position is available to make a move
        if board[old_i][old_j] == "B":
            return False
        if board[new_i][new_j] != "B":
            return False
        if board[old_i][old_j][0] == "x" or board[old_i][old_j][0] == "X":
            return False
        if board[new_i][new_j] == "B":
            return True

     #Method to check palyer 1 jumps
    def check_player2_jumps(board, old_i, old_j, via_i, via_j, new_i, new_j):
        #if input is invalid returning false
        if new_i > 7 or new_i < 0:
            return False
        #if input is invalid returning false
        if new_j > 7 or new_j < 0:
            return False
         #cheking if the position is available to make a jump
        if board[via_i][via_j] == "B":
            return False
        if board[via_i][via_j][0] == "O" or board[via_i][via_j][0] == "o":
            return False
        if board[new_i][new_j] != "B":
            return False
        if board[old_i][old_j] == "B":
            return False
        if board[old_i][old_j][0] == "x" or board[old_i][old_j][0] == "X":
            return False
        return True

   # method to make a move for player 1 and player 2
    def make_a_move(board, old_i, old_j, new_i, new_j, big_letter, queen_row):
        #storing the posittion of pices in a variable
        letter = board[old_i][old_j][0]
        #taking the diffrence between new position and old position
        i_difference = old_i - new_i
        j_difference = old_j - new_j

        #making the move on the board
        if i_difference == -2 and j_difference == 2:
            board[old_i + 1][old_j - 1] = "B"
        elif i_difference == 2 and j_difference == 2:
            board[old_i - 1][old_j - 1] = "B"
        elif i_difference == 2 and j_difference == -2:
            board[old_i - 1][old_j + 1] = "B"
        elif i_difference == -2 and j_difference == -2:
            board[old_i + 1][old_j + 1] = "B"
        
        #if the piece is on queen rowmaking the piece king using king clsaa 
        if new_i == queen_row:
            letter = big_letter
        board[old_i][old_j] = "B"
        board[new_i][new_j] = letter

    #method to display menu and taking input from user
    def play(self):
        #displying menu
        print("\n##### CHECKERS GAME #####")
        print("\nInstructions to play game:\n")
        print("1.Enter Name of the players before starting. ")
        print("2.Enter 'y' or 'Y' to start game. ")
        print("3.Enter 'y' or 'Y' to making jump mandatory or not by 'n' or 'N'. ")
        print("Now, Enjoy Game!")

        #while loop to make name of player1 mandatory
        while True:
            self.Player1Name = input("\nEnter Player 1 Name: ")
            #checking if input is empty
            if self.Player1Name == "":
                print("Invalid input!")
            else:
                break
        #while loop to make name of player1 mandatory
        while True:
            self.Player2Name = input("\nEnter Player 2 Name: ")
             #checking if input is empty
            if self.Player2Name == "":
                print("Invalid input!")
            else:
                break
        #loop to ask user to start game and is jumping mandetory
        while True:
            begin = input("\nBegin Game Play(Y/N): ")
            if begin == "Y" or begin == "y":
                #making string of palyer name date and time
                self.fileName=f"{self.Player1Name}_{self.Player2Name}_{datetime.datetime.now().strftime('%Y_%m_%d__%H_%M_%p')}.txt"
                #creating empty file in folder
                with open("log.txt", 'w') as fp:
                    #writing in the file game started and name of player
                    fp.write(f"GAME STARTED\n Player 1 Name: {self.Player1Name}\n Player 2 Name: {self.Player2Name}\n")
                #remaning file name usingos module to playernam date and time
                os.rename("log.txt", self.fileName)
                break
            #if input is no exiting the program
            elif begin == "N" or begin == "n":
                print("Game ended!")
                exit()
            #if input is empty displyingmessage
            elif begin == "":
                print("Illegal input!")
            else:
                print("Illegal input!")

        #asking user if jumping is mandatory or not    
        while True:
            answer = input("\nFirst, we need to know, is jumping mandatory?[Y/n]: ")
            if answer == "Y" or answer == "y":
                self.mandatory_jumping = True
                break
            elif answer == "N" or answer == "n":
                self.mandatory_jumping = False
                break
            elif answer == "":
                print("Illegal input!")


        while True:
            #printing board
            self.print_board()
            #writing board to the file 
            with open(self.fileName,"a") as fileObject:
                for item in self.matrix:
                    fileObject.write(f"{item}\n")
                fileObject.close()
            #asking player1 to provide the input     
            if self.player1_turn is True:
                print(f'\n{self.Player1Name}`s turn ({self.Player1Name} pieces are "x".)')
                #calling payer1_input method
                self.player1_input()
            else:
                #asking player1 to provide the input
                print(f'\n{self.Player2Name}`s turn ({self.Player2Name} pieces are "O")')
                #calling payer2_input method
                self.player2_input()
            #checkingif player 1 has no piece on board
            if self.player1_pieces == 0:
                self.print_board()
                #delcaring player 2 as winner
                print(f"{self.Player1Name} have no pieces left.\n{self.Player2Name} Wins!")
                #writing result to file
                with open(self.fileName,"a") as fileObject:
                    fileObject.write(f"{self.Player1Name} have no pieces left.\n{self.Player2Name} Wins!")
                fileObject.close()
                exit()
            #checkingif player 1 has no piece on board
            elif self.player2_pieces == 0:
                self.print_board()
                #delcaring player 2 as winner
                print(f"{self.Player2Name} have no pieces left.\n{self.Player1Name} Wins!")
                with open(self.fileName,"a") as fileObject:
                    fileObject.write(f"{self.Player2Name} have no pieces left.\n{self.Player1Name} Wins!")
                fileObject.close()
                exit()
    
            #checkingfor playerturn
            self.player1_turn = not self.player1_turn
            self.player2_turn = not self.player2_turn

#running the play method using __main__
if __name__ == '__main__':
    #ceating object of class game
    checkers = Game()
    #calling play method
    checkers.play()