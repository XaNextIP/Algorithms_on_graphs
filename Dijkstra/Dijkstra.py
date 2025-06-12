import csv
import configparser
import time
import heapq
from math import inf

def read_graph(filename):
    G = {}
    with open(f"{filename}.csv", newline='') as f:
        reader = csv.reader(f, delimiter=';')
        for idx, row in enumerate(reader):
            if not row:
                continue
            values = list(map(int, row))
            G[idx] = [(values[i], values[i+1]) for i in range(0, len(values), 2)]
    return G

def dijkstra(graph, start, end):
    N = len(graph)
    dist = [inf] * N
    prev = [None] * N
    dist[start] = 0
    heap = [(0, start)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph.get(u, []):
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))

    if dist[end] == inf:
        return -1, "Путь не существует"
    
    # восстановление пути
    path = []
    u = end
    while u is not None:
        path.append(u)
        u = prev[u]
    path.reverse()
    return dist[end], path

def main():
    config = configparser.ConfigParser()
    config.read("Dijkstra.ini")
    input_file = config["Dijkstra"]['input']

    print("Считывание файла...")
    start = time.time()
    graph = read_graph(input_file)
    N = len(graph)
    print(f"Файл считан за {time.time() - start:.6f} сек")

    print("Запуск алгоритма Дейкстры...")
    start = time.time()
    total_distance, path = dijkstra(graph, 0, N - 1)
    duration = time.time() - start

    if total_distance == -1:
        print(path)
    else:
        print(f"Длина кратчайшего пути: {total_distance}")
        print("Путь:", " - ".join(map(str, path)))
    print(f"Алгоритм сработал за {duration:.6f} сек")

if __name__ == "__main__":
    main()
