"""Текстовое описание графа на языке Mermaid (этап 5)."""

HEADER = "graph TD"


def describe(graph):
    """Построить Mermaid-описание рёбер графа."""
    lines = [HEADER]
    for node in sorted(graph):
        for dep in sorted(graph[node] or []):
            lines.append("    %s-->%s" % (node, dep))
    return "\n".join(lines)
