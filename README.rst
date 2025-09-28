# Unima Projeto ED

Este projeto é um sistema de **otimização de rotas para entregas urbanas**, desenvolvido na disciplina de Estruturas de Dados. Ele aplica conceitos fundamentais de **grafos**, **algoritmos de menor caminho** e **heurísticas de roteamento de veículos** em um problema prático do dia a dia. Para isso, utilizamos dados reais do **OpenStreetMap**, que são transformados em grafos e usados para simular a operação de entregas urbanas.

---

## 🎯 Objetivo

O trabalho tem como principais metas:

- Construir um **grafo** a partir de dados reais do OSM.  
- Implementar dois algoritmos clássicos de **menor caminho**:  
  - **Dijkstra** (base).  
  - **A\*** (com heurística haversine).  
- Resolver o **Problema de Roteamento de Veículos com Capacidade (CVRP)** usando a heurística do **Vizinho Mais Próximo**.  
- Utilizar **estruturas de dados implementadas manualmente**, como:  
  - **Priority Queue** (heap binário mínimo).  
  - **Queue** (FIFO) para pedidos de entrega.  
  - **Stack** (LIFO) para reconstrução de caminhos.  

---

## ⚙️ Como funciona

O funcionamento do sistema acontece em três etapas principais:

1. **Mapa → Grafo**  
   As ruas e cruzamentos do OpenStreetMap são transformados em nós e arestas. Cada aresta recebe como peso a **distância em quilômetros**, calculada pela fórmula de haversine.  

2. **Menor Caminho**  
   - O algoritmo de **Dijkstra** encontra sempre o menor caminho explorando todas as possibilidades.  
   - O algoritmo **A\*** é uma versão otimizada que utiliza a distância em linha reta como heurística para guiar a busca e reduzir a quantidade de nós explorados.  

3. **CVRP (Capacitated Vehicle Routing Problem)**  
   Um depósito central e clientes com demandas são definidos. O sistema respeita a **capacidade máxima do veículo**, garantindo que as rotas comecem e terminem no depósito. A heurística do vizinho mais próximo é usada para construir essas rotas.  

---

## 🚀 Instalação e Execução

> **Requisitos:** [Python 3.10+](https://www.python.org/) e [Poetry](https://python-poetry.org/docs/#installation).  

No terminal, execute:

```bash
# 1) Clonar o repositório
git clone https://github.com/Alex-Nascimentoo/unima-projeto-ed.git
cd unima-projeto-ed

# 2) Instalar as dependências
poetry install

# 3) Executar o sistema

# --- Batch com A* (default) ---
# Calcula rotas usando A*. Saída: rotas geradas + distância total (em km).
poetry run python -m unima_projeto_ed.main --mode batch --sp a_star

# --- Batch com Dijkstra ---
# Calcula rotas usando Dijkstra. Saída: rotas geradas + distância total (em km).
poetry run python -m unima_projeto_ed.main --mode batch --sp dijkstra

# --- API Flask ---
# Sobe uma API HTTP em http://127.0.0.1:5000/
# Ao acessar no navegador, retorna {"message": "API de Roteamento pronta!"}.
poetry run python -m unima_projeto_ed.main --mode api
