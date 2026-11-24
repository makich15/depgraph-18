"""Прямые зависимости пакета из репозитория NuGet (этап 2).

Только стандартная библиотека: urllib для HTTP, json для разбора.
Менеджеры пакетов и сторонние библиотеки не используются.
"""

import json
import urllib.request

HTTP_TIMEOUT = 20
USER_AGENT = "depgraph-18/1.0 (student project)"

SEARCH_PAGE_SIZE = 20
SEARCH_TEMPLATE = ("https://azuresearch-usnc.nuget.org/query"
                   "?q=%s&prerelease=false&take=%d")
FLAT_TEMPLATE = "https://api.nuget.org/v3-flatcontainer/%s/index.json"
LEAF_TEMPLATE = ("https://api.nuget.org/v3/registration5-gz-semver2/"
                 "%s/%s.json")


def fetch_json(url, opener=None):
    """Скачать JSON по адресу и разобрать в словарь."""
    if opener is not None:
        return opener(url)
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def find_package_id(name, opener=None):
    """Уточнить точный идентификатор пакета через поиск."""
    url = SEARCH_TEMPLATE % (name.lower(), SEARCH_PAGE_SIZE)
    answer = fetch_json(url, opener)
    for item in answer.get("data", []):
        if item.get("id", "").lower() == name.lower():
            return item.get("id")
    raise ValueError("пакет не найден: %s" % name)


def known_versions(package_id, opener=None):
    """Все опубликованные версии пакета списком."""
    url = FLAT_TEMPLATE % package_id.lower()
    answer = fetch_json(url, opener)
    return [v for v in answer.get("versions", []) if v]


def leaf_url(package_id, version):
    """Адрес страницы версии в каталоге регистрации."""
    return LEAF_TEMPLATE % (package_id.lower(), version.lower())


def direct_dependencies(package, version, repo=None, opener=None):
    """Прямые зависимости указанной версии пакета.

    Учитываются обычные (не dev, не сборка) и не опциональные
    зависимости: именно они нужны пакету всегда.
    """
    package_id = find_package_id(package, opener)
    if version not in known_versions(package_id, opener):
        raise ValueError("версия не найдена: %s" % version)
    answer = fetch_json(leaf_url(package_id, version), opener)
    names = []
    for group in answer.get("dependencyGroups", []):
        for dep in group.get("dependencies", []):
            dep_id = dep.get("id")
            if dep_id and dep_id not in names:
                names.append(dep_id)
    return names
