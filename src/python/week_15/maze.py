import random

class maze:
    @staticmethod
    def generate_maze(width=20, height=20, min_splits=5):
        if width % 2 == 0:
            width -= 1
        if height % 2 == 0:
            height -= 1

        while True:
            grid = [[1 for _ in range(width)] for _ in range(height)]
            start_x, start_y = 1, 1
            grid[start_y][start_x] = 0
            stack = [(start_x, start_y)]
            directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]

            while stack:
                x, y = stack[-1]
                random.shuffle(directions)
                carved = False

                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 1 <= nx < width - 1 and 1 <= ny < height - 1 and grid[ny][nx] == 1:
                        grid[ny][nx] = 0
                        grid[y + dy // 2][x + dx // 2] = 0
                        stack.append((nx, ny))
                        carved = True
                        break

                if not carved:
                    stack.pop()

            grid[1][1] = 2
            grid[height - 2][width - 2] = 3

            splits = 0
            for y in range(1, height - 1):
                for x in range(1, width - 1):
                    if grid[y][x] == 0:
                        open_neighbors = 0
                        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                            if grid[y + dy][x + dx] == 0:
                                open_neighbors += 1
                        if open_neighbors >= 3:
                            splits += 1

            if splits >= min_splits:
                break

        return grid
