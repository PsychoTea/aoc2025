import functools 
import sys 
from typing import NamedTuple

class Point(NamedTuple):
    x: int 
    y: int 

class Area(NamedTuple):
    point1: Point 
    point2: Point 
    area: int 

class Board:
    def __init__(self: Board) -> None:
        self.vertices: list[Point] = [ ] 

    def get_tile(self: Board, x: int, y: int) -> bool:
        return (x, y) in self.vertices

    def add(self: Board, x: int, y: int) -> None:
        if self.get_tile(x, y):
            assert False, f"Error: tried to add a tile @ {x}, {y} which was already in the board: {self.vertices}"

        self.vertices.append(Point(x, y))

    def find_largest_area(self: Board) -> list[Area]:
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
                area = (abs(point1.x - point2.x) + 1) * (abs(point1.y - point2.y) + 1)

                if area <= best_area:
                    continue 

                # Check if the given rectangle drawn between point{1,2} fits within the polygon
                if not self._rectangle_fits(point1, point2):
                    continue 

                best_area = area 

                areas.append(Area(
                    point1,
                    point2,
                    area
                ))

        return areas

    @functools.cache 
    def _point_on_segment(self: Board, point: Point, seg1: Point, seg2: Point) -> bool:
        # Check if point P is collinear with segment endpoints
        # Cross product (P - A) x (B - A) should be 0 for collinearity
        cross = (point.x - seg1.x) * (seg2.y - seg2.y) - (point.y - seg1.y) * (seg2.x - seg1.x)
        if cross != 0:
            return False

        # Check if P is within bounding box of the segment
        if point.x < min(seg1.x, seg2.x) or point.x > max(seg1.x, seg2.x):
            return False
        if point.y < min(seg1.y, seg2.y) or point.y > max(seg1.y, seg2.y):
            return False

        return True

    @functools.cache 
    def _point_in_polygon(self: Board, point: Point) -> bool:
        inside = False 

        vertices_count = len(self.vertices)

        # Check if P is exactly on any edge
        for i in range(vertices_count):
            j = (i + 1) % vertices_count
            point1 = self.vertices[i]
            point2 = self.vertices[j]

            if self._point_on_segment(point, point1, point2):
                return True

        # Ray casting; count intersections with a horizontal ray to the right
        for i in range(vertices_count):
            j = (i + 1) % vertices_count
            pointI = self.vertices[i]
            pointJ = self.vertices[j]

            # Check if edge straddles the horizontal line at py
            # (yi > py) != (yj > py) means py is between yi and yj (exclusive)
            if ((pointI.y > point.y) != (pointJ.y > point.y)):
                # Compute x-coordinate of intersection of edge with line y = py
                x_intersect = pointI.x + (point.y - pointI.y) * (pointJ.x - pointI.x) / (pointJ.y - pointI.y)

                # If intersection is to the right of P, toggle "inside"
                if x_intersect > point.x:
                    inside = not inside

        return inside 

    @functools.cache 
    def _rectangle_fits(self, point1: Point, point2: Point):
        # Check (opposite) corners of the rectangle
        if not self._point_in_polygon(Point(point1.x, point2.y)): return False
        if not self._point_in_polygon(Point(point2.x, point1.y)): return False

        x_min, x_max = sorted((point1.x, point2.x))
        y_min, y_max = sorted((point1.y, point2.y))

        # Edge intersection check
        V = self.vertices
        n = len(V)

        for i in range(n):
            point3 = V[i]
            point4 = V[(i + 1) % n]

            # Skip edges completely outside the rectangle's bounding box
            if max(point3.x, point4.x) <= x_min or min(point3.x, point4.x) >= x_max:
                # edge is entirely to the left or right
                continue

            if max(point3.y, point4.y) <= y_min or min(point3.y, point4.y) >= y_max:
                # edge is entirely below or above
                continue

            # At this point, bounding boxes overlap; check actual segment–rectangle intersection
            if self._segment_intersects_rectangle(point3, point4, x_min, y_min, x_max, y_max):
                return False

        return True

    @functools.cache 
    def _segment_intersects_rectangle(
        self: Board,
        point1: Point,
        point2: Point,
        x_min: int, y_min: int,
        x_max: int, y_max: int
    ) -> bool:
        """
        Return True if the segment (x1,y1)-(x2,y2) has any part
        in the *interior* of the rectangle (x_min,x_max) x (y_min,y_max).

        Touching only on the rectangle boundary (edges or corners)
        returns False.
        """
        dx = point2.x - point1.x
        dy = point2.y - point1.y

        # Liang–Barsky clipping against the closed rectangle
        t0, t1 = 0.0, 1.0
        for p, q in (
            (-dx, point1.x - x_min),  # x >= x_min
            ( dx, x_max - point1.x),  # x <= x_max
            (-dy, point1.y - y_min),  # y >= y_min
            ( dy, y_max - point1.y),  # y <= y_max
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

        # Segment intersects the *closed* rectangle for t in [t0, t1]
        # Take a midpoint of the clipped segment and check if that
        # point lies in the *open* interior (strict inequalities)
        tm = (t0 + t1) * 0.5
        xm = point1.x + tm * dx
        ym = point1.y + tm * dy

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
areas = sorted(areas, key = lambda x: x.area)

for (point1, point2, area) in areas:
    print(f"point 1: {point1.x}, {point1.y}, point 2: {point2.x} {point2.y}, area: {area}")

# answer = 1566346198