"""Обратные зависимости пакета (этап 4).

Обратные зависимости — пакеты, которые зависят от данного
(прямо или через цепочку). Граф обращается, затем используется
тот же поиск в глубину с рекурсией, что на этапе 3.
"""

from depgraph.graph import dfs_recursive


def invert(graph):
    """Построить обратный граф: ребро ведёт к зависимым."""
    flipped = {}
    for node, deps in graph.items():
        flipped.setdefault(node, [])
        for dep in deps or []:
            flipped.setdefault(dep, []).append(node)
    return flipped


def reverse_deps(graph, target, max_depth=0, skip=None):
    """Все пакеты, зависящие от целевого (сам целевой первый)."""
    flipped = invert(graph)
    if target not in flipped:
        return []
    order, _ = dfs_recursive(target, flipped.get, max_depth, skip)
    return order
