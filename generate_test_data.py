import random

def generate_random_graph(n, edge_count):
    """
    Генерация случайного графа с n вершинами и заданным количеством рёбер.
    """
    adj_matrix = [[0] * n for _ in range(n)]
    edges = set()

    while len(edges) < edge_count:
        u, v = random.sample(range(n), 2)
        if u != v:
            edges.add(tuple(sorted((u, v))))

    for u, v in edges:
        adj_matrix[u][v] = 1
        adj_matrix[v][u] = 1

    return adj_matrix

def generate_graph(graph_type, size):
    """
    Генерирует граф заданного типа и размера.
    Возвращает таблицу смежности графа.
    """
    adjacency_matrix = [[0] * size for _ in range(size)]

    if graph_type == 'cycle':
        for i in range(size):
            adjacency_matrix[i][(i + 1) % size] = 1
            adjacency_matrix[(i + 1) % size][i] = 1
    elif graph_type == 'complete':
        for i in range(size):
            for j in range(i + 1, size):
                adjacency_matrix[i][j] = 1
                adjacency_matrix[j][i] = 1
    elif graph_type == 'empty':
        pass  # Пустой граф (нет рёбер)
    elif graph_type == 'star':
        center = random.randint(0, size - 1)
        for i in range(size):
            if i != center:
                adjacency_matrix[center][i] = 1
                adjacency_matrix[i][center] = 1
    elif graph_type == 'bipartite':
        # Двудольный граф
        half_size = size // 2
        for i in range(half_size):
            for j in range(half_size, size):
                adjacency_matrix[i][j] = 1
                adjacency_matrix[j][i] = 1
    elif graph_type == 'complete_bipartite':
        # Полный двудольный граф K_{m,n}
        half_size = size // 2
        for i in range(half_size):
            for j in range(half_size, size):
                adjacency_matrix[i][j] = 1
                adjacency_matrix[j][i] = 1
    return adjacency_matrix


def write_test_data():
    """
    Записывает тестовые графы в отдельные файлы для каждого типа графа.
    В каждом файле указаны параметры графа, после которых идет таблица смежности.
    """
    # Список типов графов
    graph_types = ['cycle', 'complete', 'empty', 'star', 'bipartite', 'complete_bipartite']

    # Проходим по каждому типу графа
    for graph_type in graph_types:
        # Открываем файл для записи графов этого типа
        with open(f"{graph_type}_graphs.txt", 'w') as f:
            # Записываем графы для каждого размера от 5 до 50 с шагом 5
            for size in range(5, 51, 5):
                # Генерируем граф
                adjacency_matrix = generate_graph(graph_type, size)

                # Параметры графа
                if graph_type == 'cycle':
                    f.write(f"{size}\n")
                elif graph_type == 'complete':
                    f.write(f"{size}\n")
                elif graph_type == 'empty':
                    f.write(f"{size}\n")
                elif graph_type == 'star':
                    f.write(f"{size}\n")
                elif graph_type == 'bipartite':
                    f.write(f"{size}\n")
                elif graph_type == 'complete_bipartite':
                    m = size // 2
                    n = size - m
                    f.write(f"{m} {n}\n")

                # Записываем таблицу смежности
                for row in adjacency_matrix:
                    f.write(' '.join(map(str, row)) + '\n')

                f.write('\n')  # Разделяем графы пустой строкой для удобства

