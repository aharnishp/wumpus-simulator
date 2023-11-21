# Global Settings
    # create a map of the wumpus world
global_grid_xmin = 0    #inclusive
global_grid_xmax = 3    #inclusive
global_grid_ymin = 0    #inclusive
global_grid_ymax = 3    #inclusive

global_grid_width = global_grid_xmax-global_grid_xmin
global_grid_height = global_grid_ymax-global_grid_ymin

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
            if visited[y][x] == 0:
                return False
    print("Game Over: visited all locations")
    return True



# AI Model
# grid that stores information about where wumpus could be
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

def update_knowledge():
    pass

def check_block_out_of_bounds(x,y):
    if(x < global_grid_xmin or x > global_grid_xmax or
        y < global_grid_ymin or y > global_grid_ymax):
        return True
    return False


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
        if(check_block_out_of_bounds(get_next_block_coor[0],get_next_block_coor[1])):
            print("Error: cannot move forward, out of bounds")
        


    elif(action_name == "shoot"):
        if(arrrows_left > 0):
            arrows_left -= 1

            adjacent_block = get_adjacent_blocks_coor(player_cur_loc[0],player_cur_loc[1],player_cur_direction)
            if(adjacent_block == wumpus_loc):
                print("Wumpus killed!")
                wumpus_alive = False
            else:
                print("Missed Arrow!")




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

    update_knowledge()