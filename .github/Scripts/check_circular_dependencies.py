import os
import re
from collections import defaultdict

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # On sort de .github/Scripts/
CLASS_DEF_REGEX = re.compile(r'\b(class|record)\s+([A-Z][a-zA-Z0-9_]*)')
CLASS_USAGE_REGEX = re.compile(r'\b([A-Z][a-zA-Z0-9_]*)\b')

def get_cs_files():
    for dirpath, _, filenames in os.walk(ROOT_DIR):
        for f in filenames:
            if f.endswith(".cs"):
                yield os.path.join(dirpath, f)

def extract_class_definitions(files):
    class_files = {}
    for path in files:
        with open(path, encoding='utf-8') as f:
            content = f.read()
        match = CLASS_DEF_REGEX.search(content)
        if match:
            class_name = match.group(2)
            class_files[class_name] = path
    return class_files

def build_dependency_graph(files, class_names):
    graph = defaultdict(set)
    for path in files:
        with open(path, encoding='utf-8') as f:
            content = f.read()
        current_class_match = CLASS_DEF_REGEX.search(content)
        if not current_class_match:
            continue
        current_class = current_class_match.group(2)
        used = set(CLASS_USAGE_REGEX.findall(content))
        for other_class in used:
            if other_class in class_names and other_class != current_class:
                graph[current_class].add(other_class)
    return graph

def detect_cycles(graph):
    visited = set()
    stack = []

    def dfs(node):
        if node in stack:
            return stack[stack.index(node):] + [node]
        if node in visited:
            return None
        visited.add(node)
        stack.append(node)
        for neighbor in graph[node]:
            cycle = dfs(neighbor)
            if cycle:
                return cycle
        stack.pop()
        return None

    for node in list(graph): 
        cycle = dfs(node)
        if cycle:
            return cycle
    return None


def main():
    cs_files = list(get_cs_files())
    class_defs = extract_class_definitions(cs_files)
    graph = build_dependency_graph(cs_files, class_defs.keys())
    cycle = detect_cycles(graph)
    if cycle:
        print("❌ Dépendance circulaire détectée :")
        print(" -> ".join(cycle))
        exit(1)
    else:
        print("✅ Aucun cycle détecté.")

if __name__ == "__main__":
    main()
