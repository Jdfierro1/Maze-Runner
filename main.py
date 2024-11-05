from maze import Window, Line, Point, Cell, Maze

def main():

    margin = 50
    num_rows = 20
    num_cols = 25
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows 
    run = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, run)


    maze.solve()
    run.wait_for_close()

main()