import numpy
from typing import List, Tuple, Dict


class Board:
    def __init__(self, rows: int, columns: int, block_kind_count: int):
        self.dimension = [rows, columns]
        self.block_count = rows * columns
        self.block_kind_count = block_kind_count
        self.board = numpy.floor(numpy.random.rand(rows, columns) * block_kind_count).astype(numpy.int8)
        self.count = []
        self.count_blocks()

    def get_board(self) -> numpy.ndarray:
        return self.board

    def get_count(self) -> List[int]:
        return self.count

    def count_blocks(self) -> None:
        value, count = numpy.unique(self.board, return_counts=True)
        count_dict = dict(zip(value, count))
        self.count = [count_dict[key] for key in count_dict.keys()]

    def update(self, to_remove: List[Tuple]):
        row_count = self.dimension[0]
        all_rows = [r for r in range(row_count)]
        for column in range(self.dimension[1]):
            rows_to_remove = [block[0] for block in to_remove if block[1] == column]
            remaining_rows = all_rows.copy()
            if len(rows_to_remove) > 0:
                for row in rows_to_remove:
                    remaining_rows.remove(row)
                new_column = numpy.ones(row_count, dtype=numpy.int8) * -1
                new_column[len(rows_to_remove):row_count] = self.board[numpy.array(remaining_rows), column]
                self.board[:, column] = new_column

        removed_count = len(to_remove)
        new_blocks = numpy.floor(numpy.random.rand(removed_count) * self.block_kind_count)
        new_blocks = new_blocks.astype(numpy.int8)
        to_replace = numpy.argwhere(self.board < 0)
        for (space, block) in zip(to_replace, new_blocks):
            self.board[space[0], space[1]] = block

        self.count_blocks()
