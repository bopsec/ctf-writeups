import sys
import random
import math
from pwn import *

# Server connection details
bits_server = "bits.utl"
bits_port = 6175
connection = remote(bits_server, bits_port)

# I'm just defining them here because I use them more than once
currentGame = b"win3"
currentGameStr = "win3"

# Initialize communication with the game server
connection.recvuntil(b"Welcome!")
connection.sendline(currentGame)
connection.recvline()  # Ignore empty line

# Function to read a line from the server
def read_server_line():
    return connection.recvline().decode().strip()

# Function to send a line to the server
def send_to_server(s):
    connection.sendline(str.encode(s))

# Minimum Excludant Function: Find the smallest non-negative integer not in the set
def mex(s):
    for i in range(1000):
        if i not in s:
            return i

# Precompute Grundy numbers (nimbers) for game positions
nimbers = [0] * 1000
for i in range(2, len(nimbers)):
    s = set()
    for j in range(math.ceil(i / 2)):
        s.add(nimbers[j] ^ nimbers[i - j - 1])
    nimbers[i] = mex(s)

# Calculate the combined nimber for a list of group sizes
def nimber_from_group_sizes(group_sizes):
    if not group_sizes:
        return 0
    combined_nimber = nimbers[group_sizes[0]]
    for size in group_sizes[1:]:
        combined_nimber ^= nimbers[size]
    return combined_nimber

# Find the best move that results in a position with a nimber of 0
def find_best_move(game_state, start_index):
    temp_state = list(game_state)

    for index in range(start_index, len(temp_state) - 1):
        if temp_state[index] == "0" or temp_state[index + 1] == "0":
            continue

        temp_state[index] = "0"
        group_sizes = []
        group_size = 1

        # Calculate group sizes after the move
        for i in range(len(temp_state) - 1):
            if temp_state[i] == "1" and temp_state[i + 1] == "1":
                group_size += 1
            elif temp_state[i] == "1" and temp_state[i + 1] == "0":
                if group_size > 1:
                    group_sizes.append(group_size)
                group_size = 1
        if temp_state[-1] == "1" and group_size > 1:
            group_sizes.append(group_size)

        # Check if this move leads to a winning position
        if nimber_from_group_sizes(group_sizes) == 0:
            return index

        temp_state[index] = "1"  # Revert the change

    return -1  # No winning move found

# Main game loop
def startGame():
    while True:
        game_state = read_server_line()
        #print(game_state)

        valid_move_indices = [i for i in range(1024) if game_state[i:i + 2] == '11']

        if not valid_move_indices:
            print("No valid moves")
            print(game_state)
            send_to_server(currentGameStr)
            continue

        selected_index = find_best_move(game_state, 0)
        if selected_index == -1:
            # Random fallback
            selected_index = random.choice(valid_move_indices)

        send_to_server(str(selected_index))
        server_response = read_server_line()

        if server_response == 'You lose!':
            print(server_response)
            send_to_server(currentGame)
        elif not server_response.startswith('My move: '):
            print("did we win?")
            print(server_response)
            sys.exit(1)
    connection.close()

if __name__ == "__main__":
    startGame()
