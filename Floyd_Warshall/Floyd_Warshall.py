import time
import numpy as np
from numba import njit, prange
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

start_time = time.time()

@njit(parallel=True, nogil=True)
def floyd_warshall(adj_matrix):
    n = adj_matrix.shape[0]
    dist = adj_matrix.copy()
    path = np.full((n, n), -1, dtype=np.int64)
    for k in prange(n):
        for i in prange(n):
            for j in prange(n):
                if dist[i, k] + dist[k, j] < dist[i, j]:
                    dist[i, j] = dist[i, k] + dist[k, j]
                    path[i, j] = k
    return dist, path

def reconstruct_path(path, i, j):
    if path[i, j] == -1:
        return [i, j]
    k = path[i, j]
    return reconstruct_path(path, i, k)[:-1] + reconstruct_path(path, k, j)

print("Файл считывается...")
file = f'{config["Graph"]["filename"]}.csv'
with open(file, 'r') as f:
    adj_list = [list(map(int, line.strip().split(';'))) for line in f if line.strip()]

n = len(adj_list)
adj_matrix = np.full((n, n), np.inf, dtype=np.float64)
for i in range(n):
    for j in range(0, len(adj_list[i]), 2):
        neighbor = adj_list[i][j]
        weight = adj_list[i][j + 1]
        adj_matrix[i, neighbor] = weight
np.fill_diagonal(adj_matrix, 0)

print("Файл считан. Запуск алгоритма...")
distances, path = floyd_warshall(adj_matrix)
elapsed = time.time() - start_time

i, j = 195, 463
if distances[i, j] == np.inf:
    print(f"Кратчайшего пути из {i} в {j} не существует.")
else:
    print(f"Кратчайший путь из {i} в {j} равен {int(distances[i, j])}")
    full_path = reconstruct_path(path, i, j)
    print("Путь:", " --> ".join(map(str, full_path)))

print(f"Алгоритм выполнился за {elapsed:.6f} секунд")
