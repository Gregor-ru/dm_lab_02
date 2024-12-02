import time
import os
from tabulate import tabulate
import algorithms


def test_graphs():
    """
    Функция для тестирования всех файлов с тестовыми данными.
    Для каждого файла:
    1. Прочитает графы, применит функцию analyze_graph.
    2. Измерит время работы и память.
    3. Выведет сводную таблицу.
    """
    # Список типов графов
    graph_types = ['cycle', 'complete', 'empty', 'star', 'bipartite', 'complete_bipartite']

    # Словарь для сбора результатов по времени
    time_results = {graph_type: {} for graph_type in graph_types}

    # Проходим по каждому типу графа
    for graph_type in graph_types:
        filename = f"{graph_type}_graphs.txt"

        # Проверяем существование файла
        if not os.path.exists(filename):
            print(f"Файл {filename} не найден!")
            continue

        with open(filename, 'r') as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
            # Извлекаем параметры графа (размер, m и n для двудольных графов)
            size_line = lines[i].strip()
            # Пропускаем пустые строки
            if not size_line:
                i += 1
                continue

            try:
                # Если в size_line есть пробел, то это двудольный граф (m и n)
                if " " in size_line:
                    m, n = map(int, size_line.split())
                    size = m + n
                else:
                    size = int(size_line)
            except ValueError:
                print(f"Ошибка: не удалось прочитать размер графа на строке {i + 1}. Пропускаем эту строку.")
                i += 1
                continue

            adjacency_matrix = []
            i += 1
            # Читаем таблицу смежности
            for _ in range(size):
                row = list(map(int, lines[i].strip().split()))
                adjacency_matrix.append(row)
                i += 1

            # Тестирование
            start_time = time.perf_counter()

            # Анализируем граф
            graph_types_list = algorithms.analyze_graph(adjacency_matrix)

            end_time = time.perf_counter()

            elapsed_time = end_time - start_time

            # Выводим результаты для текущего графа
            print(f"Граф размера {size} ({graph_type}):")
            print(f"  Время работы: {elapsed_time:.16f} секунд")
            print("  Типы графа:", ", ".join(graph_types_list))  # Здесь теперь список
            print("-" * 50)

            # Сохраняем данные для сводной таблицы
            if size not in time_results[graph_type]:
                time_results[graph_type][size] = []
            time_results[graph_type][size].append(elapsed_time)

    # Подготовим данные для сводной таблицы
    table_data = []
    headers = ["Размер"] + graph_types  # Заголовки таблицы

    # Собираем уникальные размеры графов
    all_sizes = sorted({size for graph_type in graph_types for size in time_results[graph_type]})

    for size in all_sizes:
        row = [size]
        for graph_type in graph_types:
            if size in time_results[graph_type]:
                avg_time = sum(time_results[graph_type][size]) / len(time_results[graph_type][size])
                row.append(f"{avg_time:.16f}")
            else:
                row.append("N/A")
        table_data.append(row)

    # Выводим сводную таблицу
    print("\nСводная таблица по времени:")
    print(tabulate(table_data, headers=headers, tablefmt="pretty"))
