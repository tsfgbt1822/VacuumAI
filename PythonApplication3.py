import heapq
import copy

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





if __name__ == "__main__":

    #Problem Statment 1:

    # Create a 4x5 grid

    grid1 = Grid(4, 5)

    

    agent_row = 2

    agent_col = 2

    



    grid1.mark_dirty(1, 2)

    grid1.mark_dirty(2, 4)

    grid1.mark_dirty(3, 5)

    

    # Display the grid

    grid1.display()



    # Problem Statement 2:
    



# Helper function to copy the agent and grid
def copy_agent(agent: Agent) -> Agent:
    # Deep copy of grid and agent to avoid mutating original objects
    new_grid = Grid(agent.grid.rows, agent.grid.cols)
    new_grid.grid = [row[:] for row in agent.grid.grid]
    new_agent = Agent(new_grid, agent.position)
    new_agent.total_cost = agent.total_cost
    return new_agent

# Define the successor function
def successor_fn(agent: Agent):
    successors = []
    actions = [
        ('Left', agent.move_left, 1.0),
        ('Right', agent.move_right, 0.9),
        ('Up', agent.move_up, 0.8),
        ('Down', agent.move_down, 0.7),
        ('Suck', agent.suck, 0.6)
    ]

    # For each possible action, create a successor state
    for action_name, action, action_cost in actions:
        # Create a copy of the agent and grid for the next state
        new_agent = copy_agent(agent)
        action()  # Apply the action to the new agent
        successors.append((action_name, new_agent, action_cost))

    return successors

# Uniform cost tree search
def uniform_cost_tree_search(agent: Agent):
    fringe = []
    heapq.heappush(fringe, (0, agent))  # Insert the initial agent state with cost 0
    expanded = 0  # Counter for expanded nodes

    while fringe:
        cost, current_agent = heapq.heappop(fringe)  # Pop the agent with the lowest cost
        
        if current_agent.is_goal_reached():  # Check if the grid is fully clean
            return current_agent, expanded  # Return the agent and the number of nodes expanded

        expanded += 1

        # Generate successors from the current agent state
        for action_name, next_agent, step_cost in successor_fn(current_agent):
            heapq.heappush(fringe, (cost + step_cost, next_agent))  # Push successors into the fringe with updated cost

    return None, expanded  # Return None if no solution is found


# Uniform cost graph search
def uniform_cost_graph_search(agent: Agent):
    fringe = []
    heapq.heappush(fringe, (0, agent))  # Insert the initial agent state with cost 0
    closed = set()  # Set to store states that have already been expanded
    expanded = 0  # Counter for expanded nodes

    while fringe:
        cost, current_agent = heapq.heappop(fringe)  # Pop the agent with the lowest cost
        
        if current_agent.is_goal_reached():  # Check if the grid is fully clean
            return current_agent, expanded  # Return the agent and the number of nodes expanded

        state_repr = (current_agent.position, tuple(map(tuple, current_agent.grid.grid)))
        if state_repr not in closed:
            closed.add(state_repr)
            expanded += 1

            # Generate successors from the current agent state
            for action_name, next_agent, step_cost in successor_fn(current_agent):
                heapq.heappush(fringe, (cost + step_cost, next_agent))  # Push successors into the fringe with updated cost

    return None, expanded  # Return None if no solution is found


# Iterative deepening search
def iterative_deepening_search(agent: Agent):
    def depth_limited_search(agent, depth_limit):
        if agent.is_goal_reached():
            return agent
        if depth_limit == 0:
            return None
        for action_name, next_agent, step_cost in successor_fn(agent):
            result = depth_limited_search(next_agent, depth_limit - 1)
            if result is not None:
                return result
        return None

    depth = 0
    while True:
        result = depth_limited_search(copy_agent(agent), depth)
        if result:
            return result
        depth += 1
