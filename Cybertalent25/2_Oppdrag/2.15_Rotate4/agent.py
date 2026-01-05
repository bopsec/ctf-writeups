from abc import ABC, abstractmethod
import numpy as np

class Agent(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_action(self, env, render=False):
        raise NotImplemented


class RandomAgent(Agent):
    def __init__(self):
        self.name = "random"

    def get_action(self, env, render=False):
        return env.get_random_action()


class MinmaxAgent(Agent):
    def __init__(self, depth=5):
        self.name = "minmax"
        self.depth = depth

    def get_action(self, env, render=False):
        valid_actions = env.valid_actions()
        if not valid_actions:
            return None
        if len(valid_actions) == 1:
            return valid_actions[0]

        player = env.current_player
        best_action = valid_actions[0]
        best_score = float('-inf')

        # Order moves: center first for better pruning
        center = env.cols // 2
        valid_actions = sorted(valid_actions, key=lambda x: abs(x - center))

        for action in valid_actions:
            env_copy = self.clone_env(env)
            env_copy.step(action)
            score = self.minmax(env_copy, self.depth - 1, float('-inf'), float('inf'), False, player)
            if score > best_score:
                best_score = score
                best_action = action

        return best_action

    def clone_env(self, env):
        from rotate4_env import Rotate4Env
        new_env = Rotate4Env()
        new_env.board = env.board.copy()
        new_env.current_player = env.current_player
        new_env.terminated = env.terminated
        new_env.winner = getattr(env, 'winner', 0)
        new_env.moves_until_rotation = env.moves_until_rotation
        new_env.next_rotation_dir = env.next_rotation_dir
        new_env.rot_dir_idx = getattr(env, 'rot_dir_idx', 0)
        new_env.fixed_mechanics = getattr(env, 'fixed_mechanics', True)
        return new_env

    def minmax(self, env, depth, alpha, beta, is_max, player):
        if env.terminated:
            if env.winner == player:
                return 10000 + depth
            elif env.winner == -player:
                return -10000 - depth
            return 0

        if depth == 0:
            return self.evaluate(env, player)

        valid_actions = env.valid_actions()
        if not valid_actions:
            return 0

        center = env.cols // 2
        valid_actions = sorted(valid_actions, key=lambda x: abs(x - center))

        if is_max:
            max_eval = float('-inf')
            for action in valid_actions:
                env_copy = self.clone_env(env)
                env_copy.step(action)
                score = self.minmax(env_copy, depth - 1, alpha, beta, False, player)
                max_eval = max(max_eval, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for action in valid_actions:
                env_copy = self.clone_env(env)
                env_copy.step(action)
                score = self.minmax(env_copy, depth - 1, alpha, beta, True, player)
                min_eval = min(min_eval, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate(self, env, player):
        score = self.score_board(env.board, player, env.rows, env.cols)
        score -= self.score_board(env.board, -player, env.rows, env.cols) * 1.1

        # Center column bonus
        center = env.cols // 2
        score += np.sum(env.board[:, center] == player) * 5

        # Rotation awareness: evaluate post-rotation position
        if env.moves_until_rotation <= 2:
            rot_board = self.simulate_rotation(env.board, env.next_rotation_dir, env.rows, env.cols)
            score += self.score_board(rot_board, player, env.rows, env.cols) * 0.7
            score -= self.score_board(rot_board, -player, env.rows, env.cols) * 0.8

        return score

    def simulate_rotation(self, board, direction, rows, cols):
        k = 1 if direction == 1 else -1
        rotated = np.rot90(board.copy(), k=k)
        for c in range(cols):
            col = rotated[:, c]
            nonzero = col[col != 0]
            new_col = np.zeros(rows, dtype=np.int8)
            if len(nonzero) > 0:
                new_col[-len(nonzero):] = nonzero
            rotated[:, c] = new_col
        return rotated

    def score_board(self, board, player, rows, cols):
        score = 0
        # Horizontal
        for r in range(rows):
            for c in range(cols - 3):
                score += self.score_window(board[r, c:c+4], player)
        # Vertical
        for r in range(rows - 3):
            for c in range(cols):
                score += self.score_window(board[r:r+4, c], player)
        # Diagonals
        for r in range(rows - 3):
            for c in range(cols - 3):
                score += self.score_window([board[r+i, c+i] for i in range(4)], player)
        for r in range(3, rows):
            for c in range(cols - 3):
                score += self.score_window([board[r-i, c+i] for i in range(4)], player)
        return score

    def score_window(self, window, player):
        window = np.array(window)
        p_count = np.sum(window == player)
        empty = np.sum(window == 0)
        opp = np.sum(window == -player)

        if opp > 0:
            return 0
        if p_count == 4:
            return 1000
        if p_count == 3 and empty == 1:
            return 50
        if p_count == 2 and empty == 2:
            return 10
        return p_count