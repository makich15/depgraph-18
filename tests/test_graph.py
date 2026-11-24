"""Тесты поиска в глубину с рекурсией (этап 3)."""

import os
import unittest

from depgraph.graph import (
    dfs_recursive,
    is_ancestor,
    load_test_repo,
    trace_cycle,
)

HERE = os.path.dirname(os.path.abspath(__file__))


def data(name):
    """Путь к файлу тестового репозитория."""
    return os.path.join(HERE, "testdata", name)


def getter(graph):
    """Зависимости вершины из словаря."""

    def get_deps(node):
        """Вернуть список зависимостей вершины."""
        return graph.get(node, [])

    return get_deps


def make_skip(needle):
    """Построить проверку подстроки фильтра для имён пакетов."""

    def skip(name):
        """Проверить, что имя содержит подстроку."""
        return needle in name

    return skip


class TestLoad(unittest.TestCase):
    """Чтение тестового файла в словарь смежности."""

    def test_chain(self):
        """Линейная цепочка читается полностью."""
        graph = load_test_repo(data("chain.txt"))
        self.assertEqual(graph, {"A": ["B"], "B": ["C"], "C": []})


class TestDfs(unittest.TestCase):
    """Обход в глубину с рекурсией."""

    def test_chain_order(self):
        """Цепочка обходится по порядку."""
        graph = load_test_repo(data("chain.txt"))
        order, cycles = dfs_recursive("A", getter(graph))
        self.assertEqual(order, ["A", "B", "C"])
        self.assertEqual(cycles, [])

    def test_cycle_found(self):
        """Цикл находится и обход завершается."""
        graph = load_test_repo(data("cycle.txt"))
        order, cycles = dfs_recursive("A", getter(graph))
        self.assertEqual(sorted(order), ["A", "B", "C"])
        self.assertEqual(len(cycles), 1)
        self.assertEqual(cycles[0][0], cycles[0][-1])

    def test_depth_limit(self):
        """Глубина ограничивает обход."""
        graph = load_test_repo(data("branch.txt"))
        order, _ = dfs_recursive("A", getter(graph), max_depth=1)
        self.assertEqual(order, ["A", "B", "C"])

    def test_filter(self):
        """Пакеты с подстрокой пропускаются."""
        graph = load_test_repo(data("branch.txt"))
        order, _ = dfs_recursive("A", getter(graph),
                                 skip=make_skip("B"))
        self.assertNotIn("B", order)

    def test_trace(self):
        """Путь цикла восстанавливается по предкам."""
        parent = {"A": None, "B": "A", "C": "B"}
        self.assertEqual(trace_cycle(parent, "C", "A"),
                         ["A", "B", "C", "A"])

    def test_ancestor(self):
        """Предок находится по цепочке родителей."""
        parent = {"A": None, "B": "A", "C": "B"}
        self.assertTrue(is_ancestor(parent, "C", "A"))
        self.assertFalse(is_ancestor(parent, "A", "C"))


if __name__ == "__main__":
    unittest.main()
