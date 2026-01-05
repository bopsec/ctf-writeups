import numpy as np
import random
import gymnasium as gym
from gymnasium import spaces
import random

MIN_ROTATION_MOVES = 3
MAX_ROTATION_MOVES = 7
PLAYER_1 = 1
PLAYER_2 = -1


class Rotate4Env(gym.Env):

    metadata = {'render_modes': ['human', 'ansi']}

    def __init__(self, render_mode=None, fixed_mechanics=True, verbose=False):
        super().__init__()
        self.rows = 7
        self.cols = 7
        self.render_mode = render_mode
        self.verbose = verbose

        self.action_space = spaces.Discrete(self.cols)

        self.observation_space = spaces.Box(low=0, high=1, shape=(3, 7, 7), dtype=np.float32)

        self.fixed_mechanics = fixed_mechanics
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.board = np.zeros((self.rows, self.cols), dtype=np.int8)
        self.current_player = PLAYER_1
        self.terminated = False
        self.winner = 0

        self.rot_dir_idx = 0  # Used for alternating if fixed current_env.rot_dir_idx
        self._set_rotation_parameters()

        return self._get_obs(), {}

    def _set_rotation_parameters(self):
        if self.fixed_mechanics:
            self.moves_until_rotation = 5
            # Alternate directions based on the index
            self.next_rotation_dir = 1 if self.rot_dir_idx % 2 == 0 else -1
            self.rot_dir_idx += 1
        else:
            self.moves_until_rotation = random.randint(3, 7)
            self.next_rotation_dir = random.choice([1, -1])  # 1=CCW, -1=CW

    def step(self, action):
        if self.terminated:
            return self._get_obs(), 0, True, False, {}

        if self.board[0, action] != 0:
            reward = -10
            self.last_reward = reward
            return self._get_obs(), reward, False, False, {"error": "invalid"}

        row = np.where(self.board[:, action] == 0)[0][-1]
        self.board[row, action] = self.current_player

        if self._check_win_vectorized(self.current_player):
            self.terminated = True
            self.winner = self.current_player
            reward = 1
            self.last_reward = reward
            return self._get_obs(), reward, True, False, {}

        self.moves_until_rotation -= 1

        if self.moves_until_rotation == 0:
            self._apply_rotation_mechanics()

            p1_win = self._check_win_vectorized(1)
            p2_win = self._check_win_vectorized(-1)

            if p1_win or p2_win:
                self.terminated = True
                if p1_win and p2_win:
                    self.winner = self.current_player  # Active player priority
                else:
                    self.winner = 1 if p1_win else -1

                reward = 1 if self.winner == self.current_player else -1
                self.last_reward = reward
                return self._get_obs(), reward, True, False, {}

            self._set_rotation_parameters()

        if np.all(self.board != 0):
            self.terminated = True
            self.last_reward = 0
            return self._get_obs(), 0, True, False, {}

        self.current_player *= -1
        self.last_reward = 0
        return self._get_obs(), 0, False, False, {}

    def is_valid_action(self, action):
        """
        Helper for the Tournament loop to check if a move is legal.
        Returns True if the column is not full (top row is 0).
        """
        if action < 0 or action >= self.cols:
            return False
        return self.board[0, action] == 0

    def _apply_rotation_mechanics(self):
        # Rotate 90 deg. k=1 (CCW) if dir=1, k=-1 (CW) if dir=-1
        k = 1 if self.next_rotation_dir == 1 else -1
        self.board = np.rot90(self.board, k=k)

        # Apply Gravity (Fast Vectorized)
        for c in range(self.cols):
            col = self.board[:, c]
            nonzero = col[col != 0]
            new_col = np.zeros(self.rows, dtype=np.int8)
            if len(nonzero) > 0:
                new_col[-len(nonzero):] = nonzero
            self.board[:, c] = new_col

    def _check_win_vectorized(self, player):
        b = (self.board == player).astype(np.int8)
        # Horizontal, Vertical, Diagonals
        if np.any(b[:, :-3] + b[:, 1:-2] + b[:, 2:-1] + b[:, 3:] == 4): return True
        if np.any(b[:-3, :] + b[1:-2, :] + b[2:-1, :] + b[3:, :] == 4): return True
        if np.any(b[:-3, :-3] + b[1:-2, 1:-2] + b[2:-1, 2:-1] + b[3:, 3:] == 4): return True
        if np.any(b[:-3, 3:] + b[1:-2, 2:-1] + b[2:-1, 1:-2] + b[3:, :-3] == 4): return True
        return False

    def _get_obs(self):
        obs = np.zeros((3, self.rows, self.cols), dtype=np.float32)
        obs[0] = (self.board == self.current_player)
        obs[1] = (self.board == -self.current_player)
        obs[2, :, :] = self.moves_until_rotation / 7.0
        obs[2, 0, 0] = self.next_rotation_dir
        return obs

    def render(self):
        """
        Public render method that delegates to _render_ansi.
        """
        output = self._render_ansi()

        if self.render_mode == 'human':
            print(output)

        return output

    def valid_actions(self):
        return [c for c in range(self.cols) if self.board[0, c] == 0]

    def get_random_action(self):
        actions = self.valid_actions()  # Get the valid actions
        if actions:  # Check if there are valid actions
            return np.random.choice(actions)  # Pick a random action
        return None  # Return None if no valid actions are available

    def _render_ansi(self):
        """
        Internal ANSI string builder.
        """
        piece_map = {
            -1: "R",  # Player 2
            1: "Y",  # Player 1
            0: "."
        }

        s = ""
        s += "\n=== ConnectFour90Lite ({}x{}) ===\n".format(self.rows, self.cols)
        s += "Current Player: {}\n".format("Y" if self.current_player == PLAYER_1 else "R")
        s += "Rotation in: {}\n".format(self.moves_until_rotation)

        is_acw = (self.rot_dir_idx - 1) % 2 == 0 if self.fixed_mechanics else (self.next_rotation_dir == 1)

        s += "Next Rotation: {}\n".format("ACW" if is_acw else "CW")

        s += "    " + "   ".join(str(c) for c in range(self.cols)) + "\n"

        for r in range(self.rows):
            row_str = " | ".join(piece_map[int(self.board[r, c])] for c in range(self.cols))
            s += f"{r} | {row_str} |\n"

        s += "-" * (self.cols * 4 + 6) + "\n"
        return s