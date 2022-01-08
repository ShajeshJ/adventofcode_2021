from libraries.questions import get_question_input


def __navigate_caves(
    node: str, connections: dict[str, list[str]], blacklisted: set[str]
):
    """Recrusive function, which given a set of cave connections, will recursively
    find all possible paths

    :param node: The cave node we're currently at
    :param connections: A dictionary of nodes and all other nodes they can visit
    :param blacklisted: A list of nodes that should no longer be visited
    :return: The list of all paths that navigate from `node` to "end"
    """
    found_paths: list[list[str]] = []

    # If `node` is at "end" already, then there is only one path to "end"
    if node == "end":
        return [["end"]]  # Doubly nested list, because we return list of subpaths

    # Ensure small caves are not revisted in later subpaths
    updated_blacklist = set(blacklisted)
    if node.islower():
        updated_blacklist.add(node)

    # Iterate through all caves connected to `node` and return all subpaths to "end"
    for cave in connections[node]:
        if cave not in blacklisted:
            subpaths = __navigate_caves(cave, connections, updated_blacklist)
            for subpath in subpaths:
                found_paths.append([node] + subpath)

    return found_paths


def part_1():
    connections: dict[str, list[str]] = {}
    for connection_str in get_question_input(12):
        cave_a, cave_b = connection_str.split("-")
        connections.setdefault(cave_a, []).append(cave_b)
        connections.setdefault(cave_b, []).append(cave_a)

    all_paths = __navigate_caves("start", connections, {"start"})
    print(len(all_paths))
