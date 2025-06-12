import csv
import configparser
import time
from collections import defaultdict

config = configparser.ConfigParser()
config.read("kosaraju.ini")
input_file = config["kosaraju"]['input']
output_file = config["kosaraju"]['output']

def printfile(file, massiv):
    # Записываем список списков в CSV файл
    with open(f'{file}.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=';', quotechar='"')
        for line in massiv:
            writer.writerow(line)

def dfs(G, start):
    # Обход в глубину (стек)
    if start not in G:
        print(f'Данной вершины {start} нет в графе')
        return None
    order = []
    visited = set([start])
    stack = [start]

    while stack:
        v = stack.pop()
        order.append(v)
        # Выбираем соседей, которые ещё не посещены
        for neighbor in G[v]:
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
    return order

def transpose(G):
    # Транспонирование графа — создаём новый граф с обратными рёбрами
    P = defaultdict(list)
    for v in G:
        for w in G[v]:
            P[w].append(v)
    # Добавляем вершины без входящих рёбер, чтобы они были в графе
    for v in G:
        if v not in P:
            P[v] = []
    return dict(P)

def kosaraju(G):
    # Первый проход — формируем порядок вершин по времени выхода из dfs
    visited = {k: False for k in G}
    stack = []

    for vertex in G:
        if not visited[vertex]:
            comp = dfs(G, vertex)
            if comp is not None:
                comp.reverse()
                for v in comp:
                    if not visited[v]:
                        stack.append(v)
                        visited[v] = True

    # Транспонируем граф
    GT = transpose(G)

    # Второй проход — поиск компонент сильной связности
    visited = {k: False for k in G}
    components = []

    while stack:
        v = stack.pop()
        if not visited[v]:
            comp = dfs(GT, v)
            comp = [node for node in comp if not visited[node]]
            if comp:
                components.append(comp)
                for node in comp:
                    visited[node] = True
    return components

def remove_duplicates_preserve_order(seq):
    seen = set()
    res = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            res.append(item)
    return res

def main():
    graph = []
    G = {}

    with open(f'{input_file}.csv', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row or not row[0].strip():
                continue
            line = row[0]
            parts = line.split(';')
            # Убираем дубликаты, сохраняя порядок
            filtered = remove_duplicates_preserve_order(parts)
            graph.append(filtered)

    # Преобразуем в словарь: ключ — строка индекса вершины, значение — список соседей
    for idx, neighbors in enumerate(graph):
        G[str(idx)] = neighbors

    components = kosaraju(G)

    print("Компоненты связности:", components)

    # Находим максимальную компоненту по размеру
    if components:
        max_comp = max(components, key=len)
    else:
        max_comp = []

    print("Максимально связная компонента:", max_comp)

    printfile(output_file, components)

if __name__ == '__main__':
    main()
