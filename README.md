# Алгоритмы на графах — Исследование и Реализация

## 📌 Описание проекта

Данный проект посвящён реализации и исследованию классических алгоритмов теории графов. Включает:

- Генератор графов различных типов.
- Реализацию алгоритмов поиска путей, потоков, остовных деревьев и других задач.
- Гибкую работу с конфигурациями и CSV-форматом.
- Оптимизацию с помощью Numba и поддержку больших графов.

---

## 📐 Генерация графов

### 🧰 Модуль генерации: `graph_generator.py`

Позволяет создавать графы следующих типов по параметрам, указанным в конфигурационном файле:

| Тип графа          | Поддержка                              |
|--------------------|----------------------------------------|
| Обычные            | Ориентированные / неориентированные    |
| Взвешенные         | Случайные веса на рёбрах               |
| Транспортные сети  | С источником и стоком                  |
| Двудольные         | Разделение вершин на две группы        |

### 🔧 Пример конфигурационного файла `graph.ini`:

```ini
[Graph]
oriented_or_not = directed  ; Тип графа: directed / undirected / bipartite / flow
top = 10                    ; Количество вершин
edges = 20                  ; Количество рёбер
rib_weight = 20             ; Максимальная длина пути ребра
filename = test_graph.csv   ; Имя файла вывода
```

## Реализованные алгоритмы

### 🔁 Алгоритм Диница (Dinic)
- **Тип задачи**: Нахождение максимального потока в транспортной сети.
- **Описание**: Использует уровневую сеть и блокирующие потоки. Подходит для больших и разреженных графов.
- **Формат входных данных**: Матрица смежности из файла CSV, содержащая пропускные способности.
- **Результат**: Максимальный поток и пути с соответствующими потоками.

### 🧠 Алгоритм Флойда–Уоршелла (Floyd-Warshall)
- **Тип задачи**: Все пары кратчайших путей.
- **Описание**: Динамическое программирование для поиска кратчайших путей между всеми парами вершин.
- **Оптимизация**: Использована библиотека `numba` для ускорения.
- **Результат**: Матрица кратчайших расстояний и восстановленный путь между указанными вершинами.

### 🧮 Венгерский алгоритм (Hungarian)
- **Тип задачи**: Задача о назначениях (минимизация/максимизация прибыли).
- **Описание**: Комбинаторный алгоритм для нахождения оптимального распределения ресурсов.
- **Особенности**: Поддержка как стоимостных, так и прибыльных матриц.
- **Результат**: Назначения и суммарная эффективность.

### 🔁 Алгоритм Косарайю (Kosaraju)
- **Тип задачи**: Поиск компонент сильной связности в ориентированном графе.
- **Описание**: Два прохода DFS — один для упорядочивания, второй по транспонированному графу.
- **Результат**: Список компонент сильной связности и максимальная по размеру компонента.

### 🌉 Алгоритм Краскала (Kruskal)
- **Тип задачи**: Нахождение минимального остовного дерева.
- **Описание**: Жадный алгоритм, использующий сортировку рёбер и систему непересекающихся множеств (Union-Find).
- **Результат**: Список рёбер MST и его суммарный вес.

### 🔍 DFS (Поиск в глубину)
- Поиск путей и обход компонент связности
- Используется также в Kosaraju

### 🌐 BFS (Поиск в ширину)
- Поиск кратчайших путей в невзвешенных графах
- Используется в алгоритме Dinic для построения уровневой сети
---

## Формат входных данных

Все алгоритмы используют входные данные в виде `.csv` файлов. Формат различается в зависимости от алгоритма:

- **Dinic / Kruskal / Kosaraju**: `i;j;w;i;j;w;...` — соседи и веса.
- **Floyd-Warshall / Hungarian**: прямоугольные таблицы или списки смежности.

Имена входных файлов и параметры работы указываются в соответствующих `.ini` файлах:
```ini
[dinic]
input = input_dinic
output = output_dinic
```

## 🎓 Примечание
Данный код был написан в образовательных целях и предназначен для изучения алгоритмов теории графов, их реализации и анализа.
