from __future__ import annotations
from functools import total_ordering


@total_ordering
class RingLinkedNode:
    def __init__(self, idx: int = 0, value: bool = False) -> None:
        if not isinstance(value, bool):
            raise TypeError("Value must be a boolean")

        self.idx = idx
        self.value = value
        self.previous = None
        self.next = None

    def __repr__(self) -> str:
        return f"RingLinkedNode(idx={self.idx}, value={self.value})"

    def __bool__(self) -> bool:
        return self.value

    def __eq__(self, other: RingLinkedList | int) -> bool:
        if isinstance(other, RingLinkedNode):
            return self.idx == other.idx
        elif isinstance(other, int):
            return self.idx == other

        raise TypeError("Invalid type for comparison")

    def __lt__(self, other: RingLinkedList | int) -> bool:
        if isinstance(other, RingLinkedNode):
            return self.idx < other.idx
        elif isinstance(other, int):
            return self.idx < other

        raise TypeError("Invalid type for comparison")


class RingLinkedList:
    def __init__(self) -> None:
        self.head = None
        self.tail = None
        self.length = 0

    def __len__(self) -> int:
        return self.length

    def __repr__(self) -> str:
        if self.length == 0:
            return f"RingLinkedList(len={self.length}, ())"

        result = []
        node = self.head
        while True:
            result.append(node.idx)

            if node is self.tail:
                break
            node = node.next

        return f"RingLinkedList(len={self.length}, {tuple(result)})"

    def __getitem__(self, idx: int = 0) -> RingLinkedList:
        if self.length == 0:
            raise IndexError("List is empty")

        if idx < self.head or idx > self.tail:
            raise IndexError("Index out of range")

        node = self.head
        while True:
            if node == idx:
                return node

            if node is self.tail:
                break
            node = node.next

        raise IndexError("Index not found")

    def __delitem__(self, idx: int = 0) -> None:
        node = self[idx]
        node.previous.next = node.next
        node.next.previous = node.previous

        if self.length == 1:
            self.head = None
            self.tail = None
        elif node is self.head:
            self.head = node.next
        elif node is self.tail:
            self.tail = node.previous

        self.length -= 1

    def __setitem__(self, idx: int, value: bool) -> None:
        new_node = RingLinkedNode(idx, value)
        if self.length == 0:
            new_node.next = new_node
            new_node.previous = new_node

            self.head = new_node
            self.tail = new_node
            self.length += 1
            return

        if idx < self.head or idx > self.tail:
            new_node.previous = self.tail
            new_node.next = self.head
            self.head.previous = new_node
            self.tail.next = new_node

            if idx < self.head:
                self.head = new_node
            elif idx > self.tail:
                self.tail = new_node

            self.length += 1
            return

        node = self.head
        while True:
            if node == idx:
                node.value = value
                return

            if node is self.tail:
                break

            if node < new_node < node.next:
                new_node.previous = node
                new_node.next = node.next
                node.next.previous = new_node
                node.next = new_node

                self.length += 1
                return

            node = node.next


def test() -> None:
    row_0 = RingLinkedList()
    row_0[3] = True
    row_0[4] = True
    print(row_0)

    row_1 = RingLinkedList()
    row_1[1] = True
    row_1[4] = True
    row_1[6] = True
    print(row_1)
    del row_1[4]
    print(row_1)
    del row_1[1]
    print(row_1)
    del row_1[6]
    print(row_1)

    row_2 = RingLinkedList()
    row_2[2] = True
    row_2[3] = True
    row_2[5] = True
    print(row_2)

    row_3 = RingLinkedList()
    row_3[6] = True
    row_3[5] = True
    print(row_3)

    row_4 = RingLinkedList()
    row_4[1] = True
    row_4[6] = True
    row_4[4] = True
    print(row_4)


if __name__ == "__main__":
    test()
