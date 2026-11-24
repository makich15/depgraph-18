"""Тесты Mermaid-описания графа (этап 5)."""

import os
import unittest

from depgraph.graph import load_test_repo
from depgraph.mermaid import describe

HERE = os.path.dirname(os.path.abspath(__file__))


def data(name):
    """Путь к файлу тестового репозитория."""
    return os.path.join(HERE, "testdata", name)


class TestMermaid(unittest.TestCase):
    """Проверка текстового описания графа."""

    def test_frame(self):
        """Описание начинается с graph TD."""
        graph = load_test_repo(data("chain.txt"))
        self.assertTrue(describe(graph).startswith("graph TD"))

    def test_edges(self):
        """Все рёбра присутствуют в виде стрелок."""
        graph = load_test_repo(data("branch.txt"))
        text = describe(graph)
        self.assertIn("A-->B", text)
        self.assertIn("A-->C", text)
        self.assertIn("B-->D", text)
        self.assertIn("C-->D", text)


if __name__ == "__main__":
    unittest.main()
