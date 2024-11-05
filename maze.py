from tkinter import Tk, BOTH, Canvas
import time
import random 

                        ##############
                        # Window Class #
                        ##############
#Description: 
# This is where most of the main widget methods and functions are established 
# root, title, protocol / close, canvas, and the beginnings of draw_line
#  
class Window:
    def __init__(self, width, height):
        self.root =  Tk() # root is the base of the widget and application
        self.root.title("Maze Runner!") # Name your window when running 
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        # .protocol is how we close the window. the .close method houses the logic 

        # Create the canvas that you will draw on, notice it takes width and height from the constructor
        self.canvas = Canvas(self.root, bg="white", width = width, height = height)
        self.canvas.pack(fill=BOTH, expand=1) # Instead of the grid system, we'll simply pack the canvas for use 

        # By default, the class is set to a not running state. We'll rely on other methods to run the program
        # We do this so we can control the closure of the window. 
        self.is_running = False 
    
    def redraw(self):
        self.root.update()
        self.root.update_idletasks()

    def wait_for_close(self): # This method keeps the application running until you call the close method
        self.is_running = True 
        while self.is_running:
            self.redraw()
        print("Closing Application...")

    def close(self): # This method controls closing the application once the window is closed by clicking red X
        # The close method is called in the constructor of Window
        self.is_running = False 
        self.root.destroy()

    def draw_line(self, line, fill_color="black"):
         # this method calls the .draw method to draw on your canvas. You will call draw_line in your main to begin drawing 
         line.draw(self.canvas, fill_color)

                        ##############
                        # Point Class #
                        ##############

# Description:
# Establish where/what point  you want to begin drawing

class Point: 
    def __init__(self, x, y):
        self.x = x
        self.y = y

                        ##############
                        # Line Class #
                        ##############

# Description: 
# This class determines what points your cursor will move to in 
# order to draw 

class Line: 
    def __init__(self, point_one, point_two):
        self.point_one = point_one
        self.point_two = point_two

    def draw(self, canvas, fill_color="black"): 
        canvas.create_line(self.point_one.x, self.point_one.y, self.point_two.x, self.point_two.y, fill = fill_color, width=2)

                        ##############
                        # Cell Class #
                        ##############

# Description
# The Cell class determines if a cell has a wall, draws lines in and around a cell
# and informs you if you've gone through a path that has a wall, or doesn't
# by using different line colors. 

class Cell: 
    def __init__(self, window = None):
        self._x1 = None
        self._x2 = None 
        self._y1 = None 
        self._y2 = None
        self.has_left_wall = True 
        self.has_right_wall = True 
        self.has_top_wall = True 
        self.has_bottom_wall = True
        self.visited = False 
        self._window = window 

    def draw(self, x1, y1, x2, y2): 
        if self._window is None:
            return 
        self._x1 = x1
        self._x2 = x2 
        self._y1 = y1 
        self._y2 = y2
        if self.has_left_wall: 
            line = Line(Point(x1, y1), Point(x1, y2))
            self._window.draw_line(line)
        else: 
            line = (Line(Point(x1, y1), Point(x1, y2)))
            self._window.draw_line(line, fill_color = "white")
            
        if self.has_right_wall: 
            line = Line(Point(x2, y1), Point(x2, y2))
            self._window.draw_line(line)
        else: 
            line = (Line(Point(x2, y1), Point(x2, y2)))
            self._window.draw_line(line, fill_color = "white")

        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._window.draw_line(line)
        else: 
            line = (Line(Point(x1, y1), Point(x2, y1)))
            self._window.draw_line(line, fill_color = "white")

        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._window.draw_line(line)
        else: 
            line = (Line(Point(x1, y2), Point(x2, y2)))
            self._window.draw_line(line, fill_color = "white")
        
    def draw_move(self, to_cell, undo=False):
        half_lengthx = abs(self._x2 - self._x1) / 2 
        half_lengthy = abs(self._y2 - self._y1) / 2
        current_x = half_lengthx + self._x1
        current_y = half_lengthy + self._y1

        target_halfx = abs(to_cell._x2 - to_cell._x1) / 2
        target_halfy = abs(to_cell._y2 - to_cell._y1) / 2
        target_x = target_halfx + to_cell._x1
        target_y = target_halfy + to_cell._y1

        if undo: 
            color = "gray"
        else: 
            color = "red"
            
        line = Line(Point(current_x, current_y), Point(target_x, target_y))
        self._window.draw_line(line, fill_color = color)

                        ##############
                        # Maze Class #
                        ##############

# Description
# This holds all the cells in the maze
# in a 2-dimensional grid, AKA a list of lists. 

class Maze: 
    def __init__(self, x1, y1, num_rows, num_cols,
        cell_size_x, cell_size_y, win = None, seed = None):
        self._cells = [] 
        self.x1 = x1 
        self.y1 = y1 
        self.num_rows = num_rows 
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x 
        self.cell_size_y = cell_size_y 
        self.win = win 
        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        if self.num_rows <= 0 or self.num_cols <= 0:
            raise ValueError("cells and rows need to be greater than 0")
        for col in range(self.num_cols):
            columns = [] 
            for row in range(self.num_rows):
                columns.append(Cell(self.win))
            self._cells.append(columns)
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                self._draw_cell(col, row)

    def _draw_cell(self, i, j):
        if self.win is None:
            return 
        x1 = self.x1 + i * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y 
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y

        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()
    
    def _break_entrance_and_exit(self): 
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)

        self._cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False 
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True 

        while True: 
            directions = []

            # Left 
            if i > 0 and not self._cells[i - 1][j].visited:
                directions.append((i - 1, j))
            
            # Right 
            if i < self.num_cols - 1 and not self._cells[i + 1][j].visited: 
                directions.append((i + 1, j))

            # Up 
            if j > 0 and not self._cells[i][j - 1].visited: 
                directions.append((i, j - 1))
            
            # Down 
            if j < self.num_rows - 1 and not self._cells[i][j + 1].visited:
                directions.append((i, j + 1))

            if len(directions) == 0: 
                self._draw_cell(i, j)
                return 

            direction_index = random.randrange(len(directions))
            next_index = directions[direction_index]

            # Right 
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False 
                self._cells[i + 1][j].has_left_wall = False 

            # Left 
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False 
            
            # Down 
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False 

            # Up 
            if next_index[1] == j - 1: 
                self._cells[i][j].has_top_wall = False 
                self._cells[i][j - 1].has_bottom_wall = False 

            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                self._cells[col][row].visited = False

    def solve(self):
        return self._solve_r(i=0, j=0)

    def _solve_r(self, i, j):
        #Step 1 Call the animate method 
        self._animate()
        
        # Step 2: set current cell to visited 
        self._cells[i][j].visited = True 

        # step 3: This condition checks for the bottom right corner of the maze. 
        if i == self.num_cols - 1 and j == self.num_rows - 1: 
            return True 
        
 # Step 4: For each direction, we check if a move is possible, make the move, and recursively solve the maze.
    
    # Right: Check if there's a cell to the right, no wall, and it hasn't been visited
        if i < self.num_cols - 1 and not self._cells[i + 1][j].visited and not self._cells[i][j].has_right_wall:
            self._cells[i][j].draw_move(self._cells[i + 1][j])  # Draw move to the right
            if self._solve_r(i + 1, j):  # Recursively try to solve from the right cell
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], undo=True)  # Undo the move if it didn't lead to a solution

        # Left: Check if there's a cell to the left, no wall, and it hasn't been visited
        if i > 0 and not self._cells[i - 1][j].visited and not self._cells[i][j].has_left_wall:
            self._cells[i][j].draw_move(self._cells[i - 1][j])  # Draw move to the left
            if self._solve_r(i - 1, j):  # Recursively try to solve from the left cell
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], undo=True)  # Undo the move if it didn't lead to a solution

        # Down: Check if there's a cell below, no wall, and it hasn't been visited
        if j < self.num_rows - 1 and not self._cells[i][j + 1].visited and not self._cells[i][j].has_bottom_wall:
            self._cells[i][j].draw_move(self._cells[i][j + 1])  # Draw move downwards
            if self._solve_r(i, j + 1):  # Recursively try to solve from the below cell
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], undo=True)  # Undo the move if it didn't lead to a solution

        # Up: Check if there's a cell above, no wall, and it hasn't been visited
        if j > 0 and not self._cells[i][j - 1].visited and not self._cells[i][j].has_top_wall:
            self._cells[i][j].draw_move(self._cells[i][j - 1])  # Draw move upwards
            if self._solve_r(i, j - 1):  # Recursively try to solve from the above cell
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], undo=True)  # Undo the move if it didn't lead to a solution

        # Part of step 3: False if the bottom right corner is not visited 
        return False  

    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(.01)