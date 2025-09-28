class Queue:
    def __init__(self):
        # Usamos uma lista e um índice de cabeça para evitar custo O(n) de pop(0)
        self._data = []
        self._head = 0  # índice do próximo elemento a sair

    def enqueue(self, item):
        """Insere no fim da fila."""
        self._data.append(item)

    def dequeue(self):
        """Remove e retorna o item do início da fila (FIFO)."""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        item = self._data[self._head]
        self._head += 1

        # Compaction ocasional para evitar crescer sem limites
        # (remove prefixo já consumido quando passa de certo tamanho)
        if self._head > 64 and self._head > len(self._data) // 2:
            self._data = self._data[self._head:]
            self._head = 0

        return item

    def peek(self):
        """Olha o primeiro sem remover."""
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._data[self._head]

    def is_empty(self):
        return self._head >= len(self._data)

    def __len__(self):
        return len(self._data) - self._head
