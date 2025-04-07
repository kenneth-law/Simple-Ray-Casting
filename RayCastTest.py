import math

def cast(r=5, c=5, square_pos=[3,3], square_size=1, light_pos=[1, 1]):
    
    rows, cols = r, c
    # Track occupied points for shadow calculation
    objects = set()
    matrix = [[' ' for _ in range(cols)] for _ in range(rows)]

    
    
    # Add a square if position is provided
    if square_pos:
        sx, sy = square_pos
        h_stretch = 1  # Make the square wider
        for y in range(max(0, sy), min(rows, sy + square_size)):
            for x in range(max(0, sx), min(cols, sx + square_size * h_stretch)):
                matrix[y][x] = '.'
                objects.add((x, y))


    print(objects)


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


cast(
            6, 6,
            square_pos=[2, 2],
            square_size=1,
            light_pos=[0,0]
        )
