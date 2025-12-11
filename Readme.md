# Pathfinder

![Pathfinding Algorithm Visualizer](https://img.shields.io/badge/Python-3.7%2B-blue)
![PyGame](https://img.shields.io/badge/PyGame-2.0%2B-green)
![Algorithms](https://img.shields.io/badge/Algorithms-12%2B-orange)
![Mazes](https://img.shields.io/badge/Mazes-10%2B-purple)

An interactive pathfinding algorithm visualizer with comprehensive visualization capabilities, featuring 12+ pathfinding algorithms and 10+ maze generation techniques. This tool provides real-time visualization of search algorithms with detailed statistics, performance metrics, and educational insights.

## Key Features

### **Pathfinding Algorithms (12+)**
- **Basic Algorithms**: A* Search, Dijkstra's Algorithm, Breadth-First Search, Depth-First Search, Greedy Best-First
- **Advanced Algorithms**: Bidirectional Search, Jump Point Search, IDA* Search
- **Heuristic Algorithms**: Swarm Algorithm, Convergent Swarm

### **Maze Generation (10+)**
- Random Obstacles
- Recursive Division Maze
- Prim's Algorithm Maze
- Kruskal's Algorithm Maze
- Depth-First Search Maze
- Cellular Automata Maze
- Spiral Maze
- Sidewinder Maze
- Binary Tree Maze
- Eller's Algorithm Maze

### **Interactive Features**
- Real-time algorithm visualization with color-coded states
- Interactive grid editing (draw/erase obstacles)
- Adjustable search speed (5x to 100x)
- Tabbed interface for easy navigation
- Comprehensive statistics and metrics
- Multiple heuristic functions

## Algorithm Details & Mathematics

### **A* Search Algorithm**
- **Heuristic Function**: Manhattan Distance with 8-direction movement
- **Cost Calculation**: `f(n) = g(n) + h(n)`
  - `g(n)`: Actual cost from start node to node n
  - `h(n)`: Heuristic estimate from node n to goal
- **Movement Costs**: 
  - Orthogonal moves: 10 units
  - Diagonal moves: 14 units (approximation of √2)
- **Mathematical Foundation**: Guarantees optimal path when heuristic is admissible (never overestimates)

### **Dijkstra's Algorithm**
- **Special Case**: A* with `h(n) = 0` for all nodes
- **Complexity**: O((V + E) log V) with binary heap
- **Guarantee**: Finds shortest path in weighted graphs
- **Use Case**: When all edge weights are non-negative

### **Bidirectional Search**
- **Concept**: Simultaneous search from start and goal
- **Termination**: When search frontiers meet
- **Advantage**: Reduces search space from O(b^d) to O(b^(d/2))
- **Mathematical Benefit**: Exponential reduction in nodes visited

### **Heuristic Functions**
1. **Manhattan Distance**: `h(n) = |x₁ - x₂| + |y₁ - y₂|`
2. **Diagonal Heuristic**: Combines Manhattan with diagonal movement
3. **Swarm Intelligence**: Pheromone-based path reinforcement

### **Jump Point Search Optimization**
- **Key Insight**: Symmetry reduction in uniform-cost grids
- **Mathematical Principle**: Prunes neighbors that don't change the optimal path
- **Performance**: Can be orders of magnitude faster than A* on uniform grids

## Installation

### **Requirements**
- Python 3.7+
- PyGame 2.0+

### **Installation Steps**
```bash
# Clone the repository
git clone https://github.com/praisejamesx/pathfinder.git
cd pathfinder

# Install dependencies
pip install pygame

# Run the visualizer
python main.py
```

### **Optional: Install with Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pygame
python main.py
```

## Usage Guide

### **Interface Overview**
```
┌─────────────────────────────────────┬─────────────────┐
│                                     │                 │
│           GRID VISUALIZATION        │   SIDEBAR UI    │
│                                     │                 │
│  • Cells color-coded by state       │  • Algorithm    │
│  • Real-time search animation       │    selection    │
│  • Path tracing                     │  • Maze         │
│                                     │    generation   │
│                                     │  • Controls     │
│                                     │  • Statistics   │
└─────────────────────────────────────┴─────────────────┘
```

### **Color Coding System**
- **White**: Empty/Unvisited cells
- **Dark Blue**: Blocked/Obstacle cells
- **Green**: Active/Frontier cells
- **Red**: Closed/Visited cells
- **Purple**: Final path
- **Light Blue**: Start position
- **Blue**: Goal/Target position

### **Controls**
| Key/Action | Function |
|------------|----------|
| **Left Click** | Draw/erase obstacles |
| **Right Click** | Move start position |
| **Space** | Pause/resume search |
| **R** | Reset current search |
| **C** | Clear all obstacles |
| **G** | Generate selected maze |
| **Tab** | Switch between tabs |
| **1-5** | Quick algorithm select |
| **ESC** | Quit application |

## Algorithm Performance Comparison

### **Theoretical Complexities**
| Algorithm | Time Complexity | Space Complexity | Optimality |
|-----------|-----------------|------------------|------------|
| A* Search | O(b^d) | O(b^d) | Yes |
| Dijkstra | O((V+E) log V) | O(V) | Yes |
| BFS | O(V+E) | O(V) | Yes (unweighted) |
| DFS | O(V+E) | O(V) | No |
| Greedy BFS | O(b^m) | O(b^m) | No |
| Bidirectional | O(b^(d/2)) | O(b^(d/2)) | Yes |

Where:
- **b**: Branching factor
- **d**: Solution depth
- **V**: Number of vertices
- **E**: Number of edges
- **m**: Maximum search depth

### **Practical Performance Metrics**
The visualizer tracks:
- **Visited Cells**: Number of cells explored
- **Path Length**: Number of steps in final path
- **Execution Time**: Real-time search duration
- **Search Speed**: Configurable visualization speed

## Maze Generation Algorithms

### **Recursive Division**
- **Complexity**: O(n log n) for n cells
- **Principle**: Recursively divides space with walls, leaving gaps
- **Mathematical Insight**: Creates perfect mazes with exactly one solution

### **Prim's Algorithm**
- **Complexity**: O(E log V)
- **Principle**: Minimum spanning tree construction
- **Visual Effect**: Creates natural, branching paths

### **Cellular Automata**
- **Rule Set**: Conway's Game of Life-inspired
- **Iterations**: Multiple passes for smoothing
- **Result**: Organic, cave-like structures

### **Spiral Maze**
- **Pattern**: Archimedean spiral generation
- **Complexity**: O(n) for n cells
- **Visual Appeal**: Artistic, winding paths

## Code Architecture

### **Main Components**
```
pathfinding_visualizer.py
├── Cell Class
│   ├── Pathfinding state management
│   ├── Neighbor calculation
│   └── Cost computation
├── PathfindingAlgorithms Class
│   ├── Step-by-step algorithm implementations
│   ├── Heuristic calculations
│   └── State management
├── MazeGenerator Class
│   ├── 10+ maze generation algorithms
│   ├── Grid manipulation
│   └── Visualization updates
├── PathfindingVisualizer Class
│   ├── Main game loop
│   ├── UI management
│   └── Event handling
└── UI Components
    ├── Button and Tab systems
    ├── Statistics display
    └── Interactive controls
```

### **Key Data Structures**
- **Grid**: Dictionary of Cell objects indexed by (x,y) coordinates
- **Open Set**: Priority queue for frontier cells (A*, Dijkstra)
- **Closed Set**: List of visited cells
- **Pheromone Map**: Dictionary for swarm algorithm reinforcement

### **Mathematical Functions**
```python
# Heuristic calculation (Manhattan with diagonal)
def get_h(self, goal_pos):
    dx = abs(goal_pos[0] - self.pos[0])
    dy = abs(goal_pos[1] - self.pos[1])
    self.h_cost = 10 * (dx + dy)  # Manhattan distance

# Movement cost calculation
def get_distance_to(self, other_cell):
    dx = abs(other_cell.pos[0] - self.pos[0])
    dy = abs(other_cell.pos[1] - self.pos[1])
    if dx == 1 and dy == 1:
        return 14  # Diagonal: √2 ≈ 1.414, scaled by 10
    return 10  # Orthogonal
```

## Educational Value

### **Learning Objectives**
1. **Algorithm Analysis**: Compare time/space complexities visually
2. **Heuristic Design**: Understand how different heuristics affect search
3. **Optimization Techniques**: Learn about algorithm-specific optimizations
4. **Problem-Solving**: Develop intuition for pathfinding challenges

### **Classroom Applications**
- **Computer Science**: Algorithm design and analysis
- **Mathematics**: Graph theory and optimization
- **Artificial Intelligence**: Search strategies and heuristics
- **Robotics**: Path planning fundamentals

## Performance Optimization

### **Efficient Data Structures**
- **Priority Queue Simulation**: List with `min()` for simplicity
- **Neighbor Caching**: Pre-computed to avoid repeated calculations
- **State Management**: Efficient cell state updates with minimal redraws

### **Visualization Optimizations**
- **Partial Updates**: Only redraw changed cells
- **Frame Rate Control**: Configurable FPS for smooth animation
- **Memory Management**: Reuse cell objects instead of recreation

## Future Enhancements

### **Planned Features**
- [ ] Additional algorithms (Theta*, D* Lite, HPA*)
- [ ] 3D visualization support
- [ ] Weighted grid cells
- [ ] Dynamic obstacles
- [ ] Multi-agent pathfinding
- [ ] Benchmarking suite
- [ ] Export statistics to CSV
- [ ] Custom heuristic editor
- [ ] Web version with JavaScript

### **Research Applications**
- **Algorithm Development**: Test new pathfinding algorithms
- **Heuristic Analysis**: Compare heuristic performance
- **Educational Research**: Study algorithm learning patterns

## Theoretical Background

### **Search Algorithms Classification**
```
Search Algorithms
├── Uninformed Search
│   ├── Breadth-First Search
│   ├── Depth-First Search
│   └── Dijkstra's Algorithm
├── Informed Search
│   ├── A* Search
│   ├── Greedy Best-First
│   └── IDA*
└── Advanced Techniques
    ├── Bidirectional Search
    ├── Swarm Intelligence
    └── Jump Point Optimization
```

### **Mathematical Foundations**
1. **Graph Theory**: Nodes, edges, paths, cycles
2. **Heuristic Theory**: Admissibility, consistency, dominance
3. **Optimization Theory**: Cost minimization, constraint satisfaction
4. **Computational Geometry**: Distance metrics, obstacle representation

## Development

### **Contributing**
1. Fork the repository
2. Create a feature branch
3. Implement improvements
4. Submit a pull request

### **Code Style**
- Follow PEP 8 guidelines
- Use descriptive variable names
- Include docstrings for functions
- Maintain modular architecture

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **PyGame Community**: For the excellent game development library
- **Algorithm Researchers**: For the pathfinding algorithms implemented
- **Open Source Contributors**: For inspiration and code examples

## Support

Buy me a coffee: https://selar.com/showlove/judahx
Read my essays: https://crive.substack.com

For questions, issues, or contributions:
- Open an issue on GitHub
- Contact the maintainer directly: praisejames011@gmail.com

---

**Built with ❤️ by praisejamesx** | *Exploring the boundaries of Cognition, Coordination and Computation*