This project simulates an intelligent vacuum cleaner agent operating in a 2D grid environment. Each cell in the grid can be either clean or dirty, and the agent must navigate the grid to clean all dirty cells efficiently.

The agent uses the following search strategies to determine the optimal path:

- Uniform Cost Tree Search
- Uniform Cost Graph Search
- Iterative Deepening Depth-First Search (IDDFS)

Each movement and cleaning action incurs a specific cost:
- Move Left: 1.0
- Move Right: 0.9
- Move Up: 0.8
- Move Down: 0.7
- Clean (Suck): 0.6

The simulation reports metrics such as total execution time, number of moves, nodes generated, nodes expanded, and total cost. This allows for a comparative analysis of search strategies in agent-based pathfinding tasks.
