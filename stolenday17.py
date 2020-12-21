from copy import deepcopy
from itertools import product

import numpy as np


def main():
    init_state = np.array([list(line) for line in open("day17.txt").readlines()]) == "#"
    print(ConwayCubes(init_state, dimensions=4).run(num_cycles=6).active_num);


class ConwayCubes:

    def __init__(self, init_state: np.ndarray, dimensions: int):
        shape = init_state.shape
        new_shape = [1] * (dimensions - len(shape)) + list(shape)
        self.init_state = np.reshape(init_state, tuple(new_shape))
        self.state = self.init_state
        self.dims = dimensions

    def run(self, num_cycles: int):
        prev_state = self.state
        for _cycle_num in range(num_cycles):
            next_state = self.get_next_state(prev_state)
            next_state = self.trim_state(next_state)
            prev_state = next_state
            print(f"{self.dims}-D cycle #{_cycle_num + 1} finished.")
            # self.print_state(next_state)

        self.state = prev_state

        return self

    @property
    def active_num(self):
        return np.sum(self.state)

    def get_next_state(self, prev_state):
        prev_state = np.pad(prev_state, pad_width=1, constant_values=False)
        next_state = deepcopy(prev_state)

        for idx in np.ndindex(prev_state.shape):
            c = 0
            for offset in product([-1, 0, 1], repeat=self.dims):
                if all(i == 0 for i in offset):
                    continue

                oidx = tuple(np.array(idx) + np.array(offset))

                if not all(0 <= oidx[i] < prev_state.shape[i] for i in range(self.dims)):
                    continue

                if prev_state[oidx]:
                    c += 1

            was_act = prev_state[idx]
            if (was_act and c == 2 or c == 3) or (not was_act and c == 3):
                next_state[idx] = True
            else:
                next_state[idx] = False

        return next_state

    def trim_state(self, next_state):
        slices = []
        for d in range(len(next_state.shape)):
            slice_start = 0
            slice_end = next_state.shape[d]
            for i in range(next_state.shape[d]):
                idx = tuple([slice(None) if _d != d else i for _d in range(len(next_state.shape))])
                if not np.any(next_state[idx]):
                    slice_start += 1
                else:
                    break
            for i in reversed(range(next_state.shape[d])):
                idx = tuple([slice(None) if _d != d else i for _d in range(len(next_state.shape))])
                if not np.any(next_state[idx]):
                    slice_end -= 1
                else:
                    break

            slices.append(slice(slice_start, slice_end))

        return next_state[tuple(slices)]

    def print_state(self, state):
        for i in range(state.shape[0]):
            print("\n".join("".join("#" if s else "." for s in line) for line in state[i]))
            print();

main();