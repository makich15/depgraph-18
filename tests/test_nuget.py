"""Тесты прямых зависимостей из NuGet (этап 2)."""

import unittest

from depgraph.nuget import (
    direct_dependencies,
    find_package_id,
    known_versions,
)

SEARCH = {"data": [{"id": "Demo", "version": "2.0.0"}]}
VERSIONS = {"versions": ["1.0.0", "2.0.0"]}
LEAF = {"dependencyGroups": [
    {"targetFramework": "net8.0",
     "dependencies": [{"id": "DepA"}, {"id": "DepB"}]},
    {"targetFramework": "",
     "dependencies": [{"id": "DepA"}, {"id": "BuildOnly"}]},
]}


def fake_opener(mapping):
    """Подменить сеть словарём адрес-ответ."""

    def opener(url):
        for key, value in mapping.items():
            if url.startswith(key):
                return value
        return {}

    return opener


def opener():
    """Приспособление с пакетом Demo версии 2.0.0."""
    return fake_opener({
        "https://azuresearch": SEARCH,
        "https://api.nuget.org/v3-flatcontainer/demo/index.json":
            VERSIONS,
        "https://api.nuget.org/v3/registration5-gz-semver2/demo/":
            LEAF,
    })


class TestNuget(unittest.TestCase):
    """Проверки поиска пакета и чтения зависимостей."""

    def test_find_id(self):
        """Поиск возвращает точный идентификатор."""
        found = find_package_id("demo", opener())
        self.assertEqual(found, "Demo")

    def test_missing_package(self):
        """Неизвестный пакет даёт ошибку."""
        with self.assertRaises(ValueError):
            find_package_id("demo", fake_opener({}))

    def test_versions(self):
        """Список версий читается из контейнера."""
        versions = known_versions("Demo", opener())
        self.assertEqual(versions, ["1.0.0", "2.0.0"])

    def test_direct(self):
        """Сквозной разбор: пакет, версия, зависимости."""
        names = direct_dependencies("Demo", "2.0.0", opener=opener())
        self.assertIn("DepA", names)
        self.assertIn("DepB", names)

    def test_unknown_version(self):
        """Неизвестная версия даёт ошибку."""
        with self.assertRaises(ValueError):
            direct_dependencies("Demo", "9.9.9", opener=opener())


if __name__ == "__main__":
    unittest.main()
