import sys 

with open(sys.argv[1]) as f:
    lines = f.readlines()

new_lines = [ ]

for i, line in enumerate(lines):
    line = line.strip('\n')

    if i == 0:
        new_lines.append(line)
        continue

    curr_line = ""

    for j, char in enumerate(line):
        next_char = line[j + 1] if j + 1 < len(line) else None 
        prev_char = line[j - 1] if j - 1 >= 0 else None 

        if next_char == '^':
            # check char above next is line
            if new_lines[i - 1][j + 1] == "|":
                curr_line += "|"
                continue 

        if prev_char == '^':
            if new_lines[i - 1][j - 1] == "|":
                curr_line += "|"
                continue 

        if char == '.':
            prev_line = new_lines[i - 1]

            if prev_line[j] == 'S':
                curr_line += "|"
            elif prev_line[j] == "|":
                curr_line += "|"
            else:
                curr_line += "."

            continue 

        curr_line += char 

    new_lines.append(curr_line)

# search for all carots, check if pipe is present left, right, and above
num_splits = 0
for i, line in enumerate(new_lines):
    for j, char in enumerate(line):
        if char == '^':
            if new_lines[i - 1][j] == '|' and line[j - 1] == "|" and line[j + 1] == "|":
                num_splits += 1

all_nodes = [ ] 

class Node:
    def __init__(self, x, y):
        global all_nodes 
        
        self.x = x
        self.y = y

        all_nodes.append(self)

class Start(Node):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.down = None 

    def __str__(self) -> str:
        return f"Start: x = {self.x}, y = {self.y}, down = {self.down}"

class End(Node):
    def __str__(self) -> str:
        return f"End: x = {self.x}, y = {self.y}"

class Splitter(Node):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.left = None 
        self.right = None 

    def __str__(self) -> str:
        return f"Splitter: x = {self.x}, y = {self.y}, left = {type(self.left).__name__}, right = {type(self.right).__name__}"

print("output")

for line in new_lines:
    print(line)

print(f"{num_splits=}")

root_node = None 

for y, line in enumerate(new_lines):
    for x, char in enumerate(line):
        if char == 'S':
            root_node = Start(x, y)

            # Search down until we find the first splitter 
            off = 0 
            while True:
                if new_lines[y + off][x] == '^':
                    root_node.down = Splitter(x, y + off)
                    break 

                off += 1

def find_node(x, y):
    for node in all_nodes:
        if node.x == x and node.y == y:
            return node 
        
    return None 

def node_calculate(node):
    # if isinstance(node, End):
    #     return 
    if node == None:
        return 

    if node.left == None:
        # Search down the left side until we find a splitter, or the end 
        left_char = new_lines[node.y][node.x - 1]

        off = 0
        while left_char == '|':
            off += 1
            if node.y + off >= len(new_lines):
                left_char = None 
                break 
            
            left_char = new_lines[node.y + off][node.x - 1]

        if left_char == '^':
            if found_node := find_node(node.x -1, node.y + off):
                node.left = found_node
            else:
                node.left = Splitter(node.x - 1, node.y + off)
        elif left_char == None:
            if found_node := find_node(node.x + 1, node.y + off):
                node.left = found_node
            else:
                node.left = None
        else:
            print(f"Reached unknown char: {left_char}")

        node_calculate(node.left)

    if node.right == None:
        # Search down the right side until we find a splitter, or the end 
        right_char = new_lines[node.y][node.x + 1]

        off = 0
        while right_char == '|':
            off += 1
            if node.y + off >= len(new_lines):
                right_char = None 
                break 

            right_char = new_lines[node.y + off][node.x + 1]

        if right_char == '^':
            if found_node := find_node(node.x + 1, node.y + off):
                node.right = found_node
            else:
                node.right = Splitter(node.x + 1, node.y + off)
        elif right_char == None:
            if found_node := find_node(node.x + 1, node.y + off):
                node.right = found_node
            else:
                node.right = None
        else:
            print(f"Reached unknown char: {right_char}")

        node_calculate(node.right)

node_calculate(root_node.down)

print(f"calculated {len(all_nodes)} unique nodes")

print(root_node)

print(root_node.down)

# print("=== dumping nodes ===")

# for node in all_nodes:
#     print(node)

# Walk the tree from the root node to each possible End node 
def walk_node(node):
    # if node is None:
    #     return 0

    if node == None:
        return 1

    return walk_node(node.left) + walk_node(node.right)

print("walking nodes...")
found_ends = walk_node(root_node.down)
print(f"{found_ends=}")
