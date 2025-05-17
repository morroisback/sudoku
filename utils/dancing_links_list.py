from __future__ import annotations
from functools import total_ordering


class Node:
    def __init__(self, row: RowNode | None = None, col: ColNode | None = None) -> None:
        self.left = None
        self.right = None
        self.up = None
        self.down = None

        self.row = row
        self.col = col

    def __repr__(self) -> str:
        return f"Node({self.row.idx}, {self.col.idx})"

    def __eq__(self, other: Node) -> bool:
        return self.row == other.row and self.col == other.col


@total_ordering
class RowNode:
    def __init__(self, idx: int | tuple, up: RowNode | None = None, down: RowNode | None = None) -> None:
        self.up = up
        self.down = down

        self.head = None
        self.tail = None
        self.length = 0
        self.idx = idx

    def __repr__(self) -> str:
        if self.length == 0:
            return f"RowNode(idx={self.idx}, length={self.length}, ())"

        result = []
        node = self.head
        while True:
            result.append((node.row.idx, node.col.idx))

            if node is self.tail:
                break
            node = node.right

        return f"RowNode(idx={self.idx}, length={self.length}, {tuple(result)})"

    def __len__(self) -> int:
        return self.length

    def __eq__(self, other: RowNode | int | tuple) -> bool:
        if isinstance(other, RowNode):
            return self.idx == other.idx
        elif isinstance(other, int):
            return self.idx == other
        elif isinstance(other, tuple):
            return self.idx == other

        raise TypeError("Invalid type for comparison")

    def __lt__(self, other: RowNode | int | tuple) -> bool:
        if isinstance(other, RowNode):
            return self.idx < other.idx
        elif isinstance(other, int):
            return self.idx < other
        elif isinstance(other, tuple):
            return self.idx < other

        raise TypeError("Invalid type for comparison")

    def __getitem__(self, col_idx: int | tuple) -> Node:
        if self.length == 0:
            raise IndexError("Row is empty")

        if col_idx < self.head.col or col_idx > self.tail.col:
            raise IndexError("Column index out of range")

        node = self.head
        while True:
            if node.col == col_idx:
                return node

            if node is self.tail:
                break
            node = node.right

        raise IndexError("Node not found")

    def __delitem__(self, col_idx: int | tuple) -> None:
        node = self[col_idx]
        node.left.right = node.right
        node.right.left = node.left

        if self.length == 1:
            self.head = None
            self.tail = None
        elif node is self.head:
            self.head = node.right
        elif node is self.tail:
            self.tail = node.left

        self.length -= 1

    def __setitem__(self, col_idx: int | tuple, new_node: Node) -> None:
        if not isinstance(new_node, Node):
            raise TypeError("Invalid type for new node")

        if new_node.col != col_idx:
            raise ValueError("Node column index mismatch")

        if new_node.row != self.idx:
            raise ValueError("Node row index mismatch")

        if self.length == 0:
            new_node.left = new_node
            new_node.right = new_node

            self.head = new_node
            self.tail = new_node
            self.length += 1
            return

        if col_idx < self.head.col or col_idx > self.tail.col:
            new_node.left = self.tail
            new_node.right = self.head
            self.head.left = new_node
            self.tail.right = new_node

            if col_idx < self.head.col:
                self.head = new_node
            elif col_idx > self.tail.col:
                self.tail = new_node

            self.length += 1
            return

        node = self.head
        while True:
            if node.col == col_idx:
                raise ValueError("Node already exists")

            if node is self.tail:
                break

            if node.col < col_idx < node.right.col:
                new_node.left = node
                new_node.right = node.right
                node.right.left = new_node
                node.right = new_node

                self.length += 1
                return

            new_node = new_node.right

    def del_row(self) -> None:
        self.up.down = self.down
        self.down.up = self.up

        if self.length == 0:
            return None

        node = self.head
        while True:
            node.up.down = node.down
            node.down.up = node.up

            if node.col.length == 1:
                node.col.head = None
                node.col.tail = None
            elif node is node.col.head:
                node.col.head = node.down
            elif node is node.col.tail:
                node.col.tail = node.up

            node.col.length -= 1
            if node is self.tail:
                break
            node = node.right

    def restore_row(self) -> None:
        self.up.down = self
        self.down.up = self

        if self.length == 0:
            return None

        node = self.head
        while True:
            node.up.down = node
            node.down.up = node

            if node.col.length == 0:
                node.col.head = node
                node.col.tail = node
            if self < node.col.head.row:
                node.col.head = node
            elif self > node.col.tail.row:
                node.col.tail = node

            node.col.length += 1
            if node is self.tail:
                break
            node = node.right


@total_ordering
class ColNode:
    def __init__(self, idx: int | tuple, left: ColNode | None = None, right: ColNode | None = None) -> None:
        self.left = left
        self.right = right

        self.head = None
        self.tail = None
        self.length = 0
        self.idx = idx

    def __repr__(self) -> str:
        if self.length == 0:
            return f"ColNode(idx={self.idx}, length={self.length}, ())"

        result = []
        node = self.head
        while True:
            result.append((node.row.idx, node.col.idx))

            if node is self.tail:
                break
            node = node.down

        return f"ColNode(idx={self.idx}, length={self.length}, {tuple(result)})"

    def __len__(self) -> int:
        return self.length

    def __eq__(self, other: ColNode | int | tuple) -> bool:
        if isinstance(other, ColNode):
            return self.idx == other.idx
        elif isinstance(other, int):
            return self.idx == other
        elif isinstance(other, tuple):
            return self.idx == other

        raise TypeError("Invalid type for comparison")

    def __lt__(self, other: ColNode | int | tuple) -> bool:
        if isinstance(other, ColNode):
            return self.idx < other.idx
        elif isinstance(other, int):
            return self.idx < other
        elif isinstance(other, tuple):
            return self.idx < other

        raise TypeError("Invalid type for comparison")

    def __getitem__(self, row_idx: int | tuple) -> Node:
        if self.length == 0:
            raise IndexError("Column is empty")

        if row_idx < self.head.row or row_idx > self.tail.row:
            raise IndexError("Row index out of range")

        node = self.head
        while True:
            if node.row == row_idx:
                return node

            if node is self.tail:
                break
            node = node.down

        raise IndexError("Node not found")

    def __delitem__(self, row_idx: int | tuple) -> None:
        node = self[row_idx]
        node.up.down = node.down
        node.down.up = node.up

        if self.length == 1:
            self.head = None
            self.tail = None
        elif node is self.head:
            self.head = node.down
        elif node is self.tail:
            self.tail = node.up

        self.length -= 1

    def __setitem__(self, row_idx: int | tuple, new_node: Node) -> None:
        if not isinstance(new_node, Node):
            raise TypeError("Invalid type for new node")

        if new_node.row != row_idx:
            raise ValueError("Node row index mismatch")

        if new_node.col != self.idx:
            raise ValueError("Node column index mismatch")

        if self.length == 0:
            new_node.up = new_node
            new_node.down = new_node

            self.head = new_node
            self.tail = new_node
            self.length += 1
            return

        if row_idx < self.head.row or row_idx > self.tail.row:
            new_node.up = self.tail
            new_node.down = self.head
            self.head.up = new_node
            self.tail.down = new_node

            if row_idx < self.head.row:
                self.head = new_node
            elif row_idx > self.tail.row:
                self.tail = new_node

            self.length += 1
            return

        node = self.head
        while True:
            if node.row == row_idx:
                raise ValueError("Node already exists")

            if node is self.tail:
                break

            if node.row < row_idx < node.down.row:
                new_node.up = node
                new_node.down = node.down
                node.down.up = new_node
                node.down = new_node

                self.length += 1
                return

            node = node.down

    def del_col(self) -> None:
        self.left.right = self.right
        self.right.left = self.left

        if self.length == 0:
            return None

        node = self.head
        while True:
            node.left.right = node.right
            node.right.left = node.left

            if node.row.length == 1:
                node.row.head = None
                node.row.tail = None
            elif node is node.row.head:
                node.row.head = node.right
            elif node is node.row.tail:
                node.row.tail = node.left

            node.row.length -= 1
            if node is self.tail:
                break
            node = node.down

    def restore_col(self) -> None:
        self.left.right = self
        self.right.left = self

        if self.length == 0:
            return None

        node = self.head
        while True:
            node.left.right = node
            node.right.left = node

            if node.row.length == 0:
                node.row.head = node
                node.row.tail = node
            elif self < node.row.head.col:
                node.row.head = node
            elif self > node.row.tail.col:
                node.row.tail = node

            node.row.length += 1
            if node is self.tail:
                break
            node = node.down


class DancingLinksList:
    def __init__(self, str_size: int = 3) -> None:
        self.row_head = None
        self.row_tail = None
        self.row_length = 0

        self.col_head = None
        self.col_tail = None
        self.col_length = 0

        self.stack = []
        self.str_size = str_size

    def __repr__(self) -> str:
        repr_str = f"DancingLinksList(row_length={self.row_length}, col_length={self.col_length})\n"

        row_node = self.row_head
        while True:
            repr_str += f"{row_node}\n"
            if row_node is self.row_tail:
                break
            row_node = row_node.down

        return repr_str

    def __str__(self) -> str:
        row_sep = "-" * self.str_size
        row_fill = " " * self.str_size

        header_str_0 = f"|{row_sep * 2}|"
        header_str_1 = f"|{row_fill * 2}|"
        header_str_2 = f"|{row_fill * 2}|"
        header_str_3 = f"|{row_sep * 2}|"

        if self.col_length != 0:
            col_node = self.col_head
            while True:
                header_str_0 += f"{row_sep}|"
                header_str_1 += f"{str(col_node.idx):>{self.str_size}}|"
                header_str_2 += f"{col_node.length:>{self.str_size}}|"
                header_str_3 += f"{row_sep}|"

                if col_node is self.col_tail:
                    break
                col_node = col_node.right

        result_str = f"{header_str_0}\n" + f"{header_str_1}\n" + f"{header_str_2}\n" + f"{header_str_3}\n"
        if self.row_length == 0:
            return result_str

        row_str = ""
        tail_str = f"|{row_sep * 2}|" + f"{row_sep}|" * (self.col_length)
        row_node = self.row_head
        while True:
            row_str += f"|{str(row_node.idx):>{self.str_size}}{row_node.length:>{self.str_size}}|"
            if row_node.length == 0:
                row_str += f"{0:>{self.str_size}}|" * self.col_length + "\n"
                if row_node is self.row_tail:
                    break
                row_node = row_node.down
                continue

            col_node = self.col_head
            node = row_node.head
            while True:
                if node.col is col_node:
                    row_str += f"{1:>{self.str_size}}|"
                    node = node.right
                else:
                    row_str += f"{0:>{self.str_size}}|"

                if col_node is self.col_tail:
                    row_str += "\n"
                    break
                col_node = col_node.right

            if row_node is self.row_tail:
                break
            row_node = row_node.down

        result_str += f"{row_str}" + f"{tail_str}\n"
        return result_str

    def __getitem__(self, idxs: tuple) -> Node:
        if isinstance(idxs, tuple) and len(idxs) == 2:
            row_idx, col_idx = idxs
            return self.get_node(row_idx, col_idx)
        else:
            raise TypeError("Invalid type for indexes")

    def __delitem__(self, idxs: tuple) -> None:
        if isinstance(idxs, tuple) and len(idxs) == 2:
            row_idx, col_idx = idxs
            self.del_node(row_idx, col_idx)
        else:
            raise TypeError("Invalid type for indexes")

    def __setitem__(self, idxs: tuple, is_enabled: bool) -> None:
        if isinstance(idxs, tuple) and len(idxs) == 2 and isinstance(is_enabled, bool):
            row_idx, col_idx = idxs

            if is_enabled:
                self.set_node(row_idx, col_idx)
            else:
                self.del_node(row_idx, col_idx)
        else:
            raise TypeError("Invalid type for indexes")

    @staticmethod
    def get_rows_cross_col(col_node: ColNode) -> list[RowNode]:
        rows = []
        if col_node.length == 0:
            return rows

        node = col_node.head
        while True:
            rows.append(node.row)
            if node is col_node.tail:
                break
            node = node.down

        return rows

    @staticmethod
    def get_cols_cross_row(row_node: RowNode) -> list[ColNode]:
        cols = []
        if row_node.length == 0:
            return cols

        node = row_node.head
        while True:
            cols.append(node.col)
            if node is row_node.tail:
                break
            node = node.right

        return cols

    def get_row(self, idx: int | tuple) -> RowNode:
        if self.row_length == 0:
            raise IndexError("Row list is empty")

        if idx < self.row_head or idx > self.row_tail:
            raise IndexError("Row index out of range")

        row_node = self.row_head
        while True:
            if row_node == idx:
                return row_node

            if row_node is self.row_tail:
                break
            row_node = row_node.down

        raise IndexError("Row not found")

    def del_row(self, idx: int | tuple) -> RowNode:
        row_node = self.get_row(idx)
        row_node.del_row()

        if self.row_length == 1:
            self.row_head = None
            self.row_tail = None
        elif row_node is self.row_head:
            self.row_head = row_node.down
        elif row_node is self.row_tail:
            self.row_tail = row_node.up

        self.row_length -= 1
        return row_node

    def set_row(self, idx: int | tuple) -> None:
        if self.row_length == 0:
            new_row_node = RowNode(idx)
            new_row_node.up = new_row_node
            new_row_node.down = new_row_node

            self.row_head = new_row_node
            self.row_tail = new_row_node
            self.row_length += 1
            return

        if idx < self.row_head or idx > self.row_tail:
            new_row_node = RowNode(idx, self.row_tail, self.row_head)
            self.row_head.up = new_row_node
            self.row_tail.down = new_row_node

            if idx < self.row_head:
                self.row_head = new_row_node
            elif idx > self.row_tail:
                self.row_tail = new_row_node

            self.row_length += 1
            return

        row_node = self.row_head
        while True:
            if row_node == idx:
                raise ValueError("Node already exists")

            if row_node is self.row_tail:
                break

            if row_node < idx < row_node.down:
                new_row_node = RowNode(idx, row_node, row_node.down)
                row_node.down.up = new_row_node
                row_node.down = new_row_node

                self.row_length += 1
                return

            row_node = row_node.down

    def restore_row(self, row_node: RowNode) -> None:
        row_node.restore_row()

        if self.row_length == 0:
            self.row_head = row_node
            self.row_tail = row_node
        elif row_node < self.row_head:
            self.row_head = row_node
        elif row_node > self.row_tail:
            self.row_tail = row_node

        self.row_length += 1

    def get_col(self, idx: int | tuple) -> ColNode:
        if self.col_length == 0:
            raise IndexError("Column list is empty")

        if idx < self.col_head or idx > self.col_tail:
            raise IndexError("Column index out of range")

        col_node = self.col_head
        while True:
            if col_node == idx:
                return col_node

            if col_node is self.col_tail:
                break
            col_node = col_node.right

        raise IndexError("Column not found")

    def del_col(self, idx: int | tuple) -> ColNode:
        col_node = self.get_col(idx)
        col_node.del_col()

        if self.col_length == 1:
            self.col_head = None
            self.col_tail = None
        elif col_node is self.col_head:
            self.col_head = col_node.right
        elif col_node is self.col_tail:
            self.col_tail = col_node.left

        self.col_length -= 1
        return col_node

    def set_col(self, idx: int | tuple) -> None:
        if self.col_length == 0:
            new_col_node = ColNode(idx)
            new_col_node.left = new_col_node
            new_col_node.right = new_col_node

            self.col_head = new_col_node
            self.col_tail = new_col_node
            self.col_length += 1
            return

        if idx < self.col_head or idx > self.col_tail:
            new_col_node = ColNode(idx, self.col_tail, self.col_head)
            self.col_head.left = new_col_node
            self.col_tail.right = new_col_node

            if idx < self.col_head:
                self.col_head = new_col_node
            elif idx > self.col_tail:
                self.col_tail = new_col_node

            self.col_length += 1
            return

        col_node = self.col_head
        while True:
            if col_node == idx:
                raise ValueError("Node already exists")

            if col_node is self.col_tail:
                break

            if col_node < idx < col_node.right:
                new_col_node = ColNode(idx, col_node, col_node.right)
                col_node.right.left = new_col_node
                col_node.right = new_col_node

                self.col_length += 1
                return

            col_node = col_node.right

    def restore_col(self, col_node: ColNode) -> None:
        col_node.restore_col()

        if self.col_length == 0:
            self.col_head = col_node
            self.col_tail = col_node
        elif col_node < self.col_head:
            self.col_head = col_node
        elif col_node > self.col_tail:
            self.col_tail = col_node

        self.col_length += 1

    def get_node(self, row_idx: int | tuple, col_idx: int | tuple) -> Node:
        row_node = self.get_row(row_idx)
        col_node = self.get_col(col_idx)

        node = row_node[col_idx]
        if node is col_node[row_idx]:
            return node

        raise IndexError("Node not found")

    def del_node(self, row_idx: int | tuple, col_idx: int | tuple) -> None:
        row_node = self.get_row(row_idx)
        col_node = self.get_col(col_idx)

        node = row_node[col_idx]
        if node is col_node[row_idx]:
            del row_node[col_idx]
            del col_node[row_idx]
            return

        raise IndexError("Node not found")

    def set_node(self, row_idx: int | tuple, col_idx: int | tuple) -> None:
        row_node = self.get_row(row_idx)
        col_node = self.get_col(col_idx)

        node = Node(row_node, col_node)
        row_node[col_idx] = node
        col_node[row_idx] = node

    def get_min_row_length(self) -> RowNode:
        if self.row_length == 0:
            raise IndexError("Row list is empty")

        row_node = self.row_head
        min_row = row_node
        while True:
            if row_node.length < min_row.length:
                min_row = row_node

            if row_node is self.row_tail:
                break
            row_node = row_node.down

        return min_row

    def get_min_col_length(self) -> ColNode:
        if self.col_length == 0:
            raise IndexError("Column list is empty")

        col_node = self.col_head
        min_column = col_node
        while True:
            if col_node.length < min_column.length:
                min_column = col_node

            if col_node is self.col_tail:
                break
            col_node = col_node.right

        return min_column

    def get_sorted_rows(self) -> list[RowNode]:
        rows = []
        if self.row_length == 0:
            return rows

        row = self.row_head
        while True:
            rows.append(row)
            if row == self.row_tail:
                break
            row = row.down
        rows.sort(key=lambda x: x.length)
        return rows

    def get_sorted_cols(self) -> list[ColNode]:
        cols = []
        if self.col_length == 0:
            return cols

        col = self.col_head
        while True:
            cols.append(col)
            if col == self.col_tail:
                break
            col = col.right
        cols.sort(key=lambda x: x.length)
        return cols

    def set_list_matrix(self, matrix: list[list[int]]) -> None:
        if (rows_length := len(matrix)) == 0:
            raise ValueError("Matrix is empty")

        if (cols_length := len(matrix[0])) == 0:
            raise ValueError("Matrix is empty")

        for i in range(rows_length):
            if len(matrix[i]) != cols_length:
                raise ValueError("Matrix is not rectangular")

        for i in range(rows_length):
            self.set_row(i)

        for j in range(cols_length):
            self.set_col(j)

        for i in range(rows_length):
            for j in range(cols_length):
                if matrix[i][j]:
                    self.set_node(i, j)

    def set_dict_matrix(self, matrix: dict[tuple, dict[tuple, int]]) -> None:
        if len(matrix) == 0:
            raise ValueError("Matrix is empty")

        cols = matrix[list(matrix.keys())[0]]
        if len(cols) == 0:
            raise ValueError("Matrix is empty")

        for row in matrix:
            if len(matrix[row]) != len(cols):
                raise ValueError("Matrix is not rectangular")

        for row in matrix:
            self.set_row(row)

        for col in cols:
            self.set_col(col)

        for row in matrix:
            for col in cols:
                if matrix[row][col]:
                    self.set_node(row, col)

    def push_stack(self, subset: RowNode) -> None:
        self.stack.append(subset)

    def refresh_stack(self) -> None:
        self.stack = []

    def get_stack(self) -> list[RowNode]:
        return self.stack

    def cover(self, row: RowNode) -> tuple[list[ColNode], list[RowNode]]:
        del_cols = []
        del_rows = []

        node = row.head
        while row.length > 0:
            result = self.del_col(node.col.idx)
            del_cols.append(result)
            node = node.right

        for del_col in del_cols:
            node = del_col.head
            while True:
                if node.row not in del_rows:
                    result = self.del_row(node.row.idx)
                    del_rows.append(result)

                if node is del_col.tail:
                    break
                node = node.down

        return del_cols, del_rows

    def uncover(self, del_cols: list[ColNode], del_rows: list[RowNode]) -> None:
        for del_row in del_rows[::-1]:
            self.restore_row(del_row)

        for del_col in del_cols[::-1]:
            self.restore_col(del_col)

    def algorithm_x(self) -> list | None:
        # if (stack_length := len(self.stack)) > 600:
        #     print(stack_length)

        if self.col_length == 0:
            return self.stack

        if self.row_length == 0:
            return None

        column_list = self.get_sorted_cols()
        # column_list = [self.get_min_col_length()]
        for column in column_list:
            if not (rows := self.get_rows_cross_col(column)):
                return None

            for row in rows:
                self.stack.append(row)
                del_cols, del_rows = self.cover(row)

                if result := self.algorithm_x():
                    return result

                self.uncover(del_cols, del_rows)
                if self.stack:
                    self.stack.pop()


def test_1() -> None:
    row_node_1 = RowNode(1)
    row_node_2 = RowNode(2, row_node_1, row_node_1)
    row_node_3 = RowNode(3, row_node_2, row_node_1)

    row_node_1.down = row_node_2
    row_node_1.up = row_node_3

    row_node_2.down = row_node_3

    col_node_1 = ColNode(1)
    col_node_2 = ColNode(2, col_node_1, col_node_1)
    col_node_3 = ColNode(3, col_node_2, col_node_1)

    col_node_1.right = col_node_2
    col_node_1.left = col_node_3

    col_node_2.right = col_node_3

    print("=" * 20)
    print(row_node_1)
    print(row_node_2)
    print(row_node_3)
    print(col_node_1)
    print(col_node_2)
    print(col_node_3)

    node_1_2 = Node(row_node_1, col_node_2)
    node_2_2 = Node(row_node_2, col_node_2)
    node_3_1 = Node(row_node_3, col_node_1)
    node_3_2 = Node(row_node_3, col_node_2)
    node_3_3 = Node(row_node_3, col_node_3)

    row_node_1[2] = node_1_2
    col_node_2[1] = node_1_2

    row_node_2[2] = node_2_2
    col_node_2[2] = node_2_2

    row_node_3[1] = node_3_1
    col_node_1[3] = node_3_1

    row_node_3[2] = node_3_2
    col_node_2[3] = node_3_2

    row_node_3[3] = node_3_3
    col_node_3[3] = node_3_3

    print("=" * 20)
    print(row_node_1)
    print(row_node_2)
    print(row_node_3)
    print(col_node_1)
    print(col_node_2)
    print(col_node_3)

    row_node_3.del_row()

    print("=" * 20)
    print(row_node_1)
    print(row_node_2)
    print(row_node_3)
    print(col_node_1)
    print(col_node_2)
    print(col_node_3)

    row_node_3.restore_row()

    print("=" * 20)
    print(row_node_1)
    print(row_node_2)
    print(row_node_3)
    print(col_node_1)
    print(col_node_2)
    print(col_node_3)

    col_node_2.del_col()

    print("=" * 20)
    print(row_node_1)
    print(row_node_2)
    print(row_node_3)
    print(col_node_1)
    print(col_node_2)
    print(col_node_3)

    col_node_2.restore_col()

    print("=" * 20)
    print(row_node_1)
    print(row_node_2)
    print(row_node_3)
    print(col_node_1)
    print(col_node_2)
    print(col_node_3)


def test_2() -> None:
    dancing_links_list = DancingLinksList()
    dancing_links_list.set_row(1)
    dancing_links_list.set_row(4)
    dancing_links_list.set_row(2)
    dancing_links_list.set_row(6)
    dancing_links_list.set_row(3)
    dancing_links_list.set_row(5)

    dancing_links_list.set_col(1)
    dancing_links_list.set_col(5)
    dancing_links_list.set_col(3)
    dancing_links_list.set_col(7)
    dancing_links_list.set_col(2)
    dancing_links_list.set_col(6)
    dancing_links_list.set_col(4)

    dancing_links_list.set_node(2, 4)
    dancing_links_list.set_node(4, 4)
    dancing_links_list.set_node(6, 4)
    dancing_links_list.set_node(2, 1)
    dancing_links_list.set_node(4, 1)
    dancing_links_list.set_node(1, 3)
    dancing_links_list.set_node(3, 3)
    dancing_links_list.set_node(1, 5)
    dancing_links_list.set_node(6, 5)
    dancing_links_list.set_node(3, 2)
    dancing_links_list.set_node(5, 2)
    dancing_links_list.set_node(1, 6)
    dancing_links_list.set_node(3, 6)
    dancing_links_list.set_node(2, 7)
    dancing_links_list.set_node(5, 7)
    dancing_links_list.set_node(6, 7)
    dancing_links_list.set_node(5, 6)

    print(repr(dancing_links_list))
    print(str(dancing_links_list))

    dancing_links_list = DancingLinksList()
    dancing_links_list.set_row(1)
    dancing_links_list.set_row(2)
    dancing_links_list.set_row(3)
    dancing_links_list.set_row(4)
    dancing_links_list.set_row(5)

    dancing_links_list.set_col(1)
    dancing_links_list.set_col(2)
    dancing_links_list.set_col(3)
    dancing_links_list.set_col(4)
    dancing_links_list.set_col(5)

    dancing_links_list.set_node(1, 1)
    dancing_links_list.set_node(1, 2)
    dancing_links_list.set_node(2, 2)
    dancing_links_list.set_node(2, 3)
    dancing_links_list.set_node(3, 1)
    dancing_links_list.set_node(3, 5)
    dancing_links_list.set_node(4, 1)
    dancing_links_list.set_node(4, 4)
    dancing_links_list.set_node(5, 5)

    print(repr(dancing_links_list))
    print(str(dancing_links_list))

    dancing_links_list = DancingLinksList()
    dancing_links_list.set_row(1)
    dancing_links_list.set_row(2)
    dancing_links_list.set_row(3)
    dancing_links_list.set_row(4)
    dancing_links_list.set_row(5)
    dancing_links_list.set_row(6)
    dancing_links_list.set_row(7)

    dancing_links_list.set_col(1)
    dancing_links_list.set_col(2)
    dancing_links_list.set_col(3)
    dancing_links_list.set_col(4)
    dancing_links_list.set_col(5)
    dancing_links_list.set_col(6)
    dancing_links_list.set_col(7)

    dancing_links_list.set_node(1, 1)
    dancing_links_list.set_node(1, 4)
    dancing_links_list.set_node(1, 7)
    dancing_links_list.set_node(2, 1)
    dancing_links_list.set_node(2, 4)
    dancing_links_list.set_node(3, 4)
    dancing_links_list.set_node(3, 5)
    dancing_links_list.set_node(3, 7)
    dancing_links_list.set_node(4, 3)
    dancing_links_list.set_node(4, 5)
    dancing_links_list.set_node(4, 6)
    dancing_links_list.set_node(5, 2)
    dancing_links_list.set_node(5, 3)
    dancing_links_list.set_node(5, 6)
    dancing_links_list.set_node(5, 7)
    dancing_links_list.set_node(6, 2)
    dancing_links_list.set_node(6, 7)
    dancing_links_list.set_node(7, 1)
    dancing_links_list.set_node(7, 4)

    print(repr(dancing_links_list))
    print(str(dancing_links_list))

    row = dancing_links_list.del_row(4)

    print(repr(dancing_links_list))
    print(str(dancing_links_list))

    dancing_links_list.restore_row(row)

    print(repr(dancing_links_list))
    print(str(dancing_links_list))


def test_3() -> None:
    dancing_links_list = DancingLinksList()
    list_matrix = [
        [0, 0, 1, 0, 1, 1, 0],
        [1, 0, 0, 1, 0, 0, 1],
        [0, 1, 1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 1, 0, 1],
    ]
    dancing_links_list.set_list_matrix(list_matrix)

    print(dancing_links_list)

    deletes = dancing_links_list.cover(dancing_links_list.get_row(2))

    print(dancing_links_list)

    dancing_links_list.uncover(*deletes)

    print(dancing_links_list)

    dancing_links_list = DancingLinksList(len(str((0, 0, 0))) + 1)
    dict_matrix = {
        (2, 0, 0): {(0, 0, 0): 0, (0, 0, 1): 0, (0, 1, 0): 1, (0, 1, 1): 0, (1, 0, 0): 1, (1, 0, 1): 1, (1, 1, 0): 0},
        (2, 0, 1): {(0, 0, 0): 1, (0, 0, 1): 0, (0, 1, 0): 0, (0, 1, 1): 1, (1, 0, 0): 0, (1, 0, 1): 0, (1, 1, 0): 1},
        (2, 1, 0): {(0, 0, 0): 0, (0, 0, 1): 1, (0, 1, 0): 1, (0, 1, 1): 0, (1, 0, 0): 0, (1, 0, 1): 1, (1, 1, 0): 0},
        (2, 1, 1): {(0, 0, 0): 1, (0, 0, 1): 0, (0, 1, 0): 0, (0, 1, 1): 1, (1, 0, 0): 0, (1, 0, 1): 0, (1, 1, 0): 0},
        (3, 0, 0): {(0, 0, 0): 0, (0, 0, 1): 1, (0, 1, 0): 0, (0, 1, 1): 0, (1, 0, 0): 0, (1, 0, 1): 0, (1, 1, 0): 1},
        (3, 0, 1): {(0, 0, 0): 0, (0, 0, 1): 0, (0, 1, 0): 0, (0, 1, 1): 1, (1, 0, 0): 1, (1, 0, 1): 0, (1, 1, 0): 1},
    }
    dancing_links_list.set_dict_matrix(dict_matrix)

    print(dancing_links_list)

    if cover_sets := dancing_links_list.algorithm_x():
        for cover_set in cover_sets:
            print(cover_set)
    else:
        print("No solve", dancing_links_list.get_stack())


if __name__ == "__main__":
    # test_1()
    # test_2()
    test_3()
