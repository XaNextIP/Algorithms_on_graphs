import numpy as np
import configparser
import csv
import time

def load_matrix(input_filename):
    with open(f"{input_filename}.csv", newline='') as file:
        reader = csv.reader(file, delimiter=';')
        matrix = [[int(cell) for cell in row] for row in reader if row]
    return matrix

def min_zero_row(zero_mat, mark_zero):
    min_row = [float('inf'), -1]
    for row_num in range(zero_mat.shape[0]):
        count_zeros = np.sum(zero_mat[row_num])
        if 0 < count_zeros < min_row[0]:
            min_row = [count_zeros, row_num]

    zero_index = np.where(zero_mat[min_row[1]])[0][0]
    mark_zero.append((min_row[1], zero_index))
    zero_mat[min_row[1], :] = False
    zero_mat[:, zero_index] = False

def mark_matrix(mat):
    zero_bool_mat = (mat == 0)
    zero_bool_mat_copy = zero_bool_mat.copy()
    marked_zero = []

    while np.any(zero_bool_mat_copy):
        min_zero_row(zero_bool_mat_copy, marked_zero)

    marked_zero_row = {r for r, _ in marked_zero}
    marked_zero_col = {c for _, c in marked_zero}
    non_marked_row = list(set(range(mat.shape[0])) - marked_zero_row)

    marked_cols = set()
    changed = True
    while changed:
        changed = False
        for row in non_marked_row:
            for col, val in enumerate(zero_bool_mat[row]):
                if val and col not in marked_cols:
                    marked_cols.add(col)
                    changed = True

        for r, c in marked_zero:
            if r not in non_marked_row and c in marked_cols:
                non_marked_row.append(r)
                changed = True

    marked_rows = list(set(range(mat.shape[0])) - set(non_marked_row))
    return marked_zero, marked_rows, list(marked_cols)

def adjust_matrix(mat, cover_rows, cover_cols):
    uncovered_values = [
        mat[i][j] for i in range(mat.shape[0]) if i not in cover_rows
        for j in range(mat.shape[1]) if j not in cover_cols
    ]
    min_val = min(uncovered_values)
    
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if i not in cover_rows and j not in cover_cols:
                mat[i][j] -= min_val
            elif i in cover_rows and j in cover_cols:
                mat[i][j] += min_val
    return mat

def hungarian_algorithm(mat):
    mat = mat.copy()
    for i in range(mat.shape[0]):
        mat[i] -= np.min(mat[i])
    for j in range(mat.shape[1]):
        mat[:, j] -= np.min(mat[:, j])

    while True:
        ans_pos, marked_rows, marked_cols = mark_matrix(mat)
        if len(ans_pos) == mat.shape[0]:
            return ans_pos
        mat = adjust_matrix(mat, marked_rows, marked_cols)

def ans_calculation(original, pos):
    total = sum(original[r][c] for r, c in pos)
    return total

def main():
    config = configparser.ConfigParser()
    config.read("hungarian.ini")
    input_file = config["hungarian"]['input']

    matrix = load_matrix(input_file)
    profit_matrix = np.array(matrix)
    max_val = np.max(profit_matrix)
    cost_matrix = max_val - profit_matrix

    start_time = time.time()
    ans_pos = hungarian_algorithm(cost_matrix)
    elapsed = time.time() - start_time

    ans_pos.sort()
    for pos in ans_pos:
        print(pos)
    total = ans_calculation(profit_matrix, ans_pos)
    print(f"Результат: {total}")
    print(f"Время выполнения: {elapsed:.6f} сек")

if __name__ == "__main__":
    main()
