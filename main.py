import algorithms
import generate_test_data
import  resources_testing

def read_one_graph_from_file(filename):
    """
    Читает граф из файла в виде матрицы смежности.
    Формат файла:
    - Первая строка: количество вершин (N).
    - Следующие N строк: матрица смежности (0 и 1).

    Возвращает:
        - Матрицу смежности (список списков).
    """
    with open(filename, 'r') as file:
        n = int(file.readline().strip())
        adjacency_matrix = [list(map(int, file.readline().split())) for _ in range(n)]
    return adjacency_matrix

def graph_type_test_1():
    filename = "test_1.txt"
    try:
        adjacency_matrix = read_one_graph_from_file(filename)
        algorithms.analyze_graph(adjacency_matrix)
    except FileNotFoundError:
        print("Файл не найден.")
    except Exception as e:
        print(f"Ошибка: {e}")

def graph_generate_test_1():
    n = 5
    print("Циклический граф C_5:")
    cyclic_graph = generate_test_data.generate_graph('cycle', n)
    for row in cyclic_graph:
        print(row)

if __name__ == "__main__":

    # Пример определения вида графа
    graph_type_test_1()

    # Пример генерации тестовых графов
    #graph_generate_test_1()

    # Генерация тестовых для разного размера графа каждого из типов
    #generate_test_data.write_test_data()

    # Тест времени работы алгоритма

    resources_testing.test_graphs()