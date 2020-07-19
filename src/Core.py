import numpy
from typing import List


class Board:
    def __init__(self, rows: int, columns: int, block_kind_count: int):
        self.dimension = [rows, columns]
        self.block_count = rows * columns
        self.block_kind_count = block_kind_count

        self.board = numpy.floor(numpy.random.rand(rows, columns) * block_kind_count).astype(numpy.int8)
        value, count = numpy.unique(self.board, return_counts=True)
        count_dict = dict(zip(value, count))
        self.count = [count_dict[key] for key in count_dict.keys()]

    def get_board(self) -> numpy.ndarray:
        return self.board

    def get_count(self) -> List[int]:
        return self.count
