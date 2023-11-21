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
    
            
    



#init_model_states()

print("wumpus_possible",wumpus_possible)
print("pit_possible",pit_possible)
print("visited",visited)

# simulation loop
while(1):
    pass