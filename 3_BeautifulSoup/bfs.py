from collections import deque


def bfs(graph: dict, root: str, stop: str) -> (dict, dict):
    """
    Усовершенствованный bfs для поиска кратчайшего пути от root до stop-вершины
    """

    visited, vertices = set(), deque()
    lens, parents = dict(), dict()

    # начальная инициализация - O(|V|)
    for v in graph.keys():
        lens[v] = -1            # нельзя добраться
        parents[v] = -1         # нет родителя

    vertices.append(root)
    visited.add(root)
    lens[root] = 0

    # работа алгоритма - O(|E|)
    while len(vertices) > 0:
        curr_v = vertices.popleft()
        for child in graph[curr_v]:
            if child not in visited:
                parents[child] = curr_v
                lens[child] = lens[curr_v] + 1
                vertices.append(child)
                visited.add(child)

                if child == stop:
                    return lens, parents

    return lens, parents


def get_parent_path(parents: dict, root: str, vertic: str):
    """
    Восстанавливание кратчайшего пути от root до vertic
    """

    v_parents = [vertic]
    if vertic == root:
        return v_parents

    curr_parent = parents[vertic]
    while curr_parent != root:
        v_parents.append(curr_parent)
        curr_parent = parents[curr_parent]
    v_parents.append(root)

    return v_parents[::-1]




