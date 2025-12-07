
with open('input.txt', 'r') as f:
    lines = f.readlines()

width = len(lines[0]) - 1
height = len(lines)

def get_xy(x: int, y: int):
    return lines[y][x]

# False = empty, True = filled 
def check_xy(x: int, y: int):
    if x < 0 or y < 0:
        return False
    
    if x >= width or y >= height:
        return False 
    
    return get_xy(x, y) == '@'

avail = 0

def can_be_removed(x, y) -> bool:
    roll_count = 0

    # Check the 8 adjacent positions in a 3x3 grid, ignoring the middle slot 
    for a in range(-1, 2):
        for b in range(-1, 2):
            # ignore middle slot 
            if a == 0 and b == 0:
                continue 

            if check_xy(x + a, y + b):
                roll_count += 1

    return roll_count < 4

def remove_rolls():
    num_removed = 0

    for x in range(width):
        for y in range(height):
            if get_xy(x, y) != '@':
                continue 

            if can_be_removed(x, y):
                num_removed += 1
                row = lines[y]
                lines[y] = row[:x] + '.' + row[x+1:]

    return num_removed 

prev_avail = 0
avail = 0
while True:
    avail += remove_rolls()

    if avail == prev_avail:
        break 

    prev_avail = avail

print(f"{width=} {height=}")
print(f"answer: {avail}")
