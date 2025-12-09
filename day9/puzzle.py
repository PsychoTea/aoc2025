import sys 
import functools 

class Board:
    def __init__(self: Board) -> None:
        self.vertices: list[tuple[int, int]] = [ ] 

    def get_tile(self: Board, x: int, y: int) -> bool:
        return (x, y) in self.vertices

    def add(self: Board, x: int, y: int) -> None:
        if self.get_tile(x, y):
            # return 
            assert False, f"Error: tried to add a tile @ {x}, {y} which was already in the board: {self.vertices}"

        self.vertices.append((x, y))

    def find_largest_area(self: Board) -> list[tuple[tuple[int, int], tuple[int, int]], int]:
        areas = [ ]

        N = len(self.vertices)
        num_comparisons = (N * (N - 1)) // 2
        comparisons = 0

        best_area = 0

        for i, point1 in enumerate(self.vertices):
            for point2 in self.vertices[i + 1:]:
                if (comparisons % (num_comparisons // 10)) == 0:
                    print(f"Calculating: {comparisons} / {num_comparisons}")

                comparisons += 1

                # Calculate the area of the given rectangle
                area = (abs(point1[0] - point2[0]) + 1) * (abs(point1[1] - point2[1]) + 1)

                if area <= best_area:
                    continue 

                # Check if the given rectangle drawn between point{1,2} fits within the polygon
                if not self._rectangle_fits(point1, point2):
                    continue 

                best_area = area 

                areas.append((
                    point1,
                    point2,
                    area
                ))

        return areas

    @functools.cache 
    def _point_on_segment(self: Board, px: int, py: int, x1: int, y1: int, x2: int, y2: int) -> bool:
        # Check if point P is collinear with segment endpoints
        # Cross product (P - A) × (B - A) should be 0 for collinearity
        cross = (px - x1) * (y2 - y1) - (py - y1) * (x2 - x1)
        if cross != 0:
            return False

        # Check if P is within bounding box of the segment
        if px < min(x1, x2) or px > max(x1, x2):
            return False
        if py < min(y1, y2) or py > max(y1, y2):
            return False

        return True

    @functools.cache 
    def _point_in_polygon(self: Board, px: int, py: int) -> bool:
        inside = False 

        vertices_count = len(self.vertices)

        # 1. Optional: check if P is exactly on any edge
        for i in range(vertices_count):
            j = (i + 1) % vertices_count
            (x1, y1) = self.vertices[i]
            (x2, y2) = self.vertices[j]

            if self._point_on_segment(px, py, x1, y1, x2, y2):
                return True

        # 2. Ray casting: count intersections with a horizontal ray to the right
        for i in range(vertices_count):
            j = (i + 1) % vertices_count
            (xi, yi) = self.vertices[i]
            (xj, yj) = self.vertices[j]

            # Check if edge straddles the horizontal line at py
            # (yi > py) != (yj > py) means py is between yi and yj (exclusive)
            if ((yi > py) != (yj > py)):
                # Compute x-coordinate of intersection of edge with line y = py
                x_intersect = xi + (py - yi) * (xj - xi) / (yj - yi)

                # If intersection is to the right of P, toggle "inside"
                if x_intersect > px:
                    inside = not inside

        return inside 

    @functools.cache 
    def _rectangle_fits(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        x_min, x_max = sorted((x1, x2))
        y_min, y_max = sorted((y1, y2))

        # 1) Corner check 
        if not self._point_in_polygon(x_min, y_min): return False
        if not self._point_in_polygon(x_min, y_max): return False
        if not self._point_in_polygon(x_max, y_min): return False
        if not self._point_in_polygon(x_max, y_max): return False

        # 2) Edge intersection check
        V = self.vertices
        n = len(V)

        for i in range(n):
            x3, y3 = V[i]
            x4, y4 = V[(i + 1) % n]

            # Skip edges completely outside the rectangle's bounding box
            if max(x3, x4) <= x_min or min(x3, x4) >= x_max:
                # edge is entirely to the left or right
                continue

            if max(y3, y4) <= y_min or min(y3, y4) >= y_max:
                # edge is entirely below or above
                continue

            # At this point, bounding boxes overlap; check actual segment–rectangle intersection.
            if self._segment_intersects_rectangle(x3, y3, x4, y4, x_min, y_min, x_max, y_max):
                return False

        return True

    @functools.cache 
    def _segment_intersects_rectangle(
        self: Board,
        x1: int, y1: int,
        x2: int, y2: int,
        x_min: int, y_min: int,
        x_max: int, y_max: int
    ) -> bool:
        """
        Return True if the segment (x1,y1)-(x2,y2) has any part
        in the *interior* of the rectangle (x_min,x_max) x (y_min,y_max).

        Touching only on the rectangle boundary (edges or corners)
        returns False.
        """
        dx = x2 - x1
        dy = y2 - y1

        # Liang–Barsky clipping against the closed rectangle
        t0, t1 = 0.0, 1.0
        for p, q in (
            (-dx, x1 - x_min),  # x >= x_min
            ( dx, x_max - x1),  # x <= x_max
            (-dy, y1 - y_min),  # y >= y_min
            ( dy, y_max - y1),  # y <= y_max
        ):
            if p == 0:
                # Segment is parallel to this boundary
                if q < 0:
                    # Entire segment is outside this boundary
                    return False
                # Otherwise, no constraint from this boundary
                continue

            r = q / p
            if p < 0:
                # Entering boundary
                if r > t1:
                    return False
                if r > t0:
                    t0 = r
            else:  # p > 0
                # Leaving boundary
                if r < t0:
                    return False
                if r < t1:
                    t1 = r

        if t0 > t1:
            # No overlap with the rectangle at all
            return False

        # Segment intersects the *closed* rectangle for t in [t0, t1].
        # Take a midpoint of the clipped segment and check if that
        # point lies in the *open* interior (strict inequalities).
        tm = (t0 + t1) * 0.5
        xm = x1 + tm * dx
        ym = y1 + tm * dy

        return (x_min < xm < x_max) and (y_min < ym < y_max)

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

board = Board()

print(f"Creating board...")

for line in lines:
    line = line.strip('\n')

    parts = line.split(',')

    board.add(
        int(parts[0], 10),
        int(parts[1], 10)
    )

print(f"Calculating areas...")
areas = board.find_largest_area()

print(f"Sorting areas...")
areas = sorted(areas, key = lambda x: x[2])

for item in areas:
    (x1, y1), (x2, y2), area = item 

    print(f"t1: {x1}, {y1}, t2: {x2} {y2}, area: {area}")

# answer = 1566346198