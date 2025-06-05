import random

class maze:
    @staticmethod
    def generate_random_maze(width=20, height=20, wall_density=0.25, min_paths=2, max_attempts=100, traps=10):
        def count_paths(grid, start, end, max_paths=3, max_depth=200):
            path_count = 0

            def dfs(x, y, visited, depth):
                nonlocal path_count
                if (x, y) == end:
                    path_count += 1
                    return
                if path_count >= max_paths or depth >= max_depth:
                    return
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < width and 0 <= ny < height and
                        (grid[ny][nx] == 0 or grid[ny][nx] == 4) and (nx, ny) not in visited):
                        visited.add((nx, ny))
                        dfs(nx, ny, visited, depth + 1)
                        visited.remove((nx, ny))

            visited = set()
            visited.add(start)
            dfs(start[0], start[1], visited, 0)
            return path_count

        def open_neighbors(grid, pos, directions):
            x, y = pos
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    grid[ny][nx] = 0

        for attempt in range(max_attempts):
            grid = [[1 if x == 0 or y == 0 or x == width - 1 or y == height - 1 else 0
                     for x in range(width)] for y in range(height)]

            for y in range(1, height - 1):
                for x in range(1, width - 1):
                    if random.random() < wall_density:
                        grid[y][x] = 1

            start = (1, 1)
            end = (width - 2, height - 2)
            grid[start[1]][start[0]] = 0
            grid[end[1]][end[0]] = 0

            open_neighbors(grid, start, [(1, 0), (0, 1)])
            open_neighbors(grid, end, [(-1, 0), (0, -1)])

            placed = 0
            while placed <= traps:
                random_y = random.randint(0, height - 1)
                random_x = random.randint(0, width - 1)
                if grid[random_y][random_x] == 0:
                    grid[random_y][random_x] = 4
                    placed += 1

            if count_paths(grid, start, end, max_paths=min_paths) >= min_paths:
                grid[start[1]][start[0]] = 2
                grid[end[1]][end[0]] = 3
                return grid

        raise ValueError("Failed to generate a maze with the required number of paths.")
