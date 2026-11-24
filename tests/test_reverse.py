"""Тесты обратных зависимостей (этап 4)."""

import os
import unittest

from depgraph.graph import load_test_repo
from depgraph.reverse import invert, reverse_deps

HERE = os.path.dirname(os.path.abspath(__file__))


def data(name):
    """Путь к файлу тестового репозитория."""
    return os.path.join(HERE, "testdata", name)


class TestInvert(unittest.TestCase):
    """Обращение рёбер графа."""

    def test_edges(self):
        """Зависимые становятся потомками зависимости."""
        graph = load_test_repo(data("branch.txt"))
        flipped = invert(graph)
        self.assertIn("A", flipped["B"])
        self.assertIn("A", flipped["C"])
        self.assertIn("B", flipped["D"])
        self.assertIn("C", flipped["D"])


class TestReverse(unittest.TestCase):
    """Поиск пакетов, зависящих от заданного."""

    def test_leaf(self):
        """От листа зависят все пакеты выше."""
        graph = load_test_repo(data("branch.txt"))
        found = reverse_deps(graph, "D")
        self.assertEqual(found[0], "D")
        self.assertEqual(sorted(found), ["A", "B", "C", "D"])

    def test_middle(self):
        """От среднего пакета зависит только верхний."""
        graph = load_test_repo(data("branch.txt"))
        found = reverse_deps(graph, "B")
        self.assertEqual(sorted(found), ["A", "B"])

    def test_unknown(self):
        """Неизвестный пакет даёт пустой список."""
        graph = load_test_repo(data("branch.txt"))
        self.assertEqual(reverse_deps(graph, "Z"), [])


if __name__ == "__main__":
    unittest.main()
