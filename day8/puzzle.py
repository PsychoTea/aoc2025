import sys 
import math 
import functools 
from typing import Tuple 

class Box:
    def __init__(self: Box, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.circuit = None 

    @functools.cache 
    def distance_to(self: Box, box: Box) -> float:
        return pow(self.x - box.x, 2) + pow(self.y - box.y, 2) + pow(self.z - box.z, 2)

    def __str__(self: Box) -> str:
        return f"x: {self.x}, y: {self.y}, z: {self.z}"

class Circuit:
    index = 1

    def __init__(self: Circuit) -> None:
        self.boxes = [ ]

        self.id = Circuit.index 
        Circuit.index += 1

    def __str__(self: Circuit) -> str:
        return f"Circuit({self.id}) ({len(self.boxes)} boxes)"

    def count(self: Circuit) -> int:
        return len(self.boxes)

    def contains_box(self: Circuit, box: Box) -> bool:
        return box in self.boxes 

    def add_box(self: Circuit, box: Box) -> None:
        # Box is already in this circuit 
        if self.contains_box(box):
            return 

        box.circuit = self 
        self.boxes.append(box)

    # Connect two circuits together 
    def connect(self: Circuit, circuit: Circuit) -> bool:
        if self == circuit:
            return False 

        for box in circuit.boxes:
            self.add_box(box)

        circuit.boxes.clear()

        return True 

# Parse the input and create a circuit for each box
def create_boxes(input: list[str]) -> list[Box]:
    all_boxes = [ ]

    for line in input:
        parts = line.strip('\n').split(',')

        x = int(parts[0], 10)
        y = int(parts[1], 10)
        z = int(parts[2], 10)

        box = Box(x, y, z)

        circuit = Circuit()
        circuit.add_box(box)

        all_boxes.append(box)

    return all_boxes

# Calculate the distances between all unique boxes
def find_distances(all_boxes: list[Box]) -> Tuple[Box, Box, float]:
    distances = [ ]

    for i, box1 in enumerate(all_boxes):
        for box2 in all_boxes[i + 1:]:
            distances.append((
                box1, 
                box2, 
                box1.distance_to(box2))
            )

    return distances 

def main():
    with open(sys.argv[1], "r") as f:
        lines = f.readlines()

    print("Parsing input...")
    all_boxes = create_boxes(lines)

    print("Calculating distances...")
    all_distances = find_distances(all_boxes)

    print(f"Number of distances: {len(all_distances)}")

    print("Sorting distances...")
    all_distances = sorted(all_distances, key = lambda x: x[2])

    # Part 1: connect the first 1000 circuits

    print("Connecting circuits...")
    for boxes in all_distances[:1000]:
        boxes[0].circuit.connect(boxes[1].circuit)

    # Find all unique circuits
    all_circuits = { box.circuit for box in all_boxes }

    print("Sorting circuits...")
    circuits_sorted = sorted(all_circuits, key = lambda x: x.count(), reverse = True)

    # Sanity check we haven't lost any circuits
    assert sum([x.count() for x in circuits_sorted]) == len(lines)

    answer = math.prod([circuits_sorted[i].count() for i in range(3)])
    print(f"Part 1 answer = {answer}")

    # Part 2: continue connecting all boxes

    last_connection = (None, None)
    for boxes in all_distances[1000:]:
        if boxes[0].circuit.connect(boxes[1].circuit):
            # Record the last successful connection 
            last_connection = boxes

    print(f"Answer = {last_connection[0].x * last_connection[1].x}")

    # Part 1 answer = 133574
    # Part 2 answer = 2435100380

if __name__ == "__main__":
    main()