import heapq
import time

class Grid:

    #initializing the grid

    def __init__(self, rows: int, cols: int):

        self.rows = rows

        self.cols = cols

        # all cells are initally set to clean

        self.grid = [['clean' for _ in range(cols)] for _ in range(rows)]



    #Marks a given cell as dirty

    def mark_dirty(self, row: int, col: int):

        if self.is_valid_cell(row, col):

            self.grid[row - 1][col - 1] = 'dirty'

        else:

            raise ValueError("Invalid cell coordinates.")

    

    #Marks a given cell as clean. 

    def mark_clean(self, row: int, col: int):

        if self.is_valid_cell(row, col):

            self.grid[row - 1][col - 1] = 'clean'

        else:

            raise ValueError("Invalid cell coordinates.")

    

    #Bounds checking

    def is_valid_cell(self, row: int, col: int) -> bool:

        row -= 1

        col -= 1

        return 0 <= row < self.rows and 0 <= col < self.cols

    

    #Prints the grid in a readable format

    def display(self):

        for row in self.grid:

            print(" | ".join(row))

        print()



    #Checks all rooms are clean

    def is_all_clean(self) -> bool:

        return all(room == 'clean' for row in self.grid for room in row)





class Agent:

    #Initialize the agent and give it the starting grid

    def __init__(self, grid: Grid, start_position: tuple):

        self.grid = grid

        self.position = start_position

        self.total_cost = 0.0  # Track total action cost

    

    #Move left and add appropriate cost

    def move_left(self):

        row, col = self.position

        if col > 0:

            self.position = (row, col - 1)

            self.total_cost += 1.0

    

    #Move the agent right and add appropriate cost

    def move_right(self):

        row, col = self.position

        if col < self.grid.cols - 1:

            self.position = (row, col + 1)

            self.total_cost += 0.9

    

    #Move hte agent up and add appropriate cost

    def move_up(self):

        row, col = self.position

        if row > 0:

            self.position = (row - 1, col)

            self.total_cost += 0.8

    



    #Move agent down and add appropriate cost

    def move_down(self):

        row, col = self.position

        if row < self.grid.rows - 1:

            self.position = (row + 1, col)

            self.total_cost += 0.7

    

    #Cleans the room and adds appropriate cost

    def suck(self):

        row, col = self.position

        if self.grid.is_dirty(row, col):

            self.grid.mark_clean(row, col)

            self.total_cost += 0.6

    

    def is_goal_reached(self):

        return self.grid.is_all_clean()

    def agent_uniform_cost_search(self, dirty_rooms):
        start_time = time.time()
        moves=0
        generated = 0
        expanded = 0
        for pos in dirty_rooms:
            result, gen, exp = uniform_cost_search(self.grid, self.position, pos)
            moves += len(result) +1
            generated += gen
            expanded += exp
            self.position = result[0][-1]
            self.total_cost += result[1]
            self.grid.mark_clean(self.position[0], self.position[1])
        
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Execution time: {total_time:.6f} seconds")
        print(f"Total number of moves: {moves}")
        print(f"Total number of nodes generated: {generated}")
        print(f"Total number of nodes expanded: {expanded}")
            
    def agent_graph_search(self, dirty_rooms):
        self.total_cost = 0
        start_time = time.time()
        moves=0
        generated = 0
        expanded = 0
        
        for goal in dirty_rooms:
            self.total_cost += .6
            path, gen, exp = self.graph_search(self.position, goal)  # Perform graph search to find the path
            generated += gen
            expanded += exp
            if path:
                moves += len(path)
                i = 0

                #up.8, down.7, left1, right.9, clean.6
                while i < len(path) - 1:
                    if path[i][1] > path[i+1][1]:
                        self.total_cost += 1
                    if path[i][1] < path[i+1][1]:
                        self.total_cost += .9
                    if path[i][0] < path[i+1][0]:
                        self.total_cost += .7
                    if path[i][0] > path[i+1][0]:
                        self.total_cost += .8
                    i += 1

                self.position = path[-1]  # Move to the goal position
                self.grid.mark_clean(self.position[0], self.position[1])  # Clean the room
                
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Execution time: {total_time:.6f} seconds")
        print(f"Total number of moves: {moves}")
        print(f"Total number of nodes generated: {generated}")
        print(f"Total number of nodes expanded: {expanded}")
        
    def agent_IDDFs_Search(self, dirty_rooms):
        start_time = time.time()
        moves=0
        #generated = 0
        expanded = 0
        for room in dirty_rooms:
            path, exp = iddfs(self.grid.grid, self.position, room)
            moves += len(path)
            #generated += gen
            expanded += exp
            self.position = path[-1]
            i = 0
            #up.8, down.7, left1, right.9, clean.6
            while i < len(path) - 1:
                if path[i][1] > path[i+1][1]:
                    self.total_cost += 1
                if path[i][1] < path[i+1][1]:
                    self.total_cost += .9
                if path[i][0] < path[i+1][0]:
                    self.total_cost += .7
                if path[i][0] > path[i+1][0]:
                    self.total_cost += .8
                i += 1
            self.grid.mark_clean(self.position[0], self.position[1])  # Clean the room
            self.total_cost += 0.6
            self.total_cost = round(self.total_cost, 1)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Execution time: {total_time:.6f} seconds")
        print(f"Total number of moves: {moves}")
        global iddfs_generated
        print(f"Total number of nodes generated: {iddfs_generated}")
        print(f"Total number of nodes expanded: {expanded}")

    # Define graph_search
    def graph_search(self, start, goal):
        moves = {
            'Up': (-1, 0, 0.8),
            'Down': (1, 0, 0.7),
            'Left': (0, -1, 1.0),
            'Right': (0, 1, 0.9),
        }
        # Priority queue for weighted graph search (similar to UCS)
        fringe = []
        heapq.heappush(fringe, (0, start))  # (path_cost, position)
        
        generated = 0
        expanded = 0
        
        came_from = {start: None}  # Parent tracking for path reconstruction
        cost_so_far = {start: 0}   # Store the accumulated cost for each position
        closed = set()  # Keep track of visited positions

        while fringe:
            current_cost, node = heapq.heappop(fringe)
            expanded += 1
            
            if node == goal:
                # Reconstruct path by following parent links
                path = []
                while node:
                    path.append(node)
                    node = came_from[node]
                print(list(reversed(path)))
                print("suck")
                return list(reversed(path)), generated, expanded  # Return the path from start to goal

            closed.add(node)  # Mark the node as visited

            # Expand the current node
            for move, (dr, dc, move_cost) in moves.items():
                next_row, next_col = node[0] + dr, node[1] + dc
                next_pos = (next_row, next_col)

                # Check if the next position is within bounds
                if self.grid.is_valid_cell(next_row, next_col) and next_pos not in closed:
                    new_cost = current_cost + move_cost  # Add move cost
                    generated += 1

                    # Only explore this position if it's cheaper to reach it this way
                    if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                        cost_so_far[next_pos] = new_cost
                        heapq.heappush(fringe, (new_cost, next_pos))
                        came_from[next_pos] = node  # Track the path

        return None  # Return None if no path is found


def uniform_cost_search(grid, start, goal):
    # Define movement directions and costs
    moves = {
        'Up': (-1, 0, 0.8),
        'Down': (1, 0, 0.7),
        'Left': (0, -1, 1.0),
        'Right': (0, 1, 0.9),
    }
    
    generated = 0
    expanded = 0

    # Priority queue for UCS (heapq used as min-heap)
    fringe = []
    heapq.heappush(fringe, (0, start))  # (path_cost, position)
    
    
    # Dictionary to store the cost to reach each cell
    cost_so_far = {start: 0}
    
    # Parent dictionary to reconstruct the path
    came_from = {start: None}
    
    while fringe:
        # Get the cell with the lowest cost
        current_cost, current = heapq.heappop(fringe)
        expanded += 1
        
        # If we reach the goal, stop
        if current == goal:
            break
        
        # Explore all possible movements
        for action, (dr, dc, move_cost) in moves.items():
            next_row = current[0] + dr
            next_col = current[1] + dc
            next_pos = (next_row, next_col)
            
            # Check if the next position is within bounds and walkable
            if grid.is_valid_cell(next_row, next_col):
                # Calculate the new cost
                new_cost = current_cost + move_cost
                generated += 1
                
                # Only explore this position if it's cheaper to reach it this way
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    heapq.heappush(fringe, (new_cost, next_pos))
                    came_from[next_pos] = current
    
    # Reconstruct the path by tracing back from the goal
    path = []
    if goal in came_from:
        current = goal
        while current:
            path.append(current)
            current = came_from[current]
        path.reverse()  # The path was constructed from goal to start, so reverse it
    
    #print(f"Number of moves: {len(path)}")
    print(path)
    print("suck")
    return (path, cost_so_far.get(goal, float('inf'))), generated, expanded  # Return the path and the cost to reach the goal

iddfs_generated = 0

def iddfs(grid, start, goal):
    expanded = 0
    
    def dls(node, goal, depth):
        """Performs a Depth-Limited Search (DLS)"""
        if node == goal:
            return [node]  # Found the goal, return the path
        if depth == 0:
            return None  # Reached depth limit, no solution found here
        row, col = node
        # Explore neighbors (up, down, left, right)
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            #expanded += 1
            next_row, next_col = row + move[0], col + move[1]
            global iddfs_generated
            iddfs_generated += 1
            next_node = (next_row, next_col)
            # Ensure the move is within bounds of the grid
            if 0 <= next_row <= len(grid) and 0 <= next_col <= len(grid[0]):
                result = dls(next_node, goal, depth - 1)
                if result is not None:
                    return ([node] + result)  # Append current node to the path
        return None  # No solution found at this depth

    # Iterative deepening starts here
    for depth in range(1000):  # Arbitrary depth limit to avoid infinite loops
        result = dls(start, goal, depth)
        expanded += 1
        if result is not None:
            return result, expanded  # Return the path if found
    return None  # No solution found
def agent_IDDFs_Search(self, dirty_rooms):
        for room in dirty_rooms:
            path = iddfs(self.grid.grid, self.position, room)
            self.position = path[-1]
            i = 0
            #up.8, down.7, left1, right.9, clean.6
            while i < len(path) - 1:
                if path[i][1] > path[i+1][1]:
                    self.total_cost += 1
                if path[i][1] < path[i+1][1]:
                    self.total_cost += .9
                if path[i][0] < path[i+1][0]:
                    self.total_cost += .7
                if path[i][0] > path[i+1][0]:
                    self.total_cost += .8
                i += 1
            self.grid.mark_clean(self.position[0], self.position[1])  # Clean the room
            self.total_cost += 0.6
            self.total_cost = round(self.total_cost, 1)

# Example usage
if __name__ == "__main__":

    

    #Problem Statment 1:

    # Create a 4x5 grid

    grid1 = Grid(4, 5)
    grid1.mark_dirty(1, 2)
    grid1.mark_dirty(2, 4)
    grid1.mark_dirty(3, 5)
    
    #uc tree search
    
    print(f"Instance 1 Uniform Cost Tree Search:\n")
    agent1 = Agent(grid1, (2,2))
    agent1.agent_uniform_cost_search([(1, 2), (2, 4), (3, 5)])
    print(f"Total cost: {agent1.total_cost}\n")
    grid1.display()
    print("\n\n")
    
    
    grid1a = Grid(4, 5)
    grid1a.mark_dirty(1, 2)
    grid1a.mark_dirty(2, 4)
    grid1a.mark_dirty(3, 5)
    
    #uc graph search
    
    print(f"Instance 1 Uniform Cost Graph Search:\n")
    agent2 = Agent(grid1a, (2,2))
    agent2.agent_graph_search([(1, 2), (2, 4), (3, 5)])
    print(f"Total cost: {agent2.total_cost}\n")
    grid1a.display()
    print("\n\n")
    
    grid1b = Grid(4, 5)
    grid1b.mark_dirty(1, 2)
    grid1b.mark_dirty(2, 4)
    grid1b.mark_dirty(3, 5)
    
    print(f"Instance 1 Iterative Deepening Tree Search:\n")
    agent5 = Agent(grid1b, (2,2))
    agent5.agent_IDDFs_Search([(1, 2), (2, 4), (3, 5)])
    print(f"Total cost: {agent5.total_cost}\n")
    grid1b.display()
    print("\n\n")
    


    #Problem Statement 2:
    grid2 = Grid(4, 5)
    grid2.mark_dirty(1, 2)
    grid2.mark_dirty(2, 1)
    grid2.mark_dirty(2, 4)
    grid2.mark_dirty(3, 3)


    print(f"Instance 2 Uniform Cost Tree Search:\n")
    agent3 = Agent(grid2, (3,2))
    agent3.agent_uniform_cost_search([(1, 2), (2, 1), (2, 4), (3, 3)])
    print(f"Total cost: {agent3.total_cost}\n")
    grid2.display()
    print("\n\n")
    
    
    grid2a = Grid(4, 5)
    grid2a.mark_dirty(1, 2)
    grid2a.mark_dirty(2, 1)
    grid2a.mark_dirty(2, 4)
    grid2a.mark_dirty(3, 3)
    
    print(f"Instance 2 Uniform Cost Graph Search:\n")
    agent4 = Agent(grid2a, (3,2))
    agent4.agent_graph_search([(1, 2), (2, 1), (2, 4), (3, 3)])
    print(f"Total cost: {agent4.total_cost}\n")
    grid2a.display()
    print("\n\n")
    

    grid2b = Grid(4, 5)
    grid2b.mark_dirty(1, 2)
    grid2b.mark_dirty(2, 1)
    grid2b.mark_dirty(2, 4)
    grid2b.mark_dirty(3, 3)
    
    print(f"Instance 2 Iterative Deepening Tree Search:\n")
    agent6 = Agent(grid2b, (3,2))
    agent6.agent_IDDFs_Search([(1, 2), (2, 1), (2, 4), (3, 3)])
    print(f"Total cost: {agent6.total_cost}\n")
    grid2b.display()


    
    
    
    
