"""Граф зависимостей: поиск в глубину с рекурсией (этап 3).

Вершины тестового репозитория называются большими латинскими
буквами. Циклы находятся и выводятся, обход завершается.
"""

COMMENT_PREFIX = "#"


def load_test_repo(path):
    """Прочитать файл вида 'A: B C' в словарь смежности."""
    graph = {}
    with open(path, encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith(COMMENT_PREFIX):
                continue
            head, _, tail = line.partition(":")
            node = head.strip()
            deps = [d for d in tail.split() if d]
            graph[node] = deps
            for dep in deps:
                graph.setdefault(dep, [])
    return graph


def trace_cycle(parent, node, child):
    """Восстановить путь цикла от потомка к предку."""
    path = [child]
    while node is not None and node != child:
        path.append(node)
        node = parent.get(node)
    path.append(child)
    path.reverse()
    return path


def is_ancestor(parent, node, target):
    """Проверить, что target выше node в дереве обхода."""
    while node is not None:
        if node == target:
            return True
        node = parent.get(node)
    return False


def dfs_collect(node, get_deps, order, parent, cycles, seen,
                max_depth, depth, skip):
    """Рекурсивно обойти достижимые вершины, найти циклы."""
    seen.add(node)
    for child in get_deps(node) or []:
        if skip is not None and skip(child):
            continue
        if child in seen:
            if is_ancestor(parent, node, child):
                found = trace_cycle(parent, node, child)
                key = " ".join(found)
                if key not in seen:
                    seen.add(key)
                    cycles.append(found)
            continue
        if max_depth and depth + 1 > max_depth:
            continue
        parent[child] = node
        order.append(child)
        dfs_collect(child, get_deps, order, parent, cycles, seen,
                    max_depth, depth + 1, skip)


def dfs_recursive(start, get_deps, max_depth=0, skip=None):
    """Обход в глубину с рекурсией, возврат порядка и циклов."""
    if skip is not None and skip(start):
        return [], []
    order = [start]
    cycles = []
    dfs_collect(start, get_deps, order, {start: None}, cycles,
                set(), max_depth, 0, skip)
    return order, cycles
