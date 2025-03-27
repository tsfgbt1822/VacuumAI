This repository contains two different implementations of a vacuum cleaner agent designed to clean a grid-based environment. Each approach solves the same core problem — cleaning all dirty cells in a grid — but does so using different AI paradigms:

PythonApplication3.py: State-space search approach
PythonApplication4.py: Pathfinding-based navigation approach



PythonApplication3.py – State-Space Search
This version treats the entire grid and agent state as part of the search node. It explores possible sequences of actions (move up/down/left/right, suck) to reach a goal state where all cells are clean.

Key Features:
- Uses successor functions to generate all possible agent actions.
Implements:
- Uniform Cost Tree Search
- Uniform Cost Graph Search
- Iterative Deepening Search (IDS)



PythonApplication4.py – Pathfinding with Targeted Cleaning
This version treats each dirty cell as a sub-goal and uses pathfinding algorithms to move the agent directly to each dirty location in sequence.

Key Features:
The agent navigates the grid and cleans specific target cells.
Implements:
- Uniform Cost Search (Tree & Graph)
- Iterative Deepening Depth-First Search (IDDFS)
- Tracks detailed movement costs and prints performance metrics.


