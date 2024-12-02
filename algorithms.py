def is_cycle(adjacency_matrix):
    """
    Проверяет, является ли граф циклом (C_k).
    Условие:
        - Каждый узел имеет степень ровно 2.
        - Граф связный.
    Возвращает:
        - True, если граф - цикл, иначе False.
    """
    n = len(adjacency_matrix)
    degrees = [sum(row) for row in adjacency_matrix]

    # Проверяем, что все степени равны 2
    if all(degree == 2 for degree in degrees):
        # Проверяем связность
        if is_connected(adjacency_matrix):
            return n  # Возвращаем количество вершин (k) для цикла C_k
    return False


def is_complete_graph(adjacency_matrix):
    """
    Проверяет, является ли граф полным (K_p).
    Условие:
        - Количество рёбер: n * (n - 1) / 2.
    Возвращает:
        - True, если граф - полный, иначе False.
    """
    n = len(adjacency_matrix)
    # В полном графе каждая вершина соединена с (n-1) другими
    expected_edges = n * (n - 1) // 2
    actual_edges = sum(sum(row) for row in adjacency_matrix) // 2
    if actual_edges == expected_edges:
        return n  # Возвращаем количество вершин (p) для полного графа K_p
    return False


def is_empty_graph(adjacency_matrix):
    """
    Проверяет, является ли граф пустым (K_p).
    Условие:
        - Нет рёбер.
    Возвращает:
        - True, если граф - пустой, иначе False.
    """
    if all(all(cell == 0 for cell in row) for row in adjacency_matrix):
        return len(adjacency_matrix)  # Возвращаем количество вершин (p) для пустого графа
    return False


def is_star_graph(adjacency_matrix):
    """
    Проверяет, является ли граф звёздным (S_n).
    Условие:
        - Один узел имеет степень n-1.
        - Все остальные узлы имеют степень 1.
    Возвращает:
        - True, если граф - звёздный, иначе False.
    """
    n = len(adjacency_matrix)
    degrees = [sum(row) for row in adjacency_matrix]

    # Проверяем, что одна вершина имеет степень n-1, остальные имеют степень 1
    center_count = degrees.count(n - 1)
    leaf_count = degrees.count(1)
    if center_count == 1 and leaf_count == n - 1:
        return n  # Возвращаем количество вершин (n) для звёздного графа S_n
    return False


def is_connected(adjacency_matrix):
    """
    Проверяет связность графа.
    Возвращает:
        - True, если граф связный, иначе False.
    """
    n = len(adjacency_matrix)

    visited = [False] * n

    def dfs(node):
        visited[node] = True
        for neighbor, connected in enumerate(adjacency_matrix[node]):
            if connected and not visited[neighbor]:
                dfs(neighbor)

    # Запускаем DFS с первой вершины
    dfs(0)

    # Граф связный, если все вершины посещены
    return all(visited)


def is_bipartite(adjacency_matrix):
    """
    Проверяет, является ли граф двудольным.
    Условие:
        - Можно разбить вершины на 2 множества так, чтобы рёбра соединяли только вершины из разных множества.
    Возвращает:
        - True, если граф - двудольный, иначе False.
    """
    n = len(adjacency_matrix)
    colors = [-1] * n  # -1 означает, что вершина не окрашена

    def bfs_check(start):
        queue = [start]
        colors[start] = 0
        while queue:
            node = queue.pop(0)
            for neighbor, connected in enumerate(adjacency_matrix[node]):
                if connected:
                    if colors[neighbor] == -1:
                        # Красим соседа в противоположный цвет
                        colors[neighbor] = 1 - colors[node]
                        queue.append(neighbor)
                    elif colors[neighbor] == colors[node]:
                        # Если сосед имеет тот же цвет, граф не двудольный
                        return False
        return True

    # Проверяем все компоненты
    for i in range(n):
        if colors[i] == -1:  # Если вершина не окрашена, начинаем BFS
            if not bfs_check(i):
                return False

    return True


def is_complete_bipartite(adjacency_matrix):
    """
    Проверяет, является ли граф полным двудольным (K_{m,n}).
    Условия:
        1. Граф должен быть двудольным.
        2. Все вершины одной доли должны быть соединены со всеми вершинами другой доли.
    Возвращает:
        - True и размеры групп (m, n), если граф полный двудольный (K_{m,n}).
        - False, если граф не является полным двудольным.
    """
    if not is_bipartite(adjacency_matrix):
        return False  # Если граф не двудольный, то он не может быть полным двудольным.

    n = len(adjacency_matrix)
    colors = [-1] * n

    def bfs_partition(start):
        """BFS для разделения вершин на две группы."""
        queue = [start]
        colors[start] = 0  # Начинаем с первой вершины, красим её в 0
        group_a = {start}  # Группа 0
        group_b = set()    # Группа 1

        while queue:
            node = queue.pop(0)
            for neighbor, connected in enumerate(adjacency_matrix[node]):
                if connected:
                    if colors[neighbor] == -1:
                        # Красим соседа в противоположный цвет
                        colors[neighbor] = 1 - colors[node]
                        if colors[neighbor] == 0:
                            group_a.add(neighbor)
                        else:
                            group_b.add(neighbor)
                        queue.append(neighbor)
                    elif colors[neighbor] == colors[node]:
                        # Если сосед имеет тот же цвет, граф не двудольный
                        return None, None
        return group_a, group_b

    # Находим группы вершин
    for i in range(n):
        if colors[i] == -1:
            group_a, group_b = bfs_partition(i)
            if group_a is None:
                return False

            # Проверяем на полноту двудольности
            for a in group_a:
                for b in group_b:
                    if adjacency_matrix[a][b] != 1 or adjacency_matrix[b][a] != 1:
                        return False

            return True, len(group_a), len(group_b)

    return False


def analyze_graph(adjacency_matrix):
    """
    Анализирует граф и определяет его типы.
    Печатает типы графа, к которым он относится.
    """
    results = []
    if (k := is_cycle(adjacency_matrix)):
        results.append(f"Цикл (C_{k})")
    if (p := is_complete_graph(adjacency_matrix)):
        results.append(f"Полный граф (K_{p})")
    if (p := is_empty_graph(adjacency_matrix)):
        results.append(f"Пустой граф (K_{p})")
    if (n := is_star_graph(adjacency_matrix)):
        results.append(f"Звёздный граф (S_{n})")
    if is_bipartite(adjacency_matrix):
        results.append("Двудольный граф")
    complete_bipartite = is_complete_bipartite(adjacency_matrix)
    if complete_bipartite:
        _, m, n = complete_bipartite
        results.append(f"Полный двудольный граф (K_{{{m},{n}}})")

    if not results:
        print("Граф не принадлежит ни одному из известных типов.")
    else:
        print("Граф принадлежит следующим типам:", ", ".join(results))

    return results