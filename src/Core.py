import numpy
from random import choice, randint
from typing import List, Tuple


class Board:
    def __init__(self, rows: int, columns: int, block_kind_count: int):
        self.dimension = [rows, columns]
        self.block_count = rows * columns
        self.block_kind_count = block_kind_count
        self.board = numpy.floor(numpy.random.rand(rows, columns) * block_kind_count).astype(numpy.int8)
        self.count = []
        self.count_blocks()

        if not self.is_possible_to_move():
            self.shuffle()

    def get_board(self) -> numpy.ndarray:
        return self.board

    def get_count(self) -> List[int]:
        return self.count

    def count_blocks(self) -> None:
        value, count = numpy.unique(self.board, return_counts=True)
        count_dict = dict(zip(value, count))
        self.count = [count_dict[key] for key in count_dict.keys()]

    def update(self, to_remove: List[Tuple]) -> List[Tuple]:
        diff = []
        to_remove_animation = [(block[0], block[1], -1, -1) for block in to_remove]
        diff.extend(to_remove_animation)

        row_count, column_count = self.dimension
        all_rows = [r for r in range(row_count)]
        for column in range(column_count):
            rows_to_remove = [block[0] for block in to_remove if block[1] == column]
            remaining_rows = all_rows.copy()
            shift_lengths_for_animation = numpy.zeros(row_count)
            if len(rows_to_remove) > 0:
                for row in rows_to_remove:
                    remaining_rows.remove(row)
                    shift_lengths_for_animation += numpy.heaviside(row - numpy.array(all_rows), 0)
                shift_lengths_for_animation[numpy.array(rows_to_remove)] = 0
                new_column = numpy.ones(row_count, dtype=numpy.int8) * -1
                new_column[len(rows_to_remove):row_count] = self.board[numpy.array(remaining_rows), column]
                self.board[:, column] = new_column
            to_shift_animation = [(prev_row, column, prev_row + int(shift), column)
                                  for prev_row, shift in enumerate(shift_lengths_for_animation)
                                  if shift > 0]
            to_add_animation = [(r - len(rows_to_remove), column, r, column)
                                for r, _ in enumerate(rows_to_remove)]
            to_shift_animation.extend(to_add_animation)
            diff.extend(to_shift_animation)

        removed_count = len(to_remove)
        new_blocks = numpy.floor(numpy.random.rand(removed_count) * self.block_kind_count)
        new_blocks = new_blocks.astype(numpy.int8)
        to_replace = numpy.argwhere(self.board < 0)
        for (space, block) in zip(to_replace, new_blocks):
            self.board[space[0], space[1]] = block

        self.count_blocks()

        return diff

    def is_possible_to_move(self) -> bool:
        rows, cols = self.dimension
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        component_numbers = numpy.ones(self.dimension) * -1
        current_component_number = 0
        visited = numpy.zeros([rows, cols], numpy.bool)

        def visit(row: int, col: int):
            component_numbers[row, col] = current_component_number
            visited[row, col] = True

            neighbours = [d for d in directions
                          if -1 < row + d[0] < rows and -1 < col + d[1] < cols]
            neighbours = [n for n in neighbours
                          if self.board[row, col] == self.board[row + n[0], col + n[1]]]
            for n in neighbours:
                if not visited[row + n[0], col + n[1]]:
                    visit(row + n[0], col + n[1])

        for r in range(rows):
            for c in range(cols):
                if not visited[r, c]:
                    visit(r, c)
                    current_component_number += 1

        _, count = numpy.unique(component_numbers, return_counts=True)
        return numpy.amax(count) > 2

    def shuffle(self) -> List[Tuple]:
        diff = []

        new_board = numpy.ones(self.dimension, numpy.int8) * -1
        valid_option = [kind for kind, count in enumerate(self.count) if count > 2]
        counts = self.count.copy()
        new_kind = choice(valid_option)
        new_count = numpy.min([self.dimension[0], counts[new_kind]])
        new_count = numpy.max([randint(0, new_count - 1), 3])

        rows, cols = self.dimension
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        positions = [(randint(0, rows - 1), randint(0, cols - 1))]
        for current in range(new_count):
            row, col = positions[-1]
            new_board[row, col] = new_kind
            if current < new_count - 1:
                neighbours = [d for d in directions
                              if -1 < row + d[0] < rows and -1 < col + d[1] < cols]
                neighbours = [n for n in neighbours
                              if not new_board[row + n[0], col + n[1]] == new_kind]
                if(len(neighbours)) == 0:
                    new_count = current + 1
                    break
                d = choice(neighbours)
                next_row, next_column = row + d[0], col + d[1]
                positions.append((next_row, next_column))
        original_positions = numpy.argwhere(self.board == new_kind)[0:new_count]
        original_positions = [(op[0], op[1]) for op in original_positions]

        diff.extend([(op[0], op[1], np[0], np[1])
                     for op, np in zip(original_positions, positions)])

        prev_positions = [(p[0], p[1]) for p in numpy.argwhere(self.board > -1)]
        for op in original_positions:
            prev_positions.remove(op)
        new_positions = [(p[0], p[1]) for p in numpy.argwhere(new_board < 0)]

        indices = [i for i, _ in enumerate(prev_positions)]
        indices.reverse()
        indices = indices[:-1]
        for a in indices:
            b = randint(0, a)
            prev_positions[a], prev_positions[b] = prev_positions[b], prev_positions[a]
        for old_new in zip(prev_positions, new_positions):
            src, dest = old_new
            src_row, src_col = src
            dest_row, dest_col = dest
            new_board[dest_row, dest_col] = self.board[src_row, src_col]

        shuffles = [(b[0], b[1], a[0], a[1]) for b, a in zip(prev_positions, new_positions)]
        diff.extend(shuffles)
        diff = [d for d in diff if not (d[0] == d[2] and d[1] == d[3])]

        self.board = new_board
        self.count_blocks()

        return diff
