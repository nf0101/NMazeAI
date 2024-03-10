from collections import deque


def is_valid_move(maze, row, col):
    return len(maze.grid) > row >= 0 == maze.grid[row][col] and 0 <= col < len(maze.grid[0])


def bfs(maze):
    queue = deque([maze.start])
    visited = {maze.start}
    predecessors = {}
    while queue:
        current_row, current_col = queue.popleft()

        # Verifica se abbiamo raggiunto la fine
        if (current_row, current_col) == maze.end:
            path = reconstruct_path(predecessors, maze.start, maze.end)
            print(f"Uscita trovata: {maze.end}")
            print(path)
            print(f"Visited cells BFS: {len(visited)}")
            return True

        # Genera le mosse possibili (su, giù, sinistra, destra)
        moves = [(current_row - 1, current_col),  # su
                 (current_row + 1, current_col),  # giù
                 (current_row, current_col - 1),  # sinistra
                 (current_row, current_col + 1)]  # destra

        for move in moves:
            next_row, next_col = move

            # Verifica se la mossa è valida e non è stata visitata
            if is_valid_move(maze, next_row, next_col) and (next_row, next_col) not in visited:
                queue.append((next_row, next_col))
                visited.add((next_row, next_col))
                predecessors[(next_row, next_col)] = (current_row, current_col)

    # Se la coda si svuota senza trovare l'uscita
    return None


def dfs(maze):
    stack = [maze.start]
    visited = {maze.start}
    predecessors = {}

    while stack:
        current_row, current_col = stack.pop()

        # Verifica se abbiamo raggiunto la fine
        if (current_row, current_col) == maze.end:
            path = reconstruct_path(predecessors, maze.start, maze.end)
            print(f"Uscita trovata: {maze.end}")
            print(path)
            print(f"Visited cells DFS: {len(visited)}")
            return True

        # Genera le mosse possibili (su, giù, sinistra, destra)
        moves = [(current_row - 1, current_col),  # su
                 (current_row + 1, current_col),  # giù
                 (current_row, current_col - 1),  # sinistra
                 (current_row, current_col + 1)]  # destra

        for move in moves:
            next_row, next_col = move

            # Verifica se la mossa è valida e non è stata visitata
            if is_valid_move(maze, next_row, next_col) and (next_row, next_col) not in visited:
                stack.append((next_row, next_col))
                visited.add((next_row, next_col))
                predecessors[(next_row, next_col)] = (current_row, current_col)

    # Se lo stack si svuota senza trovare l'uscita
    return None

def reconstruct_path(predecessors, start, end):
    path = [end]
    current = end

    while current != start:
        current = predecessors[current]
        path.insert(0, current)

    return path
