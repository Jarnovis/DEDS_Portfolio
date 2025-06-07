import random

class maze:
    @staticmethod
    def generate_random_maze(values):
        def count_paths(grid, start, end, max_paths=3, max_depth=200):
            path_count = 0

            def dfs(x, y, visited, depth):
                nonlocal path_count # path_count vanuit functie aanpassen

                if (x, y) == end:
                    path_count += 1
                    return

                if path_count >= max_paths or depth >= max_depth:
                    return

                # Alle directies proberen
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy  # Nieuwe positie berekenen

                    # Geldigd pad
                    if (0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and
                        (grid[ny][nx] == 0 or grid[ny][nx] == 4) and (nx, ny) not in visited):

                        visited.add((nx, ny))          # Positie is bezocht
                        dfs(nx, ny, visited, depth + 1)  # Nieuwe pad mogelijkheden berekenen
                        visited.remove((nx, ny))       # Positie uit bezocht lijst halen, om nieuwe paden te verkennen

            visited = set()          # Set om bezochte posities bij te houden
            visited.add(start) 
            dfs(start[0], start[1], visited, 0)  # Start Depth-First Search 

            return path_count

        # Zorgen dat de start paden vrij zijn
        def open_neighbors(grid, pos, directions):
            x, y = pos
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < values["width"] and 0 <= ny < values["height"]:
                    grid[ny][nx] = 0

        # Creeëren doolhoven
        for attempt in range(values["max_attempts"]):
            # Buitenste randen creeëren
            grid = [[1 if x == 0 or y == 0 or x == values["width"] - 1 or y == values["height"] - 1 else 0
                     for x in range(values["width"])] for y in range(values["height"])]

            # Muren toevoegen
            for y in range(1, values["height"] - 1):
                for x in range(1, values["width"] - 1):
                    if random.random() < values["wall_density"]:
                        grid[y][x] = 1

            start = (1, 1)
            end = (values["width"] - 2, values["height"] - 2)
            grid[start[1]][start[0]] = 0
            grid[end[1]][end[0]] = 0

            open_neighbors(grid, start, [(1, 0), (0, 1)])
            open_neighbors(grid, end, [(-1, 0), (0, -1)])

            placed = 0
            
            # Vallen plaatsen
            while placed <= values["traps"]:
                random_y = random.randint(0, values["height"] - 1)
                random_x = random.randint(0, values["width"] - 1)
                if grid[random_y][random_x] == 0:
                    grid[random_y][random_x] = 4
                    placed += 1

            if count_paths(grid, start, end, max_paths=values["min_paths"]) >= values["min_paths"]:
                grid[start[1]][start[0]] = 2
                grid[end[1]][end[0]] = 3
                return grid

        raise ValueError("Failed to generate a maze with the required number of paths.")
