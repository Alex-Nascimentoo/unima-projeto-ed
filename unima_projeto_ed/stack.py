class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):
        """Empilha (no topo)."""
        self._data.append(item)

    def pop(self):
        """Desempilha e retorna o topo."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self):
        """Olha o topo sem remover."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)
