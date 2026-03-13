import time
import os
import random

# Define constants for visuals
EMOJI_FOURMI = "🐜"
EMOJI_VISITED = "⬛"  # Trail left behind
EMOJI_EMPTY = "🟨"

class TorusGrid:
    """
    A simulation environment representing a 2D grid on a torus (wraps around).
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Start in the middle of the grid
        self.fourmi_x = width // 2
        self.fourmi_y = height // 2
        
        # Prend note dans un tuple des coordonnées (x, y) le fourmi a visité.
        # on inclus la coordonnée ou se trouve la fourmi immédiatement.
        self.visited = {(self.fourmi_x, self.fourmi_y)}
        
        self.game_over = False
        self.status_message = "Simulation courante"

    @property
    def is_full(self):
        """Returns True if every cell in the grid has been visited."""
        return len(self.visited) >= (self.width * self.height)

    def bouger_fourmi(self, direction):
        """
        Essaye de bouger la fourmi dans un direction ('N', 'S', 'E', 'W').
        Returns True if move was successful, False if move was invalid (revisiting).
        """
        if self.game_over:
            return False

        dx, dy = 0, 0
        
        # Map direction strings to coordinate changes
        if direction == 'N': dy = -1
        elif direction == 'NE': 
            dx = 1
            dy = -1
        elif direction == 'E': dx = 1
        elif direction == 'SE':
            dx = 1
            dy = 1
        elif direction == 'S': dy = 1
        elif direction == 'SW':
            dx = -1
            dy = 1
        elif direction == 'W': dx = -1
        elif direction == 'SW':
            dx = -1
            dy = -1
        else:
            # If the user returns an invalid direction, we just skip the turn
            return True

        # Calculate new coordinates
        # The % operator handles the Torus wrapping automatically.
        # e.g., if x is 9 and width is 10, (9+1)%10 = 0 (wraps to start)
        # e.g., if x is 0 and width is 10, (0-1)%10 = 9 (wraps to end)
        new_x = (self.fourmi_x + dx) % self.width
        new_y = (self.fourmi_y + dy) % self.height

        # Check constraints: Cannot revisit old cells
        if (new_x, new_y) in self.visited:
            self.game_over = True
            self.status_message = f"CRASH! Ant tried to revisit ({new_x}, {new_y})."
            return False

        # Update state
        self.fourmi_x = new_x
        self.fourmi_y = new_y
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
                if x == self.fourmi_x and y == self.fourmi_y:
                    row_str += EMOJI_FOURMI
                elif (x, y) in self.visited:
                    row_str += EMOJI_VISITED
                else:
                    row_str += EMOJI_EMPTY
            print(row_str)
        print("-" * (self.width * 2 + 2))

# ---------------------------------------------------------
# Logique de la fourmi
# ---------------------------------------------------------

def prendre_fourmi_decision(grid_width, grid_height, 
                     current_pos, 
                     visited_set,
                     previous_moves):
    
    if previous_moves == []:
        last_direction = None
    else:
        last_direction = previous_moves[-1]

    if last_direction == 'E':
        return 'NE'  
    else:
        return 'E'
    
# ---------------------------------------------------------
# Loop d'execution de la simulation
# ---------------------------------------------------------

def run_simulation():
    # 1. Setup
    WIDTH = 11
    HEIGHT = 10
    sim = TorusGrid(WIDTH, HEIGHT)
    previous_moves = []
    
    # 2. Loop
    while not sim.game_over:
        sim.render()
        
        move_dir = prendre_fourmi_decision(
            sim.width, 
            sim.height, 
            (sim.fourmi_x, sim.fourmi_y), 
            sim.visited,
            previous_moves = previous_moves
        )
        
        # Applucation de la mouvement du fourmi
        sim.bouger_fourmi(move_dir)
        previous_moves.append(move_dir)
        
        # ralentit la fourmi pur qu'on peut voir la mouvement
        time.sleep(0.2)

    # 3. Fin du simulation
    sim.render()
    print("Simulation Ended.")

if __name__ == "__main__":
    run_simulation()
