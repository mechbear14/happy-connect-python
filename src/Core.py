import numpy
from typing import List, Tuple, Dict


class Board:
    def __init__(self, rows: int, columns: int, block_kind_count: int):
        self.dimension = [rows, columns]
        self.block_count = rows * columns
        self.block_kind_count = block_kind_count
        self.board = numpy.floor(numpy.random.rand(rows, columns) * block_kind_count).astype(numpy.int8)
        count_dict = self.count_blocks()
        self.count = [count_dict[key] for key in count_dict.keys()]

    def get_board(self) -> numpy.ndarray:
        return self.board

    def get_count(self) -> List[int]:
        return self.count

    def count_blocks(self) -> Dict:
        value, count = numpy.unique(self.board, return_counts=True)
        count_dict = dict(zip(value, count))
        return count_dict

    def update(self, to_remove: List[Tuple]):
        row_count = self.dimension[0]
        all_rows = [r for r in range(row_count)]
        for block in to_remove:
            row, col = block
            remaining_rows = all_rows.copy()
            remaining_rows.remove(row)
            new_column = numpy.ones(row_count, dtype=numpy.int8) * -1
            new_column[1:row_count] = self.board[numpy.array(remaining_rows), col]
            self.board[:, col] = new_column

        value, count = numpy.unique(self.board, return_counts=True)
        count_dict = dict(zip(value, count))
        new_block_count = count_dict[-1]
        densities = []
        for kind in range(self.block_kind_count):
            if kind in count_dict.keys():
                densities.append(count_dict[kind])
            else:
                densities.append(0)
        densities = self.block_count - numpy.array(densities)
        densities = numpy.cumsum(densities) / numpy.sum(densities)

        new_block_dice = numpy.random.rand(new_block_count)
        new_blocks = numpy.zeros(new_block_count)
        for d in densities[:-1]:
            new_blocks += numpy.heaviside(new_block_dice - d, 1)
        new_blocks = new_blocks.astype(numpy.int8)
        to_replace = numpy.argwhere(self.board < 0)
        for (space, block) in zip(to_replace, new_blocks):
            self.board[space[0], space[1]] = block

        count_dict = self.count_blocks()
        self.count = [count_dict[key] for key in count_dict.keys()]
