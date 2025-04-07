# Simple-Ray-Casting
Interactive Matrix Display with Shadows



![Uploading DemoRayCast.gif…]()






# Ray Casting Shadow Simulation

This project simulates light and shadow in a 2D grid using simple ray casting.
A light source casts rays across the grid, and objects block light to cast shadows.

---

## Grid Setup

- The grid is of size `r × c` (rows × columns).
- A square is placed at a defined position.
- A light source is placed at another position.

Let:
  - `(s_x, s_y)` be the top-left position of the square.
  - `(l_x, l_y)` be the position of the light source.
  - `square_size` be the height of the square (stretched horizontally).

---

## Ray Casting: Shadow Logic

For each point `(x, y)` on the grid, we compute a direction vector
from the light source to that point:

    \vec{d} = (x - l_x, y - l_y)

We normalize this direction vector:

    \text{distance} = \sqrt{(x - l_x)^2 + (y - l_y)^2}

    \hat{d} = \left( \frac{x - l_x}{\text{distance}}, \frac{y - l_y}{\text{distance}} \right)

---

## Stepping Through the Ray

We step from the light source to `(x, y)` along the direction vector:

    (rx, ry) = \left\lfloor l_x + t \cdot \hat{d}_x \right\rfloor, \left\lfloor l_y + t \cdot \hat{d}_y \right\rfloor

Where:

    t = 1, 2, ..., \left\lfloor \text{distance} \right\rfloor

At each `(rx, ry)`, we check:

    (rx, ry) \in \text{objects}
    \Rightarrow \text{point } (x, y) \text{ is in shadow}

---

## Grid Marking

Each grid cell is marked as follows:

- `*` : Light source
- `.` : Square (object)
- `▒` : Shadow
- `█` : Lit background (not in shadow)

---

## Example Scenario

Let:
  - Light source at: `(0, 0)`
  - Square at: `(2, 2)`
  - Grid size: `6 × 6`

We want to determine if a point like `(4, 4)` is in shadow.

Step-by-step:

1. Direction vector:

       \vec{d} = (4 - 0, 4 - 0) = (4, 4)

2. Normalize:

       \hat{d} = \left( \frac{4}{\sqrt{32}}, \frac{4}{\sqrt{32}} \right)

3. Step along this ray and check if it intersects the square at `(2, 2)`.

    → If yes, the point `(4, 4)` is in shadow.

---

## Output

The result is a simple ASCII grid showing the light, square, shadows, and lit areas.

