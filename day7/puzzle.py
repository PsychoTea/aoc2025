
with open('input.txt') as f:
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

print("output")

for line in new_lines:
    print(line)
    
print(f"{num_splits=}")