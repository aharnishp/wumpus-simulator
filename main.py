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
player_cur_loc = [1,1] # [x,y]
    # direction facing
player_cur_direction = "west"

legal_directions = ["north","east","south","west"]  # is ordered list, do not change

    # Wumpus alive
wumpus_alive = True

    # arrows left
arrows_left = 1


to_visit_stack = []     # stack of coordinates to visit
dead_ends = []


def check_out_of_bounds(x,y):
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
        return [cur_x,cur_y+1]
    elif(direction == "east"):
        return [cur_x+1,cur_y]
    elif(direction == "south"):
        return [cur_x,cur_y-1]
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
        print("Game Over: gold")
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

    # read legal directions index
    cur_direction_index = legal_directions.index(player_cur_direction)
    if(action_name == "left"):
        player_cur_direction = legal_directions[(cur_direction_index-1)%4]
    elif(action_name == "right"):
        player_cur_direction = legal_directions[(cur_direction_index+1)%4]
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
    for i in range(len(get_current_block_info())):
        if get_current_block_info()[i]!='stench':
            possible_wumpus = [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]
            for j in range(len(possible_wumpus)):
                if (check_out_of_bounds(possible_wumpus[j][0],possible_wumpus[j][1])) and (visited[possible_wumpus[j][0]][possible_wumpus[j][1]]!=1):
                    wumpus_possible[possible_wumpus[j][0]][possible_wumpus[j][1]]=0
                else:
                    continue

        if get_current_block_info()[i]!='breeze':
            possible_pit = [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]
            for j in range(len(possible_pit)):
                if (check_out_of_bounds(possible_pit[j][0],possible_pit[j][1])) and (visited[possible_pit[j][0]][possible_pit[j][1]]!=1):
                    pit_possible[possible_pit[j][0]][possible_pit[j][1]]=0
                else:
                    continue

def safe_loc(x,y):
    if (wumpus_possible[x][y]!=1) and (pit_possible[x][y]!=1):
        return True
    else:
        return False

def planner(cur_x, cur_y):
    # make a list of all nearby options with always safety first then not visited
    choices = []
    for direction in legal_directions:
        # get next direction
        next_visit_block = get_adjacent_blocks_coor(cur_x,cur_y,direction)
        if (safe_loc(next_visit_block) 
            and not(visited[next_visit_block[0]][next_visit_block[1]]) 
            and not(next_visit_block in dead_ends) 
            and check_out_of_bounds(next_visit_block[0],next_visit_block[1])):

            choices.append(next_visit_block)

    # if no valid safe option is found in first local search, then it can also visit the last visited node and marks current node as dead_end
    dead_ends.append(next_visit_block)
    for direction in legal_directions:
        if (safe_loc(next_visit_block) and not(next_visit_block in dead_ends) and check_out_of_bounds(next_visit_block[0],next_visit_block[1])):
            choices.append(next_visit_block)    ## adding last visited node as next to visit node

    



    # if more than one choices, add other choices to_visit_stack
    if(len(choices) > 1):
        for i in range(1,len(choices)):
            to_visit_stack.append(next_visit_block[i])
    mark_visited(choices[0][0],choices[0][1])

    # for 


init_model_states()

print("wumpus_possible",wumpus_possible)
print("pit_possible",pit_possible)
print("visited",visited)

############### Playground Testing ###############
player_cur_loc = [2,1]
print("current block info",get_current_block_info())


# simulation loop
while(1):
    if(check_game_over()):
        print("Game Over!")
        print("player_cur_loc",player_cur_loc)
        break

    update_knowledge(player_cur_loc)

    planner(player_cur_loc)


     