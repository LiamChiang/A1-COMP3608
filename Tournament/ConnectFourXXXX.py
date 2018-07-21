import numpy
import sys
import copy
# import Queue as Q

global_yellow_column = 0
global_red_column = 0


#node property
# class Node(object):
#     def __init__(self, i_state, i_player, i_column):
#         self.i_player = i_player
#         self.i_state = i_state
#         self.i_column = i_column
#         self.children = []
 
#     def createChildren(self, c_state, c_player, c_column):
#         self.children.append( Node(c_state, c_player, c_column))

#add token in game
def Add_Token(player, matrix, colNo):
    colNo = int(colNo)
    for row in range(0,6):
        if (matrix[row][colNo] == "."):
            # print(matrix[row][colNo])
            matrix[row][colNo] = player
            return matrix
        else:
            continue

    return matrix, colNo

#count number in a row in board game
def Count_All(player, matrix):
    count = 0
    for row in range(0,6):
        for col in range(0,7):
            # print(row, col)
            if(matrix[row][col] == player):
                count = count + 1
    return count

def Find_Diagonal(row, col, matrix, expNum):
    total = 0
    count = 0
    if row + expNum - 1 < 6 and col + expNum - 1 < 7:
        for i in range(expNum):
            if matrix[row][col] == matrix[row + i][col + i]:
                count += 1
            else:
                break
    if count == expNum:
        total += 1

    count = 0
    if row - expNum + 1 >= 0 and col + expNum - 1 < 7:
        for i in range(expNum):
            if matrix[row][col] == matrix[row - i][col + i]:
                count += 1
            else:
                break
    if count == expNum:
        total += 1

    return total

def Find_Vertical(row, col, matrix, expNum):
    count = 0
    if row + expNum - 1 < 6:
        for i in range(expNum):
            if matrix[row][col] == matrix[row + i][col]:
                count += 1
            else:
                break
    if count == expNum:
        return 1

    else:
        return 0
def Find_Horizontal(row, col, matrix, expNum):
    count = 0
    if col + expNum - 1 < 7:
        for i in range(expNum):
            if matrix[row][col] == matrix[row][col + i]:
                count += 1
            else:
                break
    if count == expNum:
        return 1
    else:
        return 0

def Find_Player(matrix, player, expNum):
    count = 0
    for i in range(6):
        for j in range(7):
            if matrix[i][j] == player:
                count += Find_Vertical(i, j, matrix, expNum)
                count += Find_Horizontal(i, j, matrix, expNum)
                count += Find_Diagonal(i, j, matrix, expNum)

    return count

def Check_Depth(matrix):
    count = 0
    for i in range(6):
        for j in range(7):
            if matrix[i][j] == ".":
                count += Find_Horizontal(i, j, matrix, 7)
    # print(count)
    return int(6 - count)

#Calculate the score for each player's state
def ScoreCal(player,matrix):

    two_in_a_row = Find_Player(matrix, player, 2)
    three_in_a_row = Find_Player(matrix, player, 3)
    four_in_a_row = Find_Player(matrix, player, 4)
    all_place = Count_All(player, matrix)

    result1 = two_in_a_row - 2 * three_in_a_row - 3 * four_in_a_row
    result2 = three_in_a_row - 2 * four_in_a_row

    if(result1 < 0):
        result1 = 0
    if(result2 < 0):
        result2 = 0
   
   
    return int(all_place + 10 * (result1) + 100 * (result2) + 1000 * four_in_a_row)

#Evaluation red - yellow
def Evaluation(matrix, red, yellow):
    return int(ScoreCal(red, matrix) - ScoreCal(yellow, matrix))

def change_Player(player):
    if(player == "r"):
        player = "y"
    elif(player == "y"):
        player = "r"
    return player

def alphabeta(state, player, depth, alpha, beta):
    
    global global_red_column
    global global_yellow_column
    
    # if its non terminal leaf node
    if(depth == 0 or ScoreCal("r", state) >= 1000 or ScoreCal("y", state) >= 1000):
        if(ScoreCal("r", state) >= 1000):
            return 10000
        elif(ScoreCal("y", state) >= 1000):
            return -10000
        return int(Evaluation(state, "r", "y"))
     
     #if maximizing player
    if (player == "r"):
 
        v = float('-inf')
        #init node
        # node = Node(state, player)      
        #expand the children
        # if not node.children:
        # parent = copy.deepcopy(state)
        
        state_list = {}
        parent = copy.deepcopy(state)
        state_list[3] = Add_Token(player, parent, 3)
        parent = copy.deepcopy(state)
        state_list[2] = Add_Token(player, parent, 2)
        parent = copy.deepcopy(state)
        state_list[4] = Add_Token(player, parent, 4)
        parent = copy.deepcopy(state)
        state_list[0] = Add_Token(player, parent, 0)
        parent = copy.deepcopy(state)
        state_list[1] = Add_Token(player, parent, 1)
        parent = copy.deepcopy(state)
        state_list[5] = Add_Token(player, parent, 5)
        parent = copy.deepcopy(state)
        state_list[6] = Add_Token(player, parent, 6)

        for key in state_list.keys():
        # for col in range(0, 7):
            # parent = copy.deepcopy(state)
            # new_state = Add_Token(player, parent, col)
            new_player = change_Player(player)
            value = alphabeta(state_list[key], new_player, int(depth - 1), alpha, beta)
            v = max(v, value)
 
            if(v > alpha):
                global_red_column = key
                alpha = v
            # alpha = max(alpha, v)
            
            if(beta <= alpha):
                break
 
        return int(v)
    #if minimizing player    
    if (player == "y"):
 
        v = float('inf')
        #init node
        # node = Node(state, player)
        #expand the children
        # if not node.children:
        
        state_list = {}
        parent = copy.deepcopy(state)
        state_list[3] = Add_Token(player, parent, 3)
        parent = copy.deepcopy(state)
        state_list[2] = Add_Token(player, parent, 2)
        parent = copy.deepcopy(state)
        state_list[4] = Add_Token(player, parent, 4)
        parent = copy.deepcopy(state)
        state_list[0] = Add_Token(player, parent, 0)
        parent = copy.deepcopy(state)
        state_list[1] = Add_Token(player, parent, 1)
        parent = copy.deepcopy(state)
        state_list[5] = Add_Token(player, parent, 5)
        parent = copy.deepcopy(state)
        state_list[6] = Add_Token(player, parent, 6)

        # parent = copy.deepcopy(state)
        # for col in range(0, 7):
        for key in state_list.keys():
            # parent = copy.deepcopy(state)
            # new_state = Add_Token(player, parent, col)
            new_player = change_Player(player)
            value = alphabeta(state_list[key], new_player, int(depth - 1), alpha, beta)
            v = min(v, value)
 
            if(v < beta):
                global_yellow_column = key
                beta = v
 
            if(beta <= alpha):
                break
 
        return int(v)
test = sys.argv

state = test[1]
player = test[2]

if (test[2] == "red" or test[2] == "r"):
    player = "r"
elif (test[2] == "yellow" or test[2] == "y"):
    player = "y"

matrix = []

row_state = state.split(",")

for i in row_state:
    testing = list(i)
    matrix.append(testing)

alphabeta(matrix, player, Check_Depth(matrix), float('-inf'), float('inf'))

if(player == "r"):
    print(global_red_column)    
elif(player == "y"):
    print(global_yellow_column)










