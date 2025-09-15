# Fila de prioridade implementada com heap binário mínimo
class PriorityQueue:
    def __init__(self):
        # Lista que armazena os elementos como tuplas (prioridade, item)
        self.heap = []
        # Contador do número de elementos na fila
        self.size = 0
    
    # Retorna o índice do pai de um nó
    def _parent(self, i):
        return (i - 1) // 2
    
    # Retorna o índice do filho esquerdo
    def _left_child(self, i):
        return 2 * i + 1
    
    # Retorna o índice do filho direito
    def _right_child(self, i):
        return 2 * i + 2
    
    # Troca dois elementos de posição no heap
    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    # Move um elemento para cima até encontrar sua posição correta
    def _heapify_up(self, i):
        # Enquanto não for a raiz e o pai tiver prioridade maior
        while i > 0 and self.heap[self._parent(i)][0] > self.heap[i][0]:
            self._swap(i, self._parent(i))
            i = self._parent(i)
    
    # Move um elemento para baixo até encontrar sua posição correta
    def _heapify_down(self, i):
        while self._left_child(i) < self.size:
            # Encontra o filho com menor prioridade
            min_child = self._left_child(i)
            if (self._right_child(i) < self.size and 
                self.heap[self._right_child(i)][0] < self.heap[min_child][0]):
                min_child = self._right_child(i)
            
            # Se o elemento já está na posição correta, para
            if self.heap[i][0] <= self.heap[min_child][0]:
                break
            
            self._swap(i, min_child)
            i = min_child
    
    # Adiciona um novo elemento com sua prioridade
    def push(self, priority, item):
        self.heap.append((priority, item))
        self._heapify_up(self.size)
        self.size += 1
    
    # Remove e retorna o elemento com menor prioridade
    def pop(self):
        if self.size == 0:
            raise IndexError("pop from empty priority queue")
        
        # Salva o elemento de menor prioridade (raiz)
        min_item = self.heap[0]
        # Move o último elemento para a raiz
        self.heap[0] = self.heap[self.size - 1]
        self.size -= 1
        self.heap.pop()
        
        # Reorganiza o heap se ainda houver elementos
        if self.size > 0:
            self._heapify_down(0)
        
        return min_item[1]
    
    # Retorna o elemento com menor prioridade sem removê-lo
    def peek(self):
        if self.size == 0:
            raise IndexError("peek from empty priority queue")
        return self.heap[0][1]
    
    # Verifica se a fila está vazia
    def is_empty(self):
        return self.size == 0
    
    # Retorna o número de elementos na fila
    def __len__(self):
        return self.size