# Global Settings
# create a map of the wumpus world
global_grid_xmin = 0    #inclusive
global_grid_xmax = 3    #inclusive
global_grid_ymin = 0    #inclusive
global_grid_ymax = 3    #inclusive

global_grid_width = global_grid_xmax-global_grid_xmin
global_grid_height = global_grid_ymax-global_grid_ymin

# take unsafe steps
take_unsafe_steps = True

# declare locations
pit_loc = [[1,3],[3,3],[3,1]]

gold_loc = [2,2]

wumpus_loc = [3,1]


# State Variables
    # and the agent starts at the given coordinate
initial_location = [0,0]
player_cur_loc = [0,0] # [x,y]
    # direction facing
player_cur_direction = "west"

legal_directions = ["north","east","south","west"]  # is ordered list, do not change

    # Wumpus alive
wumpus_alive = True

    # Gold is still on the board
gold_on_board = True

    # arrows left
arrows_left = 1


to_visit_stack = []     # stack of coordinates to visit
dead_ends = []


def check_out_of_bounds(x,y=None):
    if(y==None):    # soft overloading fn
        x,y = x[0],x[1]
    if x<global_grid_xmin or x>global_grid_xmax or y<global_grid_ymin or y>global_grid_ymax:
            return True
    return False


def mark_visited(x,y):
    visited[x][y] = 1

def check_visited(x,y):
    return(visited[x][y])
        


def get_current_block_info():
    """
    returns if current block has stench or breeze or gold
    """
    current_block_info = []

    if(player_cur_loc == gold_loc):
        current_block_info.append("gold")
    # if wumpus is near wumpus location
    if((player_cur_loc[0] == wumpus_loc[0] and player_cur_loc[1] == wumpus_loc[1]+1) or
        (player_cur_loc[0] == wumpus_loc[0]+1 and player_cur_loc[1] == wumpus_loc[1]) or
        (player_cur_loc[0] == wumpus_loc[0] and player_cur_loc[1] == wumpus_loc[1]-1) or
        (player_cur_loc[0] == wumpus_loc[0]-1 and player_cur_loc[1] == wumpus_loc[1])):
        current_block_info.append("stench")

    # if pit is near pit location
    for this_pit in pit_loc:
        if((player_cur_loc[0] == this_pit[0] and player_cur_loc[1] == this_pit[1]+1) or
            (player_cur_loc[0] == this_pit[0]+1 and player_cur_loc[1] == this_pit[1]) or
            (player_cur_loc[0] == this_pit[0] and player_cur_loc[1] == this_pit[1]-1) or
            (player_cur_loc[0] == this_pit[0]-1 and player_cur_loc[1] == this_pit[1])):
            current_block_info.append("breeze")
            break   # to prevent more than one breeze

    return current_block_info

def get_adjacent_blocks_coor(cur_x, cur_y, direction):
    # return the coordinates of the block adjacent to the current block in that direction
    if(direction == "north"):
        return [cur_x,cur_y-1]  # assumming north is y-1
    elif(direction == "east"):
        return [cur_x+1,cur_y]
    elif(direction == "south"):
        return [cur_x,cur_y+1]  # assumming south is y+1
    elif(direction == "west"):
        return [cur_x-1,cur_y]
    else:
        print("Error: invalid direction")
        return None


def check_game_over():
    
    for pit in pit_loc:             # check if player is present inside any pit?
        if pit == player_cur_loc:
            print("Game Over: pit")
            return True
    
    if wumpus_alive == True:        # check if player is present inside wumpus?
        if wumpus_loc == player_cur_loc:
            print("Game Over: wumpus")
            return True
    
    if gold_loc == player_cur_loc:  # check if player is present at gold location?
        print("Gold found, yay!")
        while player_cur_loc!= initial_location:
            return_back(player_cur_loc[0],player_cur_loc[1])
        print("the player is back and the gold is found!")
        return True
    
    # check if player has visited all locations
    for y in range(global_grid_ymin,global_grid_ymax+1):
        for x in range(global_grid_xmin,global_grid_xmax+1):
            if visited[x][y] == 0:
                return False
    print("Game Over: visited all locations")
    return True


def take_action(action_name):
    """
    Possible actions: forward, left, right, shoot, grab
    """
    global player_cur_direction
    global player_cur_loc

    print("Action:",action_name,"   current location:",player_cur_loc,"  current direction:", player_cur_direction)

    # read legal directions index
    cur_direction_index = direction_num(player_cur_direction)
    if(action_name == "left"):
        player_cur_direction = legal_directions[(cur_direction_index-1)%4]
        print_grid()
    elif(action_name == "right"):
        player_cur_direction = legal_directions[(cur_direction_index+1)%4]
        print_grid()
    elif(action_name == "forward"):
        get_next_block_coor = get_adjacent_blocks_coor(player_cur_loc[0],player_cur_loc[1],player_cur_direction)
        if(check_out_of_bounds(get_next_block_coor[0],get_next_block_coor[1])):
            print("Error: cannot move forward, out of bounds")
        else:
            player_cur_loc = get_next_block_coor  
    elif(action_name == "shoot"):
        if(arrows_left > 0):
            arrows_left -= 1

            adjacent_block = get_adjacent_blocks_coor(player_cur_loc[0],player_cur_loc[1],player_cur_direction)
            if(adjacent_block == wumpus_loc):
                print("Wumpus killed!")
                wumpus_alive = False
            else:
                print("Missed Arrow!")



# AI Model
# grid that stores information about where wumpus could be
## All the 2D grids can be accessed as [x][y]
wumpus_possible = []    # init with 1 everywhere

pit_possible = []       # init with 1 everywhere

visited = []            # init with 0 everywhere

def init_model_states():
    for y in range(global_grid_ymin,global_grid_ymax+1):
        new_0row = []
        new_1row = []
        for x in range(global_grid_xmin,global_grid_xmax+1):
            new_1row.append(1)
            new_0row.append(0)
        wumpus_possible.append(new_1row)
        pit_possible.append(new_1row)
        visited.append(new_0row)

        

def update_knowledge(player_cur_loc):
    x,y= player_cur_loc[0],player_cur_loc[1]
    visited[x][y]=1
    current_block_info = get_current_block_info()
    if not("stench" in current_block_info):
        possible_wumpus = [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]
        wumpus_possible[player_cur_loc[0]][player_cur_loc[1]]=0
        for j in range(len(possible_wumpus)):
            if (not(check_out_of_bounds(possible_wumpus[j][0],possible_wumpus[j][1]))):
                wumpus_possible[possible_wumpus[j][0]][possible_wumpus[j][1]]=0
            else:
                continue

    if not("breeze" in current_block_info):
        possible_pit = [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]
        pit_possible[player_cur_loc[0]][player_cur_loc[1]]=0
        for j in range(len(possible_pit)):
            if (not(check_out_of_bounds(possible_pit[j][0],possible_pit[j][1]))):
                pit_possible[possible_pit[j][0]][possible_pit[j][1]]=0
            else:
                continue



    # # did not mark no wumpus when nothing was returned in get_current_block_info 
    # for i in range(len(get_current_block_info())):
    #     if get_current_block_info()[i]!='stench':
    #         possible_wumpus = [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]
    #         for j in range(len(possible_wumpus)):
    #             if (check_out_of_bounds(possible_wumpus[j][0],possible_wumpus[j][1])) and (visited[possible_wumpus[j][0]][possible_wumpus[j][1]]!=1):
    #                 wumpus_possible[possible_wumpus[j][0]][possible_wumpus[j][1]]=0
    #             else:
    #                 continue

    #     if get_current_block_info()[i]!='breeze':
    #         possible_pit = [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]
    #         for j in range(len(possible_pit)):
    #             if (check_out_of_bounds(possible_pit[j][0],possible_pit[j][1])) and (visited[possible_pit[j][0]][possible_pit[j][1]]!=1):
    #                 pit_possible[possible_pit[j][0]][possible_pit[j][1]]=0
    #             else:
    #                 continue

def safe_loc(x,y):
    if (wumpus_possible[x][y]!=1) and (pit_possible[x][y]!=1):
        return True
    else:
        return False



back_home_visited=[] #tracks visited blocks while going home
back_home_deadend=[] #tracks blocks which are dead end while going home


reach_dead_ends = []    # tracks dead ends while reaching destination
reach_visited = []
reach_cached_target_location = [-1,-1]   # stores location for which the above arrays are relevant


def return_back(cur_x,cur_y):
    choices=[]
    for direction in legal_directions:
        next_block = get_adjacent_blocks_coor(cur_x,cur_y,direction)
        if visited[next_block[0]][next_block[1]] and not(check_out_of_bounds(next_block[0],next_block[1])) and safe_loc(next_block[0],next_block[1]) and not (next_block in dead_ends)and not (next_block in back_home_visited)and not (next_block in back_home_deadend):
            choices.append(next_block)
    if(len(choices) == 0):
        back_home_deadend.append([cur_x,cur_y])
        for direction in legal_directions:
            next_visit_block = get_adjacent_blocks_coor(cur_x,cur_y,direction)
            if (safe_loc(next_visit_block[0],next_visit_block[1]) and not(next_visit_block in dead_ends)and not(next_visit_block in back_home_deadend) and not(check_out_of_bounds(next_visit_block[0],next_visit_block[1]))):
                choices.append(next_visit_block)
    print("choices:",choices)
    next_block_final = choices[0]
    back_home_visited.append(next_block_final)
    action_implementation(next_block_final)
    return(player_cur_loc[0],player_cur_loc[1])

def manhatten_distance(cur_x,cur_y,new_x,new_y):
    return(abs(cur_x-new_x)+abs(cur_y-new_y))

def reach_position(new_x,new_y):

    # clear dead_ends if target location is changed
    if(reach_cached_target_location[0] != new_x or reach_cached_target_location[1] != new_y):
        reach_dead_ends.clear()
        reach_visited.clear()
        reach_cached_target_location[0] = new_x
        reach_cached_target_location[1] = new_y

    cur_x,cur_y = player_cur_loc[0],player_cur_loc[1]
    choices=[]
    for direction in legal_directions:
        next_block = get_adjacent_blocks_coor(cur_x,cur_y,direction)
        if visited[next_block[0]][next_block[1]] and not(check_out_of_bounds(next_block[0],next_block[1])) and safe_loc(next_block[0],next_block[1]) and not (next_block in dead_ends)and not (next_block in reach_visited)and not (next_block in reach_dead_ends):
            choices.append(next_block)
    if(len(choices) == 0):
        reach_dead_ends.append([cur_x,cur_y])
        for direction in legal_directions:
            next_visit_block = get_adjacent_blocks_coor(cur_x,cur_y,direction)
            if (safe_loc(next_visit_block[0],next_visit_block[1]) and not(next_visit_block in dead_ends)and not(next_visit_block in reach_dead_ends) and not(check_out_of_bounds(next_visit_block[0],next_visit_block[1]))):
                choices.append(next_visit_block)
    print("choices:",choices)

    # chooses the next block according to manhatten distance as heuristic
    min_manh_indx = 0
    min_manh_dist = manhatten_distance(choices[0][0],choices[0][1],new_x,new_y)
    if(len(choices) > 1):
        for indx,choice in iter(choices):
            if(indx == 0):
                continue
            if(manhatten_distance(cur_x,cur_y,choice[0],choice[1]) < min_manh_dist):
                min_manh_indx = indx
                min_manh_dist = manhatten_distance(cur_x,cur_y,choice[0],choice[1])

    next_block_final = choices[min_manh_indx]

    reach_visited.append(next_block_final)
    action_implementation(next_block_final)
    return(player_cur_loc[0],player_cur_loc[1])

        

def planner(cur_x, cur_y):
    # make a list of all nearby options with always safety first then not visited
    choices = []
    for direction in legal_directions:
        # get next direction
        next_visit_block = get_adjacent_blocks_coor(cur_x,cur_y,direction)
        if (safe_loc(next_visit_block[0],next_visit_block[1])                   # the location is safe (no pit, no wumpus)
            and not(visited[next_visit_block[0]][next_visit_block[1]])          # the location is not visited
            and not(next_visit_block in dead_ends)                              # the location is not a dead end
            and not(check_out_of_bounds(next_visit_block[0],next_visit_block[1]))):  # the location is inside the grid

            choices.append(next_visit_block)    # insert to list of possible choices

    # if no valid safe option is found in first local search, then it can also visit the last visited node and marks current node as dead_end
    if(len(choices) == 0):
        dead_ends.append([cur_x,cur_y])
        for direction in legal_directions:
            next_visit_block = get_adjacent_blocks_coor(cur_x,cur_y,direction)
            if (safe_loc(next_visit_block[0],next_visit_block[1]) and not(next_visit_block in dead_ends) and not(check_out_of_bounds(next_visit_block[0],next_visit_block[1]))):
                choices.append(next_visit_block)    ## adding last visited node as next to visit node

    # After the choice list is generated, pick first and commit first action
    # add all other choices to to_visit.
    next_block_final = choices[0]

    # if more than one choices, add other choices to_visit_stack
    if(len(choices) > 1):
        for i in range(1,len(choices)):
            if not(choices[i] in to_visit_stack):
                to_visit_stack.append(choices[i])

    # mark_visited(next_block_final[0],next_block_final[1])
    action_implementation(next_block_final)


def print_grid():
    # print grid with w for wumpus, p for pit, g for gold, ^v>< for agent with direction
    for y in range(global_grid_ymin,global_grid_ymax+1):
        for x in range(global_grid_xmin,global_grid_xmax+1):
            print(x,",",y,sep="",end="")
            if([x,y] == player_cur_loc):
                character_array = ["^",">","v","<"]
                print(character_array[direction_num(player_cur_direction)],end="")
            elif([x,y] == wumpus_loc):
                print("w",end="")
            elif([x,y] in pit_loc):
                print("p",end="")
            elif([x,y] == gold_loc):
                print("g",end="")
            else:
                print(" ",end="")
            print("\t|",end="")
        print("\n_________________________________\n")




def direction_num(direction):
    if direction=="north":
        dir_num=0
    elif direction=="east":
        dir_num=1
    elif direction =="south":
        dir_num=2
    elif direction =="west":
        dir_num=3
    return dir_num

"""def num_to_direction(dir_num):
    # return the direction based on the numerical input
    if dir_num == 0:
        return "north"
    elif dir_num == 1:
        return "east"
    elif dir_num == 2:
        return "south"
    elif dir_num == 3:
        return "west"
    else:
        print("Error: invalid direction number")
        return None"""
    
def get_direction_between_blocks(cur_x, cur_y, new_x, new_y):
    # return the direction from the current block to the new block
    if new_x == cur_x and new_y == cur_y + 1:
        return "south"      ## changed because assumming y increase in south.
    elif new_x == cur_x + 1 and new_y == cur_y:
        return "east"
    elif new_x == cur_x and new_y == cur_y - 1:
        return "north"      ## changed because assumming y increase in south.
    elif new_x == cur_x - 1 and new_y == cur_y:
        return "west"
    else:
        print("Error: invalid coordinates")
        return None
    
def action_implementation(new_loc):
    "performs action to go to the new location"
    x,y= player_cur_loc[0],player_cur_loc[1]
    x1,y1=new_loc[0],new_loc[1]
    if check_out_of_bounds(new_loc):
        print("Error, out of bounds")
    cur_dir = direction_num(player_cur_direction)
    new_dir = direction_num(get_direction_between_blocks(x,y,x1,y1))
    diff=new_dir-cur_dir
    if diff%4==0:
        take_action("forward")
    elif diff%4==1:
        take_action("right")
        take_action("forward")
    elif diff ==2 or diff==-2:
        take_action("right")
        take_action("right")
        take_action("forward")
    elif diff ==-1 or diff==3:
        take_action("left")
        take_action("forward")
    else:
        print("Error: Unable to determine direction")
    if(player_cur_loc != new_loc):
        print("Error: Unable to reach specified location.")
    else:
        mark_visited(player_cur_loc[0],player_cur_loc[1])
        print("the player is at the new location",player_cur_loc) #prints the new location    

def safe_loc(x,y):
    if(check_out_of_bounds(x,y)):
        return False
    if (wumpus_possible[x][y]!=1) and (pit_possible[x][y]!=1):
        return True
    else:
        return False 

def print_knowledge():
    # print("wumpus_possible",wumpus_possible)
    # print grid of wumpus_possible
    print("WUMPUS POSSIBLITIES")
    for y in range(global_grid_ymin,global_grid_ymax+1):
        for x in range(global_grid_xmin,global_grid_xmax+1):
            print(wumpus_possible[x][y],end="|")
        print("")

    print("PIT POSSIBILITIES")
    for y in range(global_grid_ymin,global_grid_ymax+1):
        for x in range(global_grid_xmin,global_grid_xmax+1):
            print(pit_possible[x][y],end="|")
        print("")
    print("VISITED LOCATIONS")
    for y in range(global_grid_ymin,global_grid_ymax+1):
        for x in range(global_grid_xmin,global_grid_xmax+1):
            print(visited[x][y],end="|")
        print("")


init_model_states()



############### Playground Testing ###############
# player_cur_loc = [2,1]
print("current block info",get_current_block_info())


# simulation loop
while(1):
    if(check_game_over()):
        print("Game Over!")
        print("player_cur_loc",player_cur_loc)
        break

    update_knowledge(player_cur_loc)

    print_knowledge()

    print("current location:",player_cur_loc,"  current direction:", player_cur_direction)
    print_grid()

    planner(player_cur_loc[0],player_cur_loc[1])



