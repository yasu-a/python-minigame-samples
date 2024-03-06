# ミニマックス法を使った〇×ゲーム

import functools
import time

import numpy as np
import pandas as pd
from tqdm import tqdm


class GameState:
    def __init__(self, field_size, state, latest_replace=None):
        self.__field_size = field_size
        self.__state = state
        self.__latest_replace = latest_replace

    @classmethod
    def create_instance(cls, field_size=3):
        state = np.zeros(shape=(field_size, field_size), dtype=np.uint8)  # [row, column]
        return cls(field_size, state)

    def clone(self):
        return type(self)(self.__field_size, np.copy(self.__state), self.__latest_replace)

    @functools.cached_property
    def available(self):
        idx_row, idx_col = np.where(self.__state == 0)
        return list(zip(idx_row, idx_col))  # [(i, j), (i, j), ...]

    def replace(self, i, j, stone):
        assert (i, j) in self.available, f'{(i, j)} is unavailable'
        assert stone in {1, 2}, f'invalid stone {stone}'
        next_state = self.clone()
        next_state.__state[i, j] = stone
        next_state.__latest_replace = (i, j)
        return next_state

    def as_dataframe(self, show_latest_replace=False):
        df = pd.DataFrame(
            np.where(self.__state == 0, ' ', np.where(self.__state == 1, 'o', 'x')),
            columns=[chr(ord('a') + i) for i in range(self.__field_size)],
            index=range(self.__field_size)
        )
        if show_latest_replace and self.__latest_replace is not None:
            i, j = self.__latest_replace
            df.iloc[i, j] = f'[{df.iloc[i, j]}]'
        return df

    @functools.cache
    def _win(self, stone):
        assert stone in {1, 2}, f'invalid stone {stone}'
        # noinspection PyTypeChecker
        truth_table: np.ndarray = self.__state != stone
        if np.any(truth_table.sum(axis=0) == 0):
            return True
        if np.any(truth_table.sum(axis=1) == 0):
            return True
        if np.diag(truth_table).sum() == 0:
            return True
        if np.diag(truth_table[:, ::-1]).sum() == 0:
            return True
        return False

    @functools.cache
    def result(self, stone):
        if self._win(stone):
            return 'self'
        elif self._win(self._next_stone(stone)):
            return 'opp'
        elif self.full:
            return 'draw'
        else:
            return None

    @functools.cached_property
    def full(self):
        return not bool(self.available)

    def prompt(self):
        while True:
            try:
                col, row = input('column row ?> ')
                i = int(row)
                j = ord(col) - ord('a')
            except ValueError:
                pass
            else:
                if (i, j) in self.available:
                    break
            print(f'invalid input')
        return i, j

    @classmethod
    def _next_stone(cls, stone):
        assert stone in {1, 2}
        return [None, 2, 1][stone]

    _WIN_SCORE = 99

    def _evaluate(self, src_stone, depth):
        result = self.result(src_stone)
        if result == 'self':
            return self._WIN_SCORE * +1 - depth
        elif result == 'opp':
            return self._WIN_SCORE * -1 + depth
        else:
            return depth

    def _take_random_available(self, n):
        rs = np.random.choice(
            np.arange(len(self.available)),
            size=min(len(self.available), n),
            replace=False
        )
        return [self.available[r] for r in rs]

    def _get_best(self, src_stone, current_stone, depth=None, max_depth=5) \
            -> tuple[tuple[int, int] | None, int]:
        if depth is None:
            depth = 0
        if depth >= max_depth:
            return None, self._evaluate(src_stone, depth)

        if self.result(src_stone) is not None:
            return None, self._evaluate(src_stone, depth)
        else:
            moves, scores = [], []
            if self.__field_size == 3 or depth == 0:
                it = self.available
            else:
                it = self._take_random_available(n=7)
            if depth == 0:
                it = tqdm(it)
            for i, j in it:
                new_state = self.replace(i, j, current_stone)
                _, score = new_state._get_best(
                    src_stone,
                    self._next_stone(current_stone),
                    depth=depth + 1
                )
                moves.append((i, j))
                scores.append(score)

            if src_stone == current_stone:
                i = np.argmax(scores)
            else:
                i = np.argmin(scores)
            return moves[i], scores[i]

    def estimate_next(self, stone):
        # r = np.random.randint(0, len(self.available) - 1)
        # return self.available[r]
        move, _ = self._get_best(stone, stone)
        return move


def main():
    field_size = int(input('Field size ?> '))
    state = GameState.create_instance(field_size=field_size)
    print(state.as_dataframe())

    you, com = 1, 2
    order = [('you', you), ('com', com)]

    if input('Reverse order[y/n] ?> ') == 'y':
        order = order[::-1]

    while True:
        for player, stone in order:
            print(f' --- {player.upper():4} --------------')

            result = state.result(you)
            if result is not None:
                print(dict(self='WIN!', opp='LOSE！', draw='DRAW')[result])
                return

            if stone == you:
                i, j = state.prompt()
            elif stone == com:
                i, j = state.estimate_next(stone)
                print(f'com > {state.as_dataframe().columns[j]}{i}')
                time.sleep(1)
            else:
                assert False
            new_state = state.replace(i, j, stone)

            it = enumerate(
                zip(
                    str(state.as_dataframe()).splitlines(),
                    str(new_state.as_dataframe(show_latest_replace=True)).splitlines()
                )
            )
            for i, (l1, l2) in it:
                if i == int(field_size / 2 + 0.5):
                    print(l1, ' -> ', l2)
                else:
                    print(l1, '    ', l2)

            state = new_state


if __name__ == '__main__':
    main()
