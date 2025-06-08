import window_normal
import window
import maze
import enviroment
import agent
import msvcrt

values = {
    "width": 12,
    "height": 12,
    "wall_density": 0.15,
    "min_paths": 2,
    "max_attempts": 10,
    "traps": 15
}

grid = maze.maze().generate_random_maze(values)

env = enviroment.enviroment(grid, values)
bot = agent.agent(env)

print("Press y to activate the special style for the game")
key = msvcrt.getch()
kind = key.decode().lower()

if kind.lower() == 'y':
    win = window.window(720, 720, grid, bot)
else:
    win = window_normal.window_normal(720, 720, grid, bot)
win.create()
win.run()