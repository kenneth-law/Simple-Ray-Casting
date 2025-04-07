import tkinter as tk
import time
import math

def createMatrix(r, c, circle_center=None, circle_radius=6, square_pos=None, square_size=5, light_pos=(1, 1)):
    # Create an r×c matrix and fill it with '█' 
    rows, cols = r, c
    matrix = [[' ' for _ in range(cols)] for _ in range(rows)]
    
    # Track occupied points for shadow calculation
    objects = set()
    
    # Add a circle if center is provided
    if circle_center:
        cx, cy = circle_center
        h_stretch = 2.0  # Horizontal stretch factor
        for y in range(rows):
            for x in range(cols):
                # Calculate distance with horizontal stretching
                distance = math.sqrt(((x - cx)/h_stretch)**2 + (y - cy)**2)
                if distance <= circle_radius:
                    matrix[y][x] = '.'
                    objects.add((x, y))
    
    # Add a square if position is provided
    if square_pos:
        sx, sy = square_pos
        h_stretch = 2  # Make the square wider
        for y in range(max(0, sy), min(rows, sy + square_size)):
            for x in range(max(0, sx), min(cols, sx + square_size * h_stretch)):
                matrix[y][x] = '.'
                objects.add((x, y))
    
    # Calculate shadows using simple ray casting
    lx, ly = light_pos
    for y in range(rows):
        for x in range(cols):
            # Skip if this is already an object
            if (x, y) in objects:
                continue
                
            # Skip the light source
            if x == lx and y == ly:
                matrix[y][x] = '*'  # Mark light source with *
                continue
                
            # Calculate direction from light to current point
            dx = x - lx
            dy = y - ly
            
            # Check if this point is in shadow
            in_shadow = False
            
            # Normalize direction for ray casting
            distance = math.sqrt(dx*dx + dy*dy)
            if distance > 0:
                dx, dy = dx/distance, dy/distance
                
                # Cast ray from light to current position
                for t in range(1, int(distance)):
                    rx = int(lx + dx * t)
                    ry = int(ly + dy * t)
                    
                    # Check if ray hit an object
                    if (rx, ry) in objects:
                        in_shadow = True
                        break
            
            # Mark shadow points
            if in_shadow:
                matrix[y][x] = '▒'  # Medium shade for shadows
            else:
                matrix[y][x] = '█'  # Solid block for background
    
    # Convert matrix to a string
    matrix_str = '\n'.join(''.join(row) for row in matrix)
    
    return matrix_str

def displayOut():
    root = tk.Tk()
    root.title("Interactive Matrix Display with Shadows")
    
    # Set the window background color
    root.configure(bg="black")
    
    # Create variables to store object positions
    circle_center = [40, 15]  # Initial position for circle
    square_pos = [70, 10]     # Initial position for square
    light_pos = [1, 1]        # Light source position
    
    # Create a frame to hold the labels
    main_frame = tk.Frame(root, bg="black")
    main_frame.pack(padx=10, pady=10)
    
    # Create the matrix label
    label = tk.Label(
        main_frame, 
        font=("Courier", 12), 
        justify="left",
        bg="black",
        fg="white"
    )
    label.pack()
    
    # Status frame
    status_frame = tk.Frame(root, bg="black")
    status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)
    
    # FPS counter
    fps_label = tk.Label(
        status_frame, 
        text="FPS: 0",
        bg="black", 
        fg="white"
    )
    fps_label.pack(side=tk.LEFT, padx=5)
    
    # Mouse position label
    mouse_pos_label = tk.Label(
        status_frame,
        text="Mouse: (0, 0)",
        bg="black",
        fg="white"
    )
    mouse_pos_label.pack(side=tk.RIGHT, padx=5)
    
    # Object selection label
    selection_label = tk.Label(
        status_frame,
        text="Click to move: Circle",
        bg="black",
        fg="white"
    )
    selection_label.pack(side=tk.LEFT, padx=20)
    
    # Track the object to move
    current_object = "circle"  # Options: "circle", "square", "light"
    
    # Track FPS
    last_time = time.time()
    frame_count = 0
    
    # Function to update mouse position
    def motion(event):
        mouse_x, mouse_y = event.x, event.y
        # Convert screen coordinates to matrix coordinates
        char_width = 10 
        char_height = 18
        matrix_x = max(0, min(99, int((event.x - 10) / char_width)))
        matrix_y = max(0, min(39, int((event.y - 10) / char_height)))
        mouse_pos_label.config(text=f"Matrix pos: ({matrix_x}, {matrix_y})")

        light_pos[0], light_pos[1] = matrix_x, matrix_y

        
        return matrix_x, matrix_y
    
    # Bind motion event to track mouse
    root.bind('<Motion>', motion)
    
    # Handle clicking to move objects
    def on_click(event):
        matrix_x, matrix_y = motion(event)
        nonlocal current_object
        
        # Move the selected object
        if current_object == "circle":
            circle_center[0], circle_center[1] = matrix_x, matrix_y
            current_object = "square"
            selection_label.config(text="Click to move: Square")
        elif current_object == "square":
            square_pos[0], square_pos[1] = matrix_x, matrix_y
            current_object = "circle"
            selection_label.config(text="Click to move: Circle")
    
    # Bind left mouse button click
    root.bind("<Button-1>", on_click)
    
    def update_display():
        nonlocal last_time, frame_count
        
        # Generate matrix with objects and shadows
        matrix_str = createMatrix(
            40, 100,
            circle_center=circle_center,
            circle_radius=6,
            square_pos=square_pos,
            square_size=5,
            light_pos=light_pos
        )
        label.config(text=matrix_str)
        
        # Calculate FPS
        current_time = time.time()
        frame_count += 1
        
        if current_time - last_time >= 1.0:
            fps = frame_count / (current_time - last_time)
            fps_label.config(text=f"FPS: {fps:.1f}")
            frame_count = 0
            last_time = current_time
        
        # Schedule next update
        root.after(16, update_display)
    
    # Start the update loop
    update_display()
    
    root.mainloop()
    
if __name__ == "__main__":
    displayOut()
