import time
import os
import random

# Define constants for visuals
EMOJI_ANT = "🐜"
EMOJI_VISITED = "🟩"  # Trail left behind
EMOJI_EMPTY = "⬜"

class TorusGrid:
    """
    A simulation environment representing a 2D grid on a torus (wraps around).
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Start in the middle of the grid
        self.ant_x = width // 2
        self.ant_y = height // 2
        
        # A set to store tuples of (x, y) coordinates the ant has visited.
        # We include the starting position immediately.
        self.visited = {(self.ant_x, self.ant_y)}
        
        self.game_over = False
        self.status_message = "Simulation Running"

    @property
    def is_full(self):
        """Returns True if every cell in the grid has been visited."""
        return len(self.visited) >= (self.width * self.height)

    def move_ant(self, direction):
        """
        Attempts to move the ant in a direction ('N', 'S', 'E', 'W').
        Returns True if move was successful, False if move was invalid (revisiting).
        """
        if self.game_over:
            return False

        dx, dy = 0, 0
        
        # Map direction strings to coordinate changes
        if direction == 'N': dy = -1
        elif direction == 'S': dy = 1
        elif direction == 'E': dx = 1
        elif direction == 'W': dx = -1
        else:
            # If the user returns an invalid direction, we just skip the turn
            return True

        # Calculate new coordinates
        # The % operator handles the Torus wrapping automatically.
        # e.g., if x is 9 and width is 10, (9+1)%10 = 0 (wraps to start)
        # e.g., if x is 0 and width is 10, (0-1)%10 = 9 (wraps to end)
        new_x = (self.ant_x + dx) % self.width
        new_y = (self.ant_y + dy) % self.height

        # Check constraints: Cannot revisit old cells
        if (new_x, new_y) in self.visited:
            self.game_over = True
            self.status_message = f"CRASH! Ant tried to revisit ({new_x}, {new_y})."
            return False

        # Update state
        self.ant_x = new_x
        self.ant_y = new_y
        self.visited.add((new_x, new_y))

        # Check win condition
        if self.is_full:
            self.game_over = True
            self.status_message = "SUCCESS! Grid is full."
        
        return True

    def render(self):
        """Prints the grid to the console."""
        # Clear the console (works on Windows and Unix-based systems)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"Grid Size: {self.width}x{self.height} | Visited: {len(self.visited)}")
        print(f"Status: {self.status_message}")
        print("-" * (self.width * 2 + 2))

        # Loop through every coordinate to decide what to draw
        for y in range(self.height):
            row_str = ""
            for x in range(self.width):
                if x == self.ant_x and y == self.ant_y:
                    row_str += EMOJI_ANT
                elif (x, y) in self.visited:
                    row_str += EMOJI_VISITED
                else:
                    row_str += EMOJI_EMPTY
            print(row_str)
        print("-" * (self.width * 2 + 2))

# ---------------------------------------------------------
# YOUR SECTION: Define the Ant's Logic Here
# ---------------------------------------------------------

def get_ant_decision(grid_width, grid_height, 
                     current_pos, 
                     visited_set,
                     previous_moves):
    """
    Determines the next move for the ant.
    
    Args:
        grid_width: Total width of grid.
        grid_height: Total height of grid.
        current_pos: Tuple (x, y) of current ant location.
        visited_set: Set of all (x, y) tuples already visited.
        last_direction: The direction ('N', 'S', 'E', 'W') the ant moved last turn, or None if first turn.
        
    Returns:
        One of 'N', 'S', 'E', 'W'.
    """
    if previous_moves == []:
        last_direction = None
    else:
        last_direction = previous_moves[-1]

    if last_direction == 'E':
        return 'N'
    else:
        return 'E'
    # --- EXAMPLE STRATEGY: Random Valid Move ---
    # This is a placeholder. You can replace this logic!
    
    x, y = current_pos
    possible_moves = [('N', 0, -1), ('S', 0, 1), ('E', 1, 0), ('W', -1, 0)]
    valid_directions = []

    for direction, dx, dy in possible_moves:
        # Calculate theoretical next step with wrapping
        nx = (x + dx) % grid_width
        ny = (y + dy) % grid_height
        
        # Only add to list if we haven't been there
        if (nx, ny) not in visited_set:
            valid_directions.append(direction)

    if valid_directions:
        return random.choice(valid_directions)
    else:
        # No valid moves left (trapped!)
        return 'N' # Will cause a crash in the simulation loop

# ---------------------------------------------------------
# Main Execution Loop
# ---------------------------------------------------------

def run_simulation():
    # 1. Setup
    WIDTH = 12
    HEIGHT = 10
    sim = TorusGrid(WIDTH, HEIGHT)
    previous_moves = []
    
    # 2. Loop
    while not sim.game_over:
        sim.render()
        
        # Get the user's decision
        # We pass copies or raw data so the user has info to make a decision
        move_dir = get_ant_decision(
            sim.width, 
            sim.height, 
            (sim.ant_x, sim.ant_y), 
            sim.visited,
            previous_moves = previous_moves
        )
        
        # Apply the move
        sim.move_ant(move_dir)
        previous_moves.append(move_dir)
        
        # Slow down so we can see the animation
        time.sleep(0.2)

    # 3. Final State
    sim.render()
    print("Simulation Ended.")

if __name__ == "__main__":
    run_simulation()
