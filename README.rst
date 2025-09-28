Unima Projeto ED
================

Este projeto é um sistema de **otimização de rotas para entregas urbanas**, desenvolvido na disciplina de Estruturas de Dados. Ele aplica conceitos fundamentais de **grafos**, **algoritmos de menor caminho** e **heurísticas de roteamento de veículos** em um problema real, utilizando dados do **OpenStreetMap** como base.

Objetivo
--------

O objetivo do trabalho é:

- Construir um **grafo** a partir de mapas reais.  
- Implementar os algoritmos de **Dijkstra** e **A\*** para cálculo de menor caminho.  
- Resolver o **Problema de Roteamento de Veículos com Capacidade (CVRP)** por meio da heurística do **Vizinho Mais Próximo**.  
- Implementar manualmente três estruturas de dados:  

  - **Priority Queue**: fila de prioridade baseada em heap binário mínimo.  
  - **Queue**: fila FIFO para gerenciar pedidos de entrega.  
  - **Stack**: pilha LIFO utilizada na reconstrução dos caminhos.  

Funcionamento
-------------

O funcionamento pode ser descrito em três etapas principais:

1. **Construção do Grafo**  
   O mapa é convertido em um grafo, onde cruzamentos se tornam nós e ruas se tornam arestas ponderadas pela distância entre os pontos, calculada pela fórmula de Haversine em quilômetros.  

2. **Algoritmos de Menor Caminho**  
   São aplicados **Dijkstra** (explorando todas as possibilidades) e **A\*** (versão otimizada com heurística admissível, usando a distância em linha reta entre os pontos).  

3. **Resolução do CVRP**  
   Considera um depósito central e clientes com demandas específicas. A capacidade máxima do veículo é respeitada, e as rotas sempre começam e terminam no depósito, utilizando a heurística do vizinho mais próximo.  

Requisitos e Instalação
-----------------------

Para executar o projeto, é necessário:

- **Python 3.10 ou superior**  
- **Poetry** instalado  

Passos para instalação:

.. code-block:: bash

   # Clonar o repositório
   git clone https://github.com/Alex-Nascimentoo/unima-projeto-ed.git

   # Entrar na pasta do projeto
   cd unima-projeto-ed

   # Instalar as dependências
   poetry install

Modos de Execução
-----------------

Existem três formas de executar o projeto:

**Modo Batch com A\***  

.. code-block:: bash

   poetry run python -m unima_projeto_ed.main --mode batch --sp a_star

**Modo Batch com Dijkstra**  

.. code-block:: bash

   poetry run python -m unima_projeto_ed.main --mode batch --sp dijkstra

Em ambos os modos *batch*, o terminal exibirá as rotas geradas, mostrando o depósito, os clientes visitados e a distância total percorrida em quilômetros.  

**Modo API Flask**  

.. code-block:: bash

   poetry run python -m unima_projeto_ed.main --mode api

A API ficará disponível em `http://127.0.0.1:5000/` e responderá com a mensagem:  

.. code-block:: json

   {"message": "API de Roteamento pronta!"}

Exemplo de Saída
----------------

No modo *batch*, um exemplo de saída é:

.. code-block:: text

   Rotas geradas (Vizinho Mais Próximo + A_STAR):
   Rota 1: 364129879 -> 431187370 -> 431187375 -> 364129879
   Rota 2: 364129879 -> 431187380 -> 364129879
   Distância total (km): 3.48

Análise de Complexidade
-----------------------

- **Fila de Prioridade (Heap Binário Mínimo):** custo de O(log N) para inserção e remoção.  
- **Dijkstra:** complexidade O((V + E) log V).  
- **A\*:** mesma ordem no pior caso, mas tende a expandir menos nós devido à heurística.  
- **CVRP:**  

  - Construção da matriz de distâncias: O(m² * SPC), onde m é o número de pontos (depósito + clientes) e SPC é o custo de uma execução de shortest path (A\* ou Dijkstra).  
  - Construção final das rotas: O(n²) sobre os clientes.  

Observações Importantes
-----------------------

- Os pesos das arestas representam distâncias em quilômetros, calculadas pela fórmula de Haversine.  
- As ruas foram tratadas como bidirecionais sempre que possível.  
- O sistema não leva em consideração fatores como tempo de viagem, semáforos ou tráfego.  
- É necessário acesso à internet para consultar a **Overpass API**, que fornece os dados do OpenStreetMap usados para montar o grafo.  

Autores
-------

Este trabalho foi desenvolvido por:

- Ygor Gabriel  
- Henrique de Moraes  
- Felipe Sorrentino  
- Alex Nascimento  
- Gabriel Calheiros  
