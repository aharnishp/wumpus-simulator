# Global Settings
    # create a map of the wumpus world
global_grid_xmin = 0
global_grid_xmax = 3
global_grid_ymin = 0
global_grid_ymax = 3

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

    # Wumpus alive
wumpus_alive = True

def check_out_of_bounds(x,y):
    if x<global_grid_xmin or x>global_grid_xmax or y<global_grid_ymin or y>global_grid_ymax:
            return True
    return False

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


def update_knowledge(player_cur_loc):
    x,y= player_cur_loc[0],player_cur_loc[1]
    visited[x][y]=1
    for i in range(len(get_current_block_info)):
        if get_current_block_info[i]=='stench':
            possible_wumpus = [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]
            for j in range(len(possible_wumpus)):
                if (check_out_of_bounds(possible_wumpus[j][0],possible_wumpus[j][1])) and (visited[possible_wumpus[j][0]][possible_wumpus[j][1]]!=1):
                    wumpus_possible[possible_wumpus[j][0]][possible_wumpus[j][1]]=1
                else:
                    continue
        if get_current_block_info[i]=='breeze':
            possible_pit = [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]
            for j in range(len(possible_pit)):
                if (check_out_of_bounds(possible_pit[j][0],possible_pit[j][1])) and (visited[possible_pit[j][0]][possible_pit[j][1]]!=1):
                    pit_possible[possible_pit[j][0]][possible_pit[j][1]]=1
                else:
                    continue



    
            
    



#init_model_states()

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
     