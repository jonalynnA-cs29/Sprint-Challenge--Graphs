from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

'''
What am I trying to do?
Fill traversal room that when walked in order will visit every room on the map at least once
If you hit a deadend -> backtrack(need way to reverse direction) to nearest room with unexplored paths
so go through all the rooms
get position and possible exits
check for room in reverse until all are visited
'''

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
opposite_direction = []

room = {}  # dict for the rooms
opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
# where is the player , starting point 0
room[0] = player.current_room.get_exits()
complete_path = []
print(room[0])
print(len(room))

print(len(room_graph) - 1)
print(len(room_graph))

# so go through all the rooms:
while len(room) < len(room_graph) - 1:
    # get the players starting position and all the possible exits:
    if player.current_room.id not in room:
        room[player.current_room.id] = player.current_room.get_exits()
        # check for rooms in reverse until all rooms are visited
        previous_room = opposite_direction[-1]
        room[player.current_room.id].remove(previous_room)

    # finally after getting to the last room:
    while len(room[player.current_room.id]) < 1:
        # add all rooms to visited:
        visited = opposite_direction.pop()
        # and append visited to the test room:
        traversal_path.append(visited)
        # have the player go through the copy of all rooms:
        player.travel(visited)

    # finally get all the exits and append them to the test room:
    exits = room[player.current_room.id].pop()
    traversal_path.append(exits)
    # also append the exits to reversed room
    opposite_direction.append(opposites[exits])
    # have the player travel through all the exits
    player.travel(exits)

# then get the traversed room
# and print all the possible paths from start to end
if len(traversal_path) < 9999:
    for i in traversal_path:
        print(f"Go \033[96m'{i}'\033[37m to get to the next room")

world.print_rooms()

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"\n\033[92mTESTS PASSED:\033[37m {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("\033[31mTESTS FAILED:\033[37m INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
