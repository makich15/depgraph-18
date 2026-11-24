"""Разбор и проверка опций командной строки (этап 1).

Параметры: имя пакета, адрес репозитория или путь к файлу,
режим тестового репозитория, версия пакета, максимальная
глубина анализа, подстрока для фильтрации пакетов.
"""

import argparse
import os


MAX_FILTER_LENGTH = 64

TEST_MODES = ("on", "off", "true", "false", "1", "0")


class ConfigError(Exception):
    """Ошибка в значениях параметров."""


def str_or_none(value):
    """Пустую строку превратить в отсутствие значения."""
    if value is None or value == "":
        return None
    return value


def parse_flag(raw):
    """Разобрать флаг on/off/true/false/1/0."""
    text = raw.strip().lower()
    if text in ("on", "true", "1"):
        return True
    if text in ("off", "false", "0"):
        return False
    raise ConfigError("флаг должен быть on/off, true/false или 1/0")


def parse_depth(raw):
    """Разобрать глубину: целое число не меньше нуля."""
    try:
        depth = int(raw)
    except (TypeError, ValueError):
        raise ConfigError("глубина должна быть целым числом")
    if depth < 0:
        raise ConfigError("глубина не может быть отрицательной")
    return depth


def check_filter(needle):
    """Проверить подстроку фильтра."""
    if needle is None:
        return None
    if len(needle) > MAX_FILTER_LENGTH:
        raise ConfigError("фильтр длиннее 64 символов")
    return needle


def parse_args(argv=None):
    """Разобрать опции командной строки в словарь."""
    parser = argparse.ArgumentParser(
        description="Граф зависимостей пакетов NuGet (вариант 18)"
    )
    parser.add_argument("--package", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--test-mode", default="off")
    parser.add_argument("--version", default="")
    parser.add_argument("--max-depth", default="0")
    parser.add_argument("--filter", default="")
    args = parser.parse_args(argv)
    return {
        "package": args.package,
        "repo": args.repo,
        "test_mode": args.test_mode,
        "version": args.version,
        "max_depth": args.max_depth,
        "filter": args.filter,
    }


def check_package(name):
    """Имя пакета обязано быть непустым."""
    if not name or not name.strip():
        raise ConfigError("пустое имя пакета")
    return name.strip()


def check_repo(path, test_mode):
    """Путь к файлу обязан существовать в тестовом режиме."""
    if test_mode and not os.path.isfile(path):
        raise ConfigError("файл репозитория не найден: " + path)
    return path


def check_version(version):
    """Версия может быть пустой (тогда берётся свежая)."""
    return version.strip()


def validate(raw):
    """Проверить все параметры, вернуть готовые настройки."""
    test_mode = parse_flag(raw["test_mode"])
    package = check_package(raw["package"])
    repo = check_repo(raw["repo"], test_mode)
    version = check_version(raw["version"])
    depth = parse_depth(raw["max_depth"])
    needle = check_filter(str_or_none(raw["filter"]))
    return {
        "package": package,
        "repo": repo,
        "test_mode": test_mode,
        "version": version,
        "max_depth": depth,
        "filter": needle,
    }


def format_params(settings):
    """Отформатировать настройки строками ключ-значение."""
    lines = []
    for key in ("package", "repo", "test_mode", "version",
                "max_depth", "filter"):
        lines.append("%s=%s" % (key, settings[key]))
    return "\n".join(lines)


def main(argv=None):
    """Точка входа: параметры, затем прямые зависимости (этап 2)."""
    try:
        settings = validate(parse_args(argv))
    except ConfigError as err:
        print("ошибка: %s" % err)
        return 2
    print(format_params(settings))
    return 0
