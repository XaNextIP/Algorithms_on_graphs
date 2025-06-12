import csv
import configparser
import time
from collections import deque

# Читаем конфиг
config = configparser.ConfigParser()
config.read("dinic.ini")
input_file = config["dinic"]['input']
output_file = config["dinic"]['output']

cfg = configparser.ConfigParser()
cfg.read('config.ini')
N = int(cfg['Graph']['top'])

# Инициализация матрицы смежности (N x N) нулями
g = [[0] * N for _ in range(N)]

# Чтение графа из CSV файла
# Ожидаем формат: каждая строка содержит ребра из вершины i в формате
# вершина_сосед;пропускная_способность;вершина_сосед;пропускная_способность;...
with open(f'{input_file}.csv', newline='') as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        if not row or not row[0].strip():
            continue
        line = row[0]
        parts = line.split(';')
        # Парсим по парам
        for j in range(0, len(parts), 2):
            if j+1 < len(parts):
                neighbor = int(parts[j])
                capacity = int(parts[j+1])
                g[i][neighbor] = capacity

s = 0      # Источник
t = N - 1  # Сток

def bfs(s, t, parent):
    visited = [False] * len(g)
    queue = deque()
    queue.append(s)
    visited[s] = True
    while queue:
        u = queue.popleft()
        for v, cap in enumerate(g[u]):
            if not visited[v] and cap > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u
                if v == t:
                    return True
    return False

def dinic(s, t):
    parent = [-1] * len(g)
    max_flow = 0
    path_number = 1

    while bfs(s, t, parent):
        # Найдём минимальную пропускную способность на найденном пути
        flow = float('inf')
        v = t
        path = []
        while v != s:
            path.append(v)
            u = parent[v]
            flow = min(flow, g[u][v])
            v = u
        path.append(s)
        path.reverse()

        print(f"Путь {path_number}: {path}, поток по пути: {flow}")
        path_number += 1

        max_flow += flow

        # Обновляем остаточные мощности в графе
        v = t
        while v != s:
            u = parent[v]
            g[u][v] -= flow
            g[v][u] += flow
            v = u

    return max_flow

start_time = time.time()
max_flow = dinic(s, t)
end_time = time.time()

print("Максимальный поток равен", max_flow)
print("Время выполнения:", end_time - start_time)
