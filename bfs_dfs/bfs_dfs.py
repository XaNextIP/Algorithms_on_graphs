import csv
import configparser
import random

config = configparser.ConfigParser()
config.read("settings.ini")
file = config["bfs_dfs"]['filename']
start = int(config["bfs_dfs"]['start_search'])

def bfs(graph, start):
    if start >= len(graph):
        return 'не удался, так как такой вершины нет'

    order = []
    visited = set()
    queue = [start]
    visited.add(start)

    unvisited = set(range(len(graph)))

    communication = False

    while queue:
        v = queue.pop(0)
        order.append(v)
        unvisited.discard(v)
        for neighbor in graph[v]:
            n = int(neighbor)
            if n not in visited:
                visited.add(n)
                queue.append(n)

        # Если очередь пуста, но остались непосещённые вершины (несвязный граф)
        if not queue and unvisited:
            v = random.choice(list(unvisited))
            queue.append(v)
            visited.add(v)
            communication = True

    if communication:
        print('Граф несвязанный')

    print('Перечень обхода в ширину насчитывает', len(order), 'вершин')
    return order


def dfs(graph, start):
    if start >= len(graph):
        return 'не удался, так как такой вершины нет'

    order = []
    visited = set()
    stack = [start]
    visited.add(start)

    unvisited = set(range(len(graph)))

    communication = False

    while stack:
        v = stack.pop()
        order.append(v)
        unvisited.discard(v)
        for neighbor in graph[v]:
            n = int(neighbor)
            if n not in visited:
                visited.add(n)
                stack.append(n)

        if not stack and unvisited:
            v = random.choice(list(unvisited))
            stack.append(v)
            visited.add(v)
            communication = True

    if communication:
        print('Граф несвязанный')

    print('Перечень обхода в глубину насчитывает', len(order), 'вершин')
    return order


def main():
    graph = []

    with open(f'{file}.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            # Преобразуем элементы строки в числа, игнорируем пустые
            neighbors = [x for x in row if x != '']
            graph.append(neighbors)

    print("Граф (списки соседей):")
    for i, neighbors in enumerate(graph):
        print(f"{i}: {neighbors}")

    print("\nОбход в ширину:", bfs(graph, start))
    print("Обход в глубину:", dfs(graph, start))


if __name__ == '__main__':
    main()
