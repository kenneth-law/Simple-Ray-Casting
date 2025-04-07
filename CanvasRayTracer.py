import tkinter as tk
import time
import math
import random


class RaycastRenderer:
    def __init__(self, root, width=1000, height=800):
        self.root = root
        self.width = width
        self.height = height

        # Set the window background color
        self.root.configure(bg="black")
        self.root.title("Canvas Raycast Renderer")

        # Create the main canvas
        self.canvas = tk.Canvas(root, width=width, height=height, bg="black", highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)

        # Grid dimensions (cells)
        self.grid_width = 100
        self.grid_height = 70

        # Calculate cell size
        self.cell_width = width / self.grid_width
        self.cell_height = height / self.grid_height

        # Setup objects
        self.circle_center = [40, 15]  # Initial position for circle
        self.square_pos = [70, 10]  # Initial position for square
        self.light_pos = [20, 15]  # Light source position

        # Current mouse position for light tracking
        self.mouse_x = 0
        self.mouse_y = 0

        # Settings
        self.enable_reflections = True
        self.light_intensity = 100
        self.diffusion_amount = 0.1
        self.follow_mouse = False  # Toggle for light following mouse

        # Object colors
        self.circle_color = "#00B000"  # Green circle
        self.square_color = "#B00000"  # Red square
        self.light_color = "#FFF0C8"  # Warm white light

        # Cell references (for updating)
        self.cells = {}

        # Status bar
        self.status_frame = tk.Frame(root, bg="black")
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)

        # FPS counter
        self.fps_label = tk.Label(
            self.status_frame,
            text="FPS: 0",
            bg="black",
            fg="white"
        )
        self.fps_label.pack(side=tk.LEFT, padx=5)

        # Object selection label
        self.selection_label = tk.Label(
            self.status_frame,
            text="Click to move: Circle",
            bg="black",
            fg="white"
        )
        self.selection_label.pack(side=tk.LEFT, padx=20)

        # Light intensity label
        self.light_label = tk.Label(
            self.status_frame,
            text=f"Light: {self.light_intensity}",
            bg="black",
            fg="white"
        )
        self.light_label.pack(side=tk.RIGHT, padx=5)

        # Reflection toggle label
        self.reflection_label = tk.Label(
            self.status_frame,
            text=f"Reflections: {'ON' if self.enable_reflections else 'OFF'}",
            bg="black",
            fg="white"
        )
        self.reflection_label.pack(side=tk.RIGHT, padx=5)

        # Mouse position label
        self.mouse_pos_label = tk.Label(
            self.status_frame,
            text="Mouse: (0, 0)",
            bg="black",
            fg="white"
        )
        self.mouse_pos_label.pack(side=tk.RIGHT, padx=5)

        # Mouse follow toggle label
        self.follow_label = tk.Label(
            self.status_frame,
            text="Follow Mouse: OFF",
            bg="black",
            fg="white"
        )
        self.follow_label.pack(side=tk.RIGHT, padx=5)

        # Bind events
        self.setup_bindings()

        # FPS tracking
        self.last_time = time.time()
        self.frame_count = 0

        # Current object to move
        self.current_object = "circle"  # Options: "circle", "square", "light"

        # Initial render
        self.create_grid()
        self.update_display()  # Initial update (no render loop yet)

    def setup_bindings(self):
        # Mouse movement tracking
        self.canvas.bind("<Motion>", self.on_mouse_move)

        # Click handling
        self.canvas.bind("<Button-1>", self.on_click)

        # Key bindings - use simple functions to prevent freezing
        self.root.bind("<w>", lambda e: self.move_light_key("up"))
        self.root.bind("<s>", lambda e: self.move_light_key("down"))
        self.root.bind("<a>", lambda e: self.move_light_key("left"))
        self.root.bind("<d>", lambda e: self.move_light_key("right"))
        self.root.bind("<plus>", lambda e: self.adjust_light_intensity(10))
        self.root.bind("<minus>", lambda e: self.adjust_light_intensity(-10))
        self.root.bind("<equal>", lambda e: self.adjust_light_intensity(10))
        self.root.bind("<r>", lambda e: self.toggle_reflections())
        self.root.bind("<f>", lambda e: self.toggle_follow_mouse())

    def create_grid(self):
        """Create the initial grid of rectangles for the cells"""
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                x1 = x * self.cell_width
                y1 = y * self.cell_height
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_height

                # Create rectangle and save the ID
                rect_id = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill="black",
                    outline="",
                    tags=f"cell_{x}_{y}"
                )

                self.cells[(x, y)] = rect_id

    def hex_to_rgb(self, hex_color):
        """Convert hex color string to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, rgb):
        """Convert RGB tuple to hex color string"""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    def adjust_color_brightness(self, color, factor):
        """Adjust color brightness by factor (0.0 to 1.0)"""
        factor = factor * 1.1
        (r, g, b) = self.hex_to_rgb(color)
        r = int(min(r * factor, 255))
        g = int(min(g * factor, 255))
        b = int(min(b * factor, 255))
        return self.rgb_to_hex((r, g, b))

    def mix_colors(self, color1, color2, weight2=0.5):
        """Mix two hex colors with the given weight for the second color"""
        r1, g1, b1 = self.hex_to_rgb(color1)
        r2, g2, b2 = self.hex_to_rgb(color2)
        weight1 = 1 - weight2
        r = int(r1 * weight1 + r2 * weight2)
        g = int(g1 * weight1 + g2 * weight2)
        b = int(b1 * weight1 + b2 * weight2)
        return self.rgb_to_hex((r, g, b))

    def blend_colors(self, color1, color2, blend_factor):
        """Blend colors based on blend factor (0-1)"""
        return self.mix_colors(color1, color2, blend_factor)

    def on_mouse_move(self, event):
        """Handle mouse movement"""
        # Convert canvas coordinates to grid coordinates
        x = min(max(0, int(event.x / self.cell_width)), self.grid_width - 1)
        y = min(max(0, int(event.y / self.cell_height)), self.grid_height - 1)

        # Store current mouse position
        self.mouse_x, self.mouse_y = x, y

        # Update position label
        self.mouse_pos_label.config(text=f"Mouse: ({x}, {y})")

        # Update light position if following mouse
        if self.follow_mouse:
            self.light_pos[0], self.light_pos[1] = x, y

        return x, y

    def on_click(self, event):
        """Handle mouse clicks to move objects"""
        x, y = self.on_mouse_move(event)

        # Move the selected object
        if self.current_object == "circle":
            self.circle_center = [x, y]
            self.current_object = "square"
            self.selection_label.config(text="Click to move: Square")
        elif self.current_object == "square":
            self.square_pos = [x, y]
            self.current_object = "light"
            self.selection_label.config(text="Click to move: Light")
        else:  # light
            self.light_pos = [x, y]
            self.current_object = "circle"
            self.selection_label.config(text="Click to move: Circle")

    def move_light_key(self, direction):
        """Handle WASD key presses to move light - simplified to prevent freezing"""
        if direction == "up" and self.light_pos[1] > 0:
            self.light_pos[1] -= 1
        elif direction == "down" and self.light_pos[1] < self.grid_height - 1:
            self.light_pos[1] += 1
        elif direction == "left" and self.light_pos[0] > 0:
            self.light_pos[0] -= 1
        elif direction == "right" and self.light_pos[0] < self.grid_width - 1:
            self.light_pos[0] += 1



        # Update light position label
        self.mouse_pos_label.config(text=f"Light: ({self.light_pos[0]}, {self.light_pos[1]})")

    def adjust_light_intensity(self, amount):
        """Adjust light intensity by amount"""
        self.light_intensity = min(200, max(10, self.light_intensity + amount))
        self.light_label.config(text=f"Light: {self.light_intensity}")

    def toggle_reflections(self):
        """Toggle reflections on/off"""
        self.enable_reflections = not self.enable_reflections
        self.reflection_label.config(text=f"Reflections: {'ON' if self.enable_reflections else 'OFF'}")

    def toggle_follow_mouse(self):
        """Toggle whether light follows the mouse cursor"""
        self.follow_mouse = not self.follow_mouse
        self.follow_label.config(text=f"Follow Mouse: {'ON' if self.follow_mouse else 'OFF'}")

    def calculate_lighting(self):
        """Calculate lighting and shadows for the scene"""
        # Create intensity and color matrices
        intensity_matrix = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        color_matrix = [["#000000" for _ in range(self.grid_width)] for _ in range(self.grid_height)]

        # Track objects and reflective surfaces
        objects = set()
        reflective_objects = set()
        object_colors = {}

        # Add circle with proper aspect ratio
        cx, cy = self.circle_center
        radius = 6
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                # Skip if far from circle center for performance
                if abs(x - cx) > radius * 2 or abs(y - cy) > radius * 2:
                    continue

                # Calculate distance with aspect ratio correction
                # We use cell_width/cell_height ratio to correct the aspect ratio
                aspect_ratio = self.cell_width / self.cell_height
                dx = x - cx
                dy = (y - cy) / aspect_ratio
                distance = math.sqrt(dx * dx + dy * dy)

                if distance <= radius:
                    objects.add((x, y))
                    object_colors[(x, y)] = self.circle_color

                    # Mark circle edge as reflective
                    if radius - 0.5 <= distance <= radius:
                        # Calculate normal vector (pointing outward from center)
                        nx = dx / distance if distance > 0 else 0
                        ny = dy / distance if distance > 0 else 0
                        reflective_objects.add((x, y, nx, ny))

        # Add square with corrected aspect ratio
        sx, sy = self.square_pos
        size_x = 5  # Horizontal size
        size_y = int(5 * self.cell_height / self.cell_width)  # Adjusted vertical size

        for y in range(max(0, sy), min(self.grid_height, sy + size_y)):
            for x in range(max(0, sx), min(self.grid_width, sx + size_x)):
                objects.add((x, y))
                object_colors[(x, y)] = self.square_color

                # Mark square edges as reflective
                if self.enable_reflections:
                    # Left edge
                    if x == sx:
                        reflective_objects.add((x, y, -1, 0))
                    # Right edge
                    elif x == sx + size_x - 1:
                        reflective_objects.add((x, y, 1, 0))
                    # Top edge
                    elif y == sy:
                        reflective_objects.add((x, y, 0, -1))
                    # Bottom edge
                    elif y == sy + size_y - 1:
                        reflective_objects.add((x, y, 0, 1))

        # Light position
        lx, ly = self.light_pos

        # Direct lighting
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                # Skip objects
                if (x, y) in objects:
                    continue

                # Mark light source
                if x == lx and y == ly:
                    intensity_matrix[y][x] = self.light_intensity * 2
                    color_matrix[y][x] = self.light_color
                    continue

                # Calculate direction to point
                dx = x - lx
                dy = y - ly
                distance = math.sqrt(dx * dx + dy * dy)

                # Check for shadows
                in_shadow = False
                if distance > 0:
                    dx /= distance
                    dy /= distance

                    # Cast ray from light to current position
                    for t in range(1, int(distance)):
                        rx = int(lx + dx * t)
                        ry = int(ly + dy * t)

                        if 0 <= rx < self.grid_width and 0 <= ry < self.grid_height:
                            if (rx, ry) in objects:
                                in_shadow = True
                                break

                # Calculate light intensity with falloff
                if not in_shadow:
                    if distance < 1:
                        distance = 1

                    # Inverse square law
                    falloff_intensity = min(self.light_intensity / (distance * 0.5), self.light_intensity)
                    intensity_matrix[y][x] += falloff_intensity
                    color_matrix[y][x] = self.light_color

        # Calculate reflections
        if self.enable_reflections:
            for ref_x, ref_y, normal_x, normal_y in reflective_objects:
                # Check if surface receives direct light
                receives_direct_light = False

                # Vector from light to reflective surface
                ldx = ref_x - lx
                ldy = ref_y - ly
                light_distance = math.sqrt(ldx * ldx + ldy * ldy)

                if light_distance > 0:
                    # Normalize
                    ldx /= light_distance
                    ldy /= light_distance

                    # Cast ray from light to reflective surface
                    blocked = False
                    for t in range(1, int(light_distance)):
                        rx = int(lx + ldx * t)
                        ry = int(ly + ldy * t)

                        if 0 <= rx < self.grid_width and 0 <= ry < self.grid_height:
                            if (rx, ry) in objects and (rx != ref_x or ry != ref_y):
                                blocked = True
                                break

                    if not blocked:
                        receives_direct_light = True

                # Calculate reflected light
                if receives_direct_light:
                    # Get color of reflective object
                    if (ref_x, ref_y) in object_colors:
                        reflection_color = object_colors[(ref_x, ref_y)]
                    else:
                        reflection_color = "#FFFFFF"

                    # Calculate reflection vector (from surface to light)
                    incoming_x = lx - ref_x
                    incoming_y = ly - ref_y

                    # Normalize incoming vector
                    incoming_len = math.sqrt(incoming_x ** 2 + incoming_y ** 2)
                    if incoming_len > 0:
                        incoming_x /= incoming_len
                        incoming_y /= incoming_len

                    # Calculate reflection
                    dot_product = normal_x * incoming_x + normal_y * incoming_y
                    reflected_x = 2 * dot_product * normal_x - incoming_x
                    reflected_y = 2 * dot_product * normal_y - incoming_y

                    # Add diffusion
                    reflected_x += (random.random() - 0.5) * self.diffusion_amount
                    reflected_y += (random.random() - 0.5) * self.diffusion_amount

                    # Normalize
                    ref_len = math.sqrt(reflected_x ** 2 + reflected_y ** 2)
                    if ref_len > 0:
                        reflected_x /= ref_len
                        reflected_y /= ref_len

                    # Cast reflected ray
                    max_reflection_distance = 40
                    reflection_intensity = self.light_intensity * 0.4
                    reflection_intensity /= (light_distance * 0.1)

                    # Mix colors for reflection
                    mixed_color = self.mix_colors(self.light_color, reflection_color, 0.7)

                    for t in range(1, max_reflection_distance):
                        rx = int(ref_x + reflected_x * t)
                        ry = int(ref_y + reflected_y * t)

                        if 0 <= rx < self.grid_width and 0 <= ry < self.grid_height:
                            if (rx, ry) in objects:
                                break

                            # Attenuate with distance
                            reflection_falloff = reflection_intensity / (t * 0.5)

                            # Add to intensity matrix
                            intensity_matrix[ry][rx] += reflection_falloff

                            # Blend colors
                            if intensity_matrix[ry][rx] > 0:
                                existing = intensity_matrix[ry][rx] - reflection_falloff
                                if existing <= 0:
                                    color_matrix[ry][rx] = mixed_color
                                else:
                                    blend_factor = reflection_falloff / intensity_matrix[ry][rx]
                                    color_matrix[ry][rx] = self.blend_colors(color_matrix[ry][rx], mixed_color,
                                                                             blend_factor)

        return objects, object_colors, intensity_matrix, color_matrix

    def update_display(self):
        """Update the canvas rendering based on current state"""
        # Update light position if following mouse
        if self.follow_mouse:
            self.light_pos[0], self.light_pos[1] = self.mouse_x, self.mouse_y

        objects, object_colors, intensity_matrix, color_matrix = self.calculate_lighting()

        # Light source location
        lx, ly = self.light_pos

        # Update all cells
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                cell_id = self.cells.get((x, y))
                if not cell_id:
                    continue  # Skip if cell doesn't exist

                # Handle objects
                if (x, y) in objects:
                    color = object_colors.get((x, y), "#FFFFFF")
                    self.canvas.itemconfig(cell_id, fill=color)
                    continue

                # Handle light source
                if x == lx and y == ly:
                    self.canvas.itemconfig(cell_id, fill=self.light_color)
                    continue

                # Handle regular lighting
                intensity = intensity_matrix[y][x]
                base_color = color_matrix[y][x]

                # Scale color by intensity
                if intensity <= 0.1:
                    color = "#000000"  # Complete shadow
                else:
                    brightness = min(intensity / self.light_intensity, 1.0)
                    color = self.adjust_color_brightness(base_color, brightness)

                self.canvas.itemconfig(cell_id, fill=color)

        # Update FPS counter
        self.frame_count += 1
        current_time = time.time()
        if current_time - self.last_time >= 1.0:
            fps = self.frame_count / (current_time - self.last_time)
            self.fps_label.config(text=f"FPS: {fps:.1f}")
            self.frame_count = 0
            self.last_time = current_time

        # Schedule next update
        self.root.after(16, self.update_display)


def main():
    root = tk.Tk()
    app = RaycastRenderer(root)

    # Display help
    help_text = """
    Controls:
    - Click to move objects
    - WASD to move light source
    - F to toggle light following mouse cursor
    - +/- to adjust light intensity
    - R to toggle reflections
    """
    print(help_text)

    root.mainloop()


if __name__ == "__main__":
    main()