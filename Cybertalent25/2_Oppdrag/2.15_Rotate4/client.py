#client
import socket
import json
import uuid
import numpy as np
import sys
from rotate4_env import Rotate4Env, PLAYER_1, PLAYER_2
from agent import RandomAgent, MinimaxAgent

HOST = 'rotate4'
PORT = 65432
verbose = True
RECEIVE_BUFFER = b""

def _receive_data(sock):
    """Reads data from the socket until a newline delimiter is found and returns a JSON object."""
    global RECEIVE_BUFFER

    while True:
        while b'\n' not in RECEIVE_BUFFER:
            try:
                chunk = sock.recv(4096)
                if not chunk: return None
                RECEIVE_BUFFER += chunk
            except Exception:
                return None

        message_end = RECEIVE_BUFFER.find(b'\n')
        message = RECEIVE_BUFFER[:message_end].decode('utf-8').strip()
        RECEIVE_BUFFER = RECEIVE_BUFFER[message_end + 1:]

        if not message: continue

        try:
            return json.loads(message)
        except json.JSONDecodeError:
            print(f"\n[Error] Failed to decode server message.")
            return None


def get_user_input(prompt, default_value):
    """Prompts the user for input with a default option."""
    return input(f"{prompt} (Default: {default_value}): ") or default_value


def display_opponent_stats(opponent_stats, opponent_name):
    """Prints the current session's win/loss/draw record against the current opponent."""
    if opponent_name not in opponent_stats:
        return

    stats = opponent_stats[opponent_name]
    wins = stats['wins']
    losses = stats['losses']
    draws = stats['draws']
    total_games = wins + losses + draws

    if total_games == 0:
        return

    win_percent = (wins / total_games) * 100

    print(f"[Stats] W/L/D: {wins}/{losses}/{draws} | Win %: {win_percent:.2f}% (Total: {total_games})")


def main():
    client_id = str(uuid.uuid4())
    username = client_id

    print("\n--- Connect Four Challenge Client ---")


    print(f"Client ID: {client_id}")
    print("-" * 40)

    local_env = Rotate4Env()

    #### Insert your own agent that has get_action(env) implementet

    my_agent = MinimaxAgent(depth=5)

    opponent_stats = {}
    current_opponent = None
    player = None

    def sync_env(response):
        """Syncs the local environment state with the server's state."""
        if 'board' in response:
            local_env.board = np.array(response['board'])
        local_env.moves_until_rotation = response.get('moves_until_rot', 7)
        local_env.next_rotation_dir = response.get('next_rot_dir', 1)
        local_env.rotation_event_counter = response.get('rot_counter', 0)
        local_env.current_player = response.get('turn', PLAYER_1)
        local_env.terminated = response.get('terminated', False)


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            print(f"[Fatal] Could not connect to the server at {HOST}:{PORT}. Is the server running?")
            sys.exit(1)

        handshake_data = {
            'client_id': client_id,
            'username': username,
        }
        s.sendall(json.dumps(handshake_data).encode() + b'\n')

        while True:
            resp = _receive_data(s)
            if not resp:
                print("Connection closed by server.")
                break

            status = resp.get('status')

            if status in ('game_start', 'board_update'):
                sync_env(resp)

            if status == 'session_end':
                print("\n" + "="*50)
                print("CHALLENGE COMPLETE! FINAL RESULTS")
                if 'FLAG' in resp:
                    print(f"-> UNLOCKED FLAG: {resp['FLAG']}")

                print(resp['final_message'])

                if 'final_gauntlet_percent' in resp:
                     print(f"Final Score: {resp['final_gauntlet_percent']}")

                print("="*50)
                break

            elif status == 'game_start':
                player = PLAYER_1 if resp['you_start'] else PLAYER_2

                # Check for new opponent
                if resp['opponent'] != current_opponent:
                    current_opponent = resp['opponent']
                    print(f"\n--- New Opponent: {current_opponent} ---")
                    if current_opponent not in opponent_stats:
                        opponent_stats[current_opponent] = {'wins': 0, 'losses': 0, 'draws': 0}


            elif status == 'game_end':
                final_result = resp.get('final_result')

                if current_opponent and final_result:
                    if final_result == 'Client':
                        opponent_stats[current_opponent]['wins'] += 1
                    elif final_result == 'Server':
                        opponent_stats[current_opponent]['losses'] += 1
                    elif final_result == 'Draw':
                        opponent_stats[current_opponent]['draws'] += 1

                if verbose:
                    print(local_env.render())
                display_opponent_stats(opponent_stats, current_opponent)


                continue

            if not local_env.terminated and local_env.current_player == player:
                col = my_agent.get_action(local_env)

                if local_env.is_valid_action(col):
                    s.sendall(json.dumps({'action': int(col)}).encode() + b'\n')
                else:
                    print(f"[Fatal] Agent proposed invalid move ({col}). Disconnecting.")
                    break


if __name__ == "__main__":
    main()
