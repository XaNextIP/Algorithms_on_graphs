import random
import csv
import configparser

def printfile(filename, graph):
    """Сохранить граф в CSV файл с разделителем ;"""
    with open(f'{filename}.csv', 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter=';', quotechar='"')
        for line in graph:
            writer.writerow(line)

def oriented(top, edges, filename):
    length = list(range(edges + 1))  # включаем edges
    graph = []

    for i in range(top):
        width = list(range(top))
        A = random.choice(length)
        while A == 0:
            A = random.choice(length)

        neighbors = []
        y = 0

        while y < A and width:
            B = random.choice(width)
            if B == i:
                width.remove(B)
                continue
            neighbors.append(B)
            width.remove(B)
            y += 1

        graph.append(neighbors)

    printfile(filename, graph)

def not_oriented(top, edges, filename):
    length = list(range(edges + 1))
    graph = [[] for _ in range(top)]

    for i in range(top):
        width = list(range(top))
        A = random.choice(length)
        while A == 0:
            A = random.choice(length)

        neighbors = []
        y = 0
        while y < A and width:
            B = random.choice(width)
            if B == i:
                width.remove(B)
                continue
            neighbors.append(B)
            width.remove(B)

            # Добавляем связь в обратную сторону, если её нет
            if i not in graph[B]:
                graph[B].append(i)
            y += 1

        # Объединяем и убираем дубликаты
        graph[i] = list(set(graph[i] + neighbors))

    # Ограничиваем количество соседей до edges
    for i in range(top):
        while len(graph[i]) > edges:
            to_remove = random.choice(graph[i])
            graph[i].remove(to_remove)
            if i in graph[to_remove]:
                graph[to_remove].remove(i)

    printfile(filename, graph)

def not_oriented_ves(top, edges, filename, rib):
    graph = [[] for _ in range(top)]

    for i in range(top):
        width = list(range(top))
        neighbors = []
        y = 0

        while y < edges and width:
            if i <= 9:
                B = random.randint(0, 9)
                if B == i:
                    continue
            else:
                B = random.randint(0, i - 1) if i > 0 else 0
                if B == i:
                    continue

            if B not in width:
                continue

            weight = random.randint(1, rib)
            neighbors.extend([B, weight])
            width.remove(B)

            # Добавляем обратное ребро
            graph[B].extend([i, weight])
            y += 1

        graph[i].extend(neighbors)

    printfile(filename, graph)

def suspended_not_oriented_graf(top, edges, rib, filename):
    global res
    for i in range(top):
        vertex_selection = [v for v in range(top) if v != i]
        connection_number = random.randint(1, edges)
        # Убираем уже связанных вершин из выбора
        for v in res[i]:
            try:
                vi = int(v) - 1
                if vi in vertex_selection:
                    vertex_selection.remove(vi)
            except ValueError:
                continue
        s = len(res[i]) // 2  # так как рёбра хранятся парами (вершина, вес)
        while s < connection_number:
            if not vertex_selection:
                break
            rand_edge = random.choice(vertex_selection)
            if len(res[rand_edge]) // 2 >= edges:
                vertex_selection.remove(rand_edge)
                continue
            distance = random.randint(1, rib)
            res[i].extend([str(rand_edge + 1), str(distance)])
            res[rand_edge].extend([str(i + 1), str(distance)])
            vertex_selection.remove(rand_edge)
            s += 1

    printfile(filename, res)

def transport_network(top, edges, rib, filename):
    length = list(range(1, edges + 1))
    graph = []

    for i in range(top):
        if i == 0:
            width = list(range(top))
            A = random.choice(length)
            neighbors = []
            y = 0
            while y < A and width:
                B = random.choice(width)
                if B == i or B == top - 1:
                    width.remove(B)
                    continue
                weight = random.randint(1, rib)
                neighbors.extend([B, weight])
                width.remove(B)
                y += 1
            graph.append(neighbors)
        elif 0 < i < top - 1:
            width = list(range(1, top))
            A = random.choice(length)
            neighbors = []
            y = 0
            while y < A and width:
                B = random.choice(width)
                if B == i:
                    width.remove(B)
                    continue
                weight = random.randint(1, rib)
                neighbors.extend([B, weight])
                width.remove(B)
                y += 1
            graph.append(neighbors)
        else:
            graph.append([])  # для вершины top-1 пустой список

    printfile(filename, graph)

def bipartite_graph(top, rib, filename):
    graph = [[] for _ in range(top)]
    for i in range(top):
        for y in range(top):
            weight = random.randint(1, rib)
            graph[i].extend([y, weight])
    printfile(filename, graph)

def oriented_ves(top, sv, filename, ves):
    graph = [[] for _ in range(top)]
    for i in range(top):
        neighbors = []
        candidates = list(range(top))
        while len(neighbors) / 2 < sv and candidates:
            x = random.choice(candidates)
            candidates.remove(x)
            weight = random.randint(1, ves)
            neighbors.extend([x, weight])
        graph[i] = neighbors
    printfile(filename, graph)

# Main

config = configparser.ConfigParser()
config.read("config.ini")

top = int(config["Graph"]['top'])
edges = int(config["Graph"]['edges'])
filename = config["Graph"]['filename']
choice = config["Graph"]['oriented_or_not']
rib = int(config["Graph"]['rib_weight'])

res = [[] for _ in range(top)]

if choice == '1':
    oriented(top, edges, filename)
elif choice == '2':
    not_oriented(top, edges, filename)
elif choice == '3':
    # Для suspended_not_oriented_graf нужна инициализация res
    # Можно сгенерировать базовый граф без весов, а потом дописать веса
    not_oriented(top, edges, filename)  # Инициализация res для примера
    with open(f'{filename}.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        res = [list(row) for row in reader]
    suspended_not_oriented_graf(top, edges, rib, filename)
elif choice == '4':
    transport_network(top, edges, rib, filename)
elif choice == '5':
    bipartite_graph(top, rib, filename)
elif choice == '6':
    oriented_ves(top, edges, filename, rib)
else:
    print("Неверный выбор типа графа в config.ini")
