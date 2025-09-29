Unima Projeto ED
================

A sample Flask project managed with Poetry.

Getting Started
---------------

Follow these steps to set up and run the project:

1. **Clone the repository**

    .. code-block:: bash

        git clone https://github.com/your-username/unima-projeto-ed.git
        cd unima-projeto-ed

2. **Install Poetry**

    If you don't have Poetry installed, see: https://python-poetry.org/docs/#installation

3. **Install dependencies**

    .. code-block:: bash

        poetry install

4. **Run the Flask application**

    .. code-block:: bash

        poetry run start

    By default, the app will be available at http://127.0.0.1:5000/



# How to execute tests

## Instalar dependências (se necessário)
pip install matplotlib pytest

## Executar todos os testes com supressão de warnings
pytest test_performance.py -v -s -W ignore::DeprecationWarning

## Executar teste específico do gráfico tempo vs tamanho
pytest test_performance.py::test_performance_vs_graph_size -v -s -W ignore::DeprecationWarning

## Executar teste específico do gráfico nós explorados
pytest test_performance.py::test_nodes_explored_comparison -v -s -W ignore::DeprecationWarning

## Executar teste de performance A-Z
pytest test_performance.py::test_performance_analysis_AZ -v -s -W ignore::DeprecationWarning

## Executar teste de correção
pytest test_performance.py::test_algorithm_correctness_AZ -v -s -W ignore::DeprecationWarning

## Executar com relatório simplificado
pytest test_performance.py -v --tb=short -W ignore::DeprecationWarning
