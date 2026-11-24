"""Тесты разбора и проверки параметров (этап 1)."""

import unittest

from depgraph.cli import (
    ConfigError,
    check_filter,
    format_params,
    parse_depth,
    parse_flag,
    validate,
)


def raw(**over):
    """Набор сырых параметров с разумными значениями."""
    base = {
        "package": "A",
        "repo": "https://example.com",
        "test_mode": "off",
        "version": "1.0.0",
        "max_depth": "0",
        "filter": "",
    }
    base.update(over)
    return base


class TestParseFlag(unittest.TestCase):
    """Разбор флага тестового режима."""

    def test_on_values(self):
        """Значения on/true/1 дают истину."""
        for text in ("on", "true", "1", "ON"):
            self.assertTrue(parse_flag(text))

    def test_off_values(self):
        """Значения off/false/0 дают ложь."""
        for text in ("off", "false", "0"):
            self.assertFalse(parse_flag(text))

    def test_bad_value(self):
        """Мусор во флаге даёт ошибку настроек."""
        with self.assertRaises(ConfigError):
            parse_flag("maybe")


class TestParseDepth(unittest.TestCase):
    """Разбор максимальной глубины."""

    def test_zero(self):
        """Ноль означает отсутствие предела."""
        self.assertEqual(parse_depth("0"), 0)

    def test_number(self):
        """Положительное число принимается."""
        self.assertEqual(parse_depth("3"), 3)

    def test_bad(self):
        """Текст и отрицательные числа отклоняются."""
        with self.assertRaises(ConfigError):
            parse_depth("много")
        with self.assertRaises(ConfigError):
            parse_depth("-1")


class TestValidate(unittest.TestCase):
    """Проверка набора параметров целиком."""

    def test_defaults(self):
        """Пустые версия и фильтр допустимы."""
        settings = validate(raw())
        self.assertEqual(settings["version"], "1.0.0")
        self.assertIsNone(settings["filter"])

    def test_empty_package(self):
        """Пустое имя пакета запрещено."""
        with self.assertRaises(ConfigError):
            validate(raw(package="   "))

    def test_filter_too_long(self):
        """Слишком длинный фильтр отклоняется."""
        with self.assertRaises(ConfigError):
            validate(raw(filter="x" * 65))

    def test_format(self):
        """Вывод настроек идёт строками ключ-значение."""
        text = format_params(validate(raw()))
        self.assertIn("package=A", text)
        self.assertIn("max_depth=0", text)

    def test_check_filter(self):
        """Пустой фильтр превращается в отсутствие."""
        self.assertIsNone(check_filter(None))


if __name__ == "__main__":
    unittest.main()
