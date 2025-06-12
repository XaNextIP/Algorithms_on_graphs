import csv
import configparser
import time

def printfile(file, massiv):
    with open(f'{file}.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=';', quotechar='"')
        for line in massiv:
            writer.writerow(line)

def kruskal(edges, top_count):
    total = 0
    edges.sort(key=lambda x: x[2])  # сортируем ребра по весу
    parents = [i for i in range(top_count)]
    size = [1] * top_count
    result = [[] for _ in range(top_count)]

    def find(x):
        while x != parents[x]:
            parents[x] = parents[parents[x]]
            x = parents[x]
        return x

    for u, v, weight in edges:
        u -= 1
        v -= 1
        root_u = find(u)
        root_v = find(v)

        if root_u != root_v:
            if size[root_u] < size[root_v]:
                root_u, root_v = root_v, root_u
            parents[root_v] = root_u
            size[root_u] += size[root_v]

            result[u].append(v + 1)
            result[u].append(weight)
            result[v].append(u + 1)
            result[v].append(weight)
            total += weight

    print('Длина пути =', total)
    printfile(output_file, result)

# Чтение конфигурации
config = configparser.ConfigParser()
config.read("kraskal.ini")
input_file = config["kraskal"]['input']
output_file = config["kraskal"]['output']

start_time = time.time()

Edges = []
vertices_count = 0

with open(f'{input_file}.csv', newline='') as f:
    reader = csv.reader(f, delimiter=';')
    for i, row in enumerate(reader):
        if not row or all(x.strip() == '' for x in row):
            continue
        current_vertex = i + 1
        j = 0
        while j < len(row) - 1:
            try:
                neighbor = int(row[j])
                weight = int(row[j + 1])
                Edges.append([current_vertex, neighbor, weight])
                vertices_count = max(vertices_count, current_vertex, neighbor)
            except ValueError:
                pass
            j += 2

end_time = time.time()
print("Время чтения файла", end_time - start_time)

start_time = time.time()
kruskal(Edges, vertices_count)
end_time = time.time()

print("Время выполнения", end_time - start_time)
