import time
import heapq
from collections import deque
import random

def dfs(maze, start, goal):
    stack = [start]
    visited = set()
    visited.add(start)

    while stack:
        x, y = stack.pop()
        if (x, y) == goal:
            return True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and
                maze[nx][ny] == 1 and (nx, ny) not in visited):
                visited.add((nx, ny))
                stack.append((nx, ny))
    return False

def bfs(maze, start, goal):
    queue = deque([start])
    visited = set()
    visited.add(start)

    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            return True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and
                maze[nx][ny] == 1 and (nx, ny) not in visited):
                visited.add((nx, ny))
                queue.append((nx, ny))
    return False

def a_star(maze, start, goal):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return True

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if (0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]) and
                maze[neighbor[0]][neighbor[1]] == 1):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return False

def generate_recursive_backtracking_maze(size):
    def carve_passages_iterative(start_x, start_y, maze):
        stack = [(start_x, start_y)]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while stack:
            cx, cy = stack.pop()
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = cx + dx * 2, cy + dy * 2
                if 0 <= nx < size and 0 <= ny < size and maze[nx][ny] == 0:
                    maze[cx + dx][cy + dy] = 1
                    maze[nx][ny] = 1
                    stack.append((nx, ny))

    # Initialize maze with walls
    maze = [[0 for _ in range(size)] for _ in range(size)]
    maze[0][0] = 1  # Start point
    carve_passages_iterative(0, 0, maze)
    maze[size - 1][size - 1] = 1  # End point
    return maze

def is_path_exists(maze, start, goal):
    queue = deque([start])
    visited = set()
    visited.add(start)

    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            return True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and
                maze[nx][ny] == 1 and (nx, ny) not in visited):
                visited.add((nx, ny))
                queue.append((nx, ny))
    return False

def find_disconnected_regions(maze):
    size = len(maze)
    visited = set()
    regions = []

    def dfs_region(x, y, region):
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) not in visited and maze[cx][cy] == 1:
                visited.add((cx, cy))
                region.add((cx, cy))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < size and 0 <= ny < size:
                        stack.append((nx, ny))

    for x in range(size):
        for y in range(size):
            if maze[x][y] == 1 and (x, y) not in visited:
                region = set()
                dfs_region(x, y, region)
                regions.append(region)

    return regions

def connect_regions(maze, regions):
    if len(regions) <= 1:
        return maze

    for i in range(len(regions) - 1):
        region_a = list(regions[i])
        region_b = list(regions[i + 1])
        x1, y1 = region_a[0]
        x2, y2 = region_b[0]

        if x1 == x2:  # Same row
            for y in range(min(y1, y2), max(y1, y2) + 1):
                maze[x1][y] = 1
        elif y1 == y2:  # Same column
            for x in range(min(x1, x2), max(x1, x2) + 1):
                maze[x][y1] = 1
        else:  # Diagonal connection
            for x in range(min(x1, x2), max(x1, x2) + 1):
                maze[x][y1] = 1
            for y in range(min(y1, y2), max(y1, y2) + 1):
                maze[x2][y] = 1

    return maze

def generate_valid_maze(size):
    while True:
        maze = generate_recursive_backtracking_maze(size)
        regions = find_disconnected_regions(maze)
        if len(regions) > 1:
            maze = connect_regions(maze, regions)
        if is_path_exists(maze, (0, 0), (size - 1, size - 1)):
            return maze

def print_maze(maze):
    for row in maze:
        print(" ".join(map(str, row)))

def main_menu():
    print("\nDobrodošli u program za pretragu lavirinta!")
    while True:
        print("\nOdaberite opciju:")
        print("1. Biranje veličine lavirinta")
        print("2. Pokretanje algoritama pretrage")
        print("3. Izlaz iz programa")
        izbor = input("Unesite broj opcije: ")

        if izbor == "1":
            global maze_size
            maze_size = int(input("Unesite veličinu lavirinta (npr. 10, 50, 100): "))
            print(f"Lavirint veličine {maze_size}x{maze_size} je spreman.")
        elif izbor == "2":
            maze = generate_valid_maze(maze_size)
            print("\nGenerisani lavirint:")
            print_maze(maze)
            for algo_name, algo in algorithms.items():
                print(f"Pokrećem {algo_name}...")
                start_time = time.time()
                result = algo(maze, (0, 0), (maze_size-1, maze_size-1))
                end_time = time.time()
                print(f"  {algo_name}: {'Put pronađen' if result else 'Put nije pronađen'} za {end_time - start_time:.6f} sekundi")
        elif izbor == "3":
            print("Hvala što ste koristili program. Doviđenja!")
            break
        else:
            print("Nepoznata opcija. Pokušajte ponovo.")

# Default settings
maze_size = 10

algorithms = {
    "DFS": dfs,
    "BFS": bfs,
    "A*": a_star,
}

if __name__ == "__main__":
    main_menu()
